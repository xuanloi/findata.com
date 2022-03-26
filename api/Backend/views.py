# Create your views here.
from rest_framework import status, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Backend.models import *
import os, psycopg2, ast
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse, FileResponse
from django.db.models import Q
from django.apps import apps
from django.http.request import QueryDict
from django.contrib.auth.hashers import make_password, check_password
from huey.contrib import djhuey as huey
from django.core.mail import EmailMessage
from django.db import models as aggregator
from django.db.models.functions import Concat
from django.db.models import F, Value, CharField, Q, Count, Min, Max, Sum


#==========DATABASE CONNECTION==================================
dbHost     = settings.DATABASES['default']['HOST']
dbUsername = settings.DATABASES['default']['USER']
dbPassword = settings.DATABASES['default']['PASSWORD']
dbName     = settings.DATABASES['default']['NAME']
connection = 'host=' + dbHost + ' dbname=' + dbName + ' user=' + dbUsername + ' password=' + dbPassword
#======================================================================================================

limit_rows = 2000
perpage = 20
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
static_folder = os.path.join(BASE_DIR, "static")   

# Get limit rows
#=============================================================================
def get_limit_rows(rows, page, onpage):
    total_rows = len(rows)
    full_data = True if (total_rows <= limit_rows) or page == -1 else False

    if full_data == True and onpage != None:
        full_data = False if total_rows > onpage else full_data

    if full_data == False:
        onpage = onpage if onpage != None else perpage
        rows = rows[(page-1) * onpage : page * onpage]
    return total_rows, full_data, rows

#=============================================================================
def get_serializer(name, depthDefault=0):
    try:
        Model = apps.get_model('Backend', name)
    except:
        return None, None

    class GenericSerializer(serializers.ModelSerializer):
        class Meta:
            model = Model
            fields = '__all__'
            depth = depthDefault

        def create(self, validated_data):
            return Model.objects.create(**validated_data)
        
        def update(self, instance, validated_data):
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            instance.save()
            return instance

    return Model, GenericSerializer


#=============================================================================
#--- One function for get all data ---
domain_list = ['https://www.findata.vn', 'https://findata.vn', 'http://localhost:3000', 'http://www.findata.com.vn', 'http://findata.com.vn']


#=============================================================================
def base_query(rows, values, summary, distinct_values, sort):
    need_serializer = True   
    if  values != None:
        rows = rows.values(*values)
        need_serializer = False
    if summary =='distinct':
        distinct_values = '' if distinct_values==None else distinct_values.split(',')
        rows = rows.distinct(*distinct_values)
    elif summary == 'count':
        rows = rows.count()
    elif summary =='annotate':
        array = [{'key': 'Count',  'val': Count}, {'key': 'Min', 'val': Min}, {'key': 'Max', 'val': Max}, {'key': 'Sum', 'val': Sum}]
        for key, value in ast.literal_eval(distinct_values).items():   #
            print(key, value)
            if isinstance(value, str) == True:
                reducer = getattr(aggregator, value)
                rows = rows.annotate(**{key: reducer(key)})
            else:
                if value['type'] == 'Concat':
                    arr = []
                    char = value['char'] if 'char' in value else '|'
                    for idx, field in enumerate(value['field']):
                        arr.append(F(field))
                        arr.append(Value(char)) if idx < len(value['field']) - 1 else False
                    reducer = Concat(*arr, output_field=CharField())
                    rows = rows.annotate(**{key: reducer})

                elif next(iter([o for o in array if o['key']==value['type']]), None) != None:
                    arr = Q()
                    for fkey in value['condition']:
                        arr.add(Q(**{fkey: value['condition'][fkey]}), Q.AND)
                    Func = next(iter([o for o in array if o['key']==value['type']]))
                    reducer = Func['val'](value['field'], filter=arr)
                    rows = rows.annotate(**{key: reducer})

    if sort != None:
        rows = rows.order_by(*sort)
    return rows, need_serializer


#=============================================================================
@api_view(['GET', 'POST'])
def data_list(request, name):
    Model, serializer_class = get_serializer(name)
    if Model == None:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    filter = request.query_params['filter'] if request.query_params.get('filter') != None else None
    values = request.query_params['values'] if request.query_params.get('values') != None else None
    values = values if values==None else values.split(',')
    summary = request.query_params['summary'] if request.query_params.get('summary') != None else None
    page = int(request.query_params['page']) if request.query_params.get('page') != None else 1
    onpage = int(request.query_params['perpage']) if request.query_params.get('perpage') != None else None
    sort = request.query_params['sort'] if request.query_params.get('sort') != None else None
    sort = '' if sort==None else sort.split(',')
    distinct_values = request.query_params['distinct_values'] if request.query_params.get('distinct_values') != None else None
    filter_or = request.query_params['filter_or'] if request.query_params.get('filter_or') != None else None
    exclude = request.query_params['exclude'] if request.query_params.get('exclude') != None else None

    need_serializer = True    
    filter_list = Q()
    if filter_or != None:
        for key, value in ast.literal_eval(filter_or).items():
            filter_list.add(Q(**{key: value}), Q.OR)

    if filter != None:
        for key, value in ast.literal_eval(filter).items():
            filter_list.add(Q(**{key: value}), Q.AND)

    if request.method == 'GET':
        rows = Model.objects.all() if len(filter_list) == 0 else Model.objects.filter(filter_list)
        if exclude != None:
            exclude_list = Q()
            for key, value in ast.literal_eval(exclude).items():
                exclude_list.add(Q(**{key: value}), Q.AND)
            rows = rows.exclude(exclude_list)
        rows, need_serializer = base_query(rows, values, summary, distinct_values, sort)
        
        #manage_request(request, 926, rows, name)
        total_rows, full_data, rows = get_limit_rows(rows, page, onpage)
        rows = rows if need_serializer == False else serializer_class(rows, many=True).data
        return Response({'total_rows': total_rows, 'full_data': full_data, 'rows': rows})

    elif request.method == 'POST':
        serializer = serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            #manage_request(request,926, [1], name)

            data = serializer.data    
            if values != None:
                data = Model.objects.filter(id=data['id']).values(*values).first()

            return Response(data, status=status.HTTP_201_CREATED)
        
        #manage_request(request,927, None, name)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#=============================================================================
#---Get object detail ---

@api_view(['GET', 'PUT', 'DELETE'])
def data_detail(request, name, pk):
    values = request.query_params['values'] if request.query_params.get('values') != None else None
    values = values if values==None else values.split(',')
    summary = request.query_params['summary'] if request.query_params.get('summary') != None else None
    sort = request.query_params['sort'] if request.query_params.get('sort') != None else None
    sort = '' if sort==None else sort.split(',')
    distinct_values = request.query_params['distinct_values'] if request.query_params.get('distinct_values') != None else None

    Model, serializer_class = get_serializer(name)
    if Model == None:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        obj = Model.objects.get(pk=pk)
    except Model.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializer_class(obj)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = serializer_class(obj, request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            if values != None:
                rows = Model.objects.filter(id=data['id'])
                rows, need_serializer = base_query(rows, values, summary, distinct_values, sort)
                return Response(rows.first())
            else:
                return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if name == 'File' or name == 'Image' or name == 'Video':
            file_name = static_folder + ('/' + name.lower() + 's/') + obj.file
            if os.path.exists(file_name):
                os.remove(file_name)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#=============================================================================
@api_view(['GET'])
def get_hash(request, name):
    if request.method == 'GET':
        password = make_password(name)
        return Response({'total_rows': 1, 'full_data': True , 'rows': [password]})
           
    return Response(status = status.HTTP_400_BAD_REQUEST)


#=============================================================================
@api_view(['GET'])
def login(request):
    if request.method == 'GET':
        filter = request.query_params['filter'] if request.query_params.get('filter') != None else None
        filter = ast.literal_eval(filter)

        user = Account.objects.filter(email=filter['email']).first()
        if user == None:
            return Response({'total_rows': 0, 'full_data': True})

        result = check_password(filter['password'], user.password)
        if result == False:
            return Response({'total_rows': 0, 'full_data': True})

        Model, serializer_class = get_serializer('Account', 1)
        serializer = serializer_class(user)
        return Response({'total_rows': 1, 'full_data': True , 'rows': serializer.data})
    
    return Response(status = status.HTTP_400_BAD_REQUEST)


#=============================================================================
#--- Validata data function ---

@api_view(['POST'])
def validate_import(request, name):    
    Model, serializer_class = get_serializer(name)
    if Model == None:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    data = request.data
    action = None
    if request.query_params.get('action') != None:
        action = request.query_params['action']
    else:
        Response(status=status.HTTP_400_BAD_REQUEST)

    array = []
    for obj in data:
        try:
            filter = {}
            if name=='Task':
                if action == 'import':
                    filter = {'company': obj['company'], 'report_period': obj['report_period'], 'year': obj['year'], 'report_name': obj['report_name'], 'report_type': obj['report_type']}
                elif action=='delete' or action=='approve':
                    filter = {'id': obj['id']}

            if name=='Task_Stock':
                filter = {'report_name': obj['report_name'], 'stock_date': obj['stock_date']}
                
            elif name=='Report_Item':
                filter = {'item': obj['item']}

            elif name=='Classification':
                filter = {'category': obj['category'], 'classify': obj['classify'], 'code': obj['code']}

            elif name=='Company':
                filter = {'stock_code': obj['stock_code']}

            elif name == 'Stock_Price' or name == 'Stock_Order' or name == 'Foreign_Order' or name == 'Foreign_Deal':
                filter = {'stock_date': obj['stock_date'], 'company': obj['company']}

            elif name == 'Price_Live':
                filter = {'stock_date': obj['stock_date'], 'time': obj['time'], 'company': obj['company']}

            elif name=='Industry':
                filter = {'level3_code': obj['level3_code']}
   
            thelist = Model.objects.filter(**filter)
            if len(thelist)==0:
                if action=='delete' or action=='approve':
                    obj['error'] = True
                    obj['note'] = 'Bản ghi không tồn tại'
                
                elif action=='import':
                    serializer = serializer_class(data = obj)
                    obj['record_type'] = 'new'
                    obj['id'] = None
                    if serializer.is_valid()==False:
                        obj['error'] = True
                        obj['note'] = serializer.errors

            else:        
                serializer = serializer_class(thelist[0], data = obj)
                obj['record_type'] = 'existed'
                obj['id'] = thelist[0].id

                if action=='import':
                    if serializer.is_valid()==False:
                        obj['error'] = True
                        obj['note'] = serializer.errors
                
                elif action=='delete':
                    serializer = serializer_class(thelist[0])
                    ele = serializer.data
                    ele['record_type'] = 'existed'
                    ele['index'] = obj['index']
                    obj = ele

                elif action=='approve':
                    serializer = serializer_class(thelist[0])
                    ele = serializer.data
                    ele['index'] = obj['index']
                    ele['record_type'] = 'existed'
                    ele['id'] = thelist[0].id
                    ele['status'] = obj['status']
                    obj = ele

            array.append(obj)

        except Exception as e:
            obj['error'] = True
            obj['note'] = e
            array.append(obj)

    return Response(array)


#=============================================================================
#--- One function for get all data ---
def get_relate_objects(Model, origin_object, id, objects):
    try:
        relate_objects = [obj for obj in objects if obj['rel_model'] == Model]

        level1 = []
        for obj in relate_objects:
            filters = {obj['field']: origin_object}        
            filter_list = obj['model'].objects.filter(**filters)

            found = next(iter([ele for ele in level1 if ele['model'] == obj['model']]), None)
            if found == None:
                level1.append({'model': obj['model'], 'data': list(filter_list)})
            else:
                for ele in filter_list:
                    record = next(iter([o for o in found['data'] if ele.id == o.id]), None)
                    found['data'].append(ele) if record == None else  1==1

        level2 = []
        for relate in relate_objects:
            values = [ele for ele in objects if ele['rel_model'] == relate['model']]

            for obj in values:
                for element in level1:
                    for val  in element['data']:
                        filters = {obj['field']: val}     
                        filter_list = obj['model'].objects.filter(**filters)

                        found = next(iter([ele for ele in level2 if ele['model'] == obj['model']]), None)
                        if found == None:
                            level2.append({'model': obj['model'], 'data': list(filter_list)})
                        else:
                            for ele in filter_list:
                                record = next(iter([o for o in found['data'] if ele.id == o.id]), None)
                                found['data'].append(ele) if record == None else  1==1

        return {'level1': level1, 'level2': level2}
    except:
        return None


#=============================================================================
@api_view(['GET', 'POST'])
def import_data(request, name):
    Model, serializer_class = get_serializer(name)
    if Model == None:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # check param action
    error = False
    return_data = []
    if request.query_params.get('action') != None:
        action = request.query_params['action']
    else:
        Response(status=status.HTTP_400_BAD_REQUEST)

    data = [request.data.dict()] if type(request.data) == QueryDict else request.data
    values = request.query_params['values'] if request.query_params.get('values') != None else None
    values = values if values==None else values.split(',')

    # check action delete
    if action == 'delete':
        objects = []
        for model in apps.get_models():
            for field in model._meta.fields:
                if field.get_internal_type() == 'ForeignKey':
                    objects.append({'model': model, 'field': field.name, 'rel_model': field.related_model})
    
    for obj in data:
        try:
            # find field id
            field_id = next(iter([key for key in obj.keys() if key == 'id']), None)
            if field_id == None:
                serializer = serializer_class(data = obj)
            else:
                # check new record
                element = Model.objects.filter(pk=obj['id']).first()
                if element == None:
                    serializer = serializer_class(data = obj)   # insert
                else:
                    serializer = serializer_class(element, data=obj)    # update
            
            if action=='import':
                if serializer.is_valid():
                    serializer.save()
                    return_data.append(serializer.data if values == None else serializer.data['id'])
                else:
                    obj['error'] = True
                    obj['note'] = serializer.errors
                    error = True
                    
            elif action=='delete':
                try:
                    if element!= None:
                        result = get_relate_objects(Model, element, obj['id'], objects)
                        if len(objects) >0:
                            # delete level 2 first
                            for rs in result['level2']:
                                for record in rs['data']:
                                    record.delete()
                            
                            # then level 1
                            for rs in result['level1']:
                                for record in rs['data']:
                                    record.delete()

                        # level 0
                        element.delete()
                        obj['deleted'] = True
                except:
                    obj['error'] = True
                    obj['note'] = 'Có lỗi xẩy ra. Không thể xóa bản ghi này'
                    error = True
        except:
            obj['error'] = True
            error = True
    
    return_data = return_data if values == None else Model.objects.filter(id__in = return_data).values(*values)
    return Response(data if error == True or action=='delete' else return_data)


#=============================================================================
#--- upload/ ---
upload_folder = "Upload/"

@api_view(['POST'])
def upload_file(request):
    if request.method == 'POST':
        file = request.data['file']
        filename = request.data['name']

        try:
            with open(upload_folder + filename, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            return Response(status.HTTP_200_OK)      

        except IOError as e: # Will only catch IOErrors
                return Response(e)    # Re-raise other IOErrors
        except OSError as e: # Will only catch OSErrors
            return Response(e)


#=============================================================================
#--- getview/ ---
@api_view(['GET'])
def getfile(request, filename):
    import pandas

    try:  
        df = pandas.read_excel(upload_folder + filename, dtype=str,  na_filter=False)
        val = df.to_json(path_or_buf= None, orient='table', force_ascii=False)

        return Response(val, status.HTTP_200_OK)      

    except IOError as e: # Will only catch IOErrors
        return Response(e)    # Re-raise other IOErrors
    except OSError as e: # Will only catch OSErrors
        return Response(e)


#=============================================================================
#--- upload/ ---
@api_view(['POST'])
def upload(request):
    upload_folder = static_folder + '/files/'
    Model = File

    if request.method == 'POST':
        file = request.data['file']
        filename = request.data['name']

        if request.data['type'] == 'image':
            upload_folder = static_folder + '/images/'
            Model = Image

        try:
            with open(upload_folder + filename, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            Model, serializer_class = get_serializer(Model.__name__)
            obj = Model.objects.filter(file=request.data['name']).first()
            if obj == None:
                data = {'user': request.data['user'], 'file': request.data['name'], 'size': request.data['size']}
                serializer = serializer_class(data = data)
                if serializer.is_valid():
                    serializer.save()

            else: 
                obj.size = request.data['size']
                obj.save()
                serializer = serializer_class(obj)

            return Response({'total_rows': 1, 'full_data': True, 'rows': [serializer.data]})
        except:
            Response(status = status.HTTP_400_BAD_REQUEST)
       
    return Response(status = status.HTTP_400_BAD_REQUEST)


#=============================================================================
#--- Check model relationship ---
@api_view(['GET', 'POST'])
def check_model_relation(request, name):
    try:
        Model = apps.get_model('Backend', name)
        objects = []
        for model in apps.get_models():
            for field in model._meta.fields:
                if field.get_internal_type() == 'ForeignKey':
                    objects.append({'model': model, 'field': field.name, 'rel_model': field.related_model})
        relate_objects = [obj for obj in objects if obj['rel_model'] == Model]

        data = {'relation': True if len(relate_objects)>0 else False}
        return Response(data)

    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


#=============================================================================
@api_view(['GET'])
def download(request):
    upload_folder = static_folder + '/files/'
    name = request.query_params['name'] if request.query_params.get('name') != None else None
    type = request.query_params['type'] if request.query_params.get('type') != None else None

    if  name == None or type == None:
        return Response(status = status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        if type == 'video':
            upload_folder = static_folder + '/videos/'
        
        elif type == 'image':
            upload_folder = static_folder + '/images/'
        
        if os.path.exists(upload_folder + name):
            response = FileResponse(open(upload_folder + name, 'rb'))
            return response

    return Response(status = status.HTTP_400_BAD_REQUEST)


#=============================================================================
#--- download data ---

@api_view(['GET'])
def download_file(request, name):
    import time
    val = time.strftime('%Y%m%d%H%M%S')
    file_path = "Download/" + name
    file_type = "application/vnd.ms-access" if name == 'DataEntry.mdb' else 'application/force-download'  

    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type=file_type)
            response['Content-Disposition'] = 'attachment; filename=' + val + '-' + os.path.basename(file_path)
            return response

    return Response(status=status.HTTP_404_NOT_FOUND)


#=============================================================================
@api_view(['GET'])
def get_datafile(request, name):
    upload_folder = "Upload/"
    
    if request.method == 'GET':
        if os.path.exists(upload_folder + name):
            response = FileResponse(open(upload_folder + name, 'rb'))
            return response

    return Response(status = status.HTTP_400_BAD_REQUEST)


#=============================================================================
#--- CHANGE DATA MODEL ---

@api_view(['GET', 'POST'])
def change_data_model(request):
    try:        
        file_path = "Backend/models.py"
        #1. open file
        f = open(file_path, "r")
        contents = f.readlines()
        f.close()

        sqlcmd = []
        data = request.data
        for resp in data:
            report_name = ''
            if resp['report_name'] == 'CDKT':
                report_name = 'BS'+ resp['company_type']

            elif resp['report_name'] == 'KQKD':
                report_name = 'BP'+ resp['company_type']

            elif resp['report_name'] == 'LCTT-TT':
                report_name = 'CFTT'+ resp['company_type']

            elif resp['report_name'] == 'LCTT-GT':
                report_name = 'CFGT'+ resp['company_type']

            elif resp['report_name'] == 'KHKD':
                report_name = 'PLAN'

            elif resp['report_name'] == 'LNUD':
                report_name = 'ESTIMATED'

            #2. find index and insert new line
            searchText = "#" + report_name + "_ADD_NEW_FIELD"
            index = [x for x in range(len(contents)) if searchText in contents[x]]

            if  len(index) == 0 or report_name == '':
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
            value = "    f" + resp['item'] + " = models.FloatField(null=True)\n"
            contents.insert(index[0], value)
            sqlcmd.append('ALTER TABLE ' + report_name + ' ADD COLUMN ' +  'f' + resp['item']  + ' DOUBLE')

        #. open file and write
        f = open(file_path, "w")
        contents = "".join(contents)
        f.write(contents)
        f.close()

        return Response(status=status.HTTP_204_NO_CONTENT)

    except IOError as e: # Will only catch IOErrors
        return Response(e)    # Re-raise other IOErrors
    except OSError as e: # Will only catch OSErrors
        return Response(e)


#=============================================================================
#--- MIGRATE DATA MODEL ---

@api_view(['GET', 'POST'])
def migrate_data_model(request):
    try:

        from django.core.management import call_command
        call_command("makemigrations", interactive=False)
        call_command("migrate", interactive=False)

        return Response(status=status.HTTP_204_NO_CONTENT)

    except IOError as e: # Will only catch IOErrors
        return Response(e)    # Re-raise other IOErrors
    except OSError as e: # Will only catch OSErrors
        return Response(e)


#=============================================================================
#---Task summary---
@api_view(['GET'])
def task_summary(request, filter):
    from psycopg2.extras import RealDictCursor

    try:   
        pg_conn = psycopg2.connect(connection)
        pg_curs = pg_conn.cursor(cursor_factory=RealDictCursor)

        sql = 'select a.status_id, a.count,  round (a.point::DECIMAL, 0)::TEXT as point, b.* \
        from (select status_id, count(1),  sum(CASE WHEN status_id =157 AND date_part(\'year\', c.create_time) = date_part(\'year\', CURRENT_DATE) THEN percentage ELSE 0 END)/100 point \
        from "Task" c join "Account" d on c.recipient_id = d.id and ' + filter  + ' \
        group by status_id) a join "Classification" b on a.status_id = b.id'
        
        pg_curs.execute(sql)
        rows = pg_curs.fetchall()
        return Response({'total_rows': len(rows), 'full_data': True, 'rows': rows})

    except IOError as e: # Will only catch IOErrors
        return Response(e)    # Re-raise other IOErrors
            
    except OSError as e: # Will only catch OSErrors
        return Response(e)    # Re-raise other IOErrors


#=============================================================================
#--- send email task/ ---

@huey.task()
def send_email(subject, content, sendto):
    email = EmailMessage(subject, content, to=[sendto])
    email.send()


#=============================================================================
#--- send email api/ ---

@api_view(['POST'])
def send_email_api(request):
    if request.method == 'POST':
        if request.data.get('subject') == None or request.data.get('content') == None or request.data.get('to') == None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            send_email(request.data.get('subject'), request.data.get('content'), request.data.get('to'))
            return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(status=status.HTTP_400_BAD_REQUEST)


#=============================================================================
#--- Export table ---

def export_table(table, filter_list):
    import jaydebeapi
    db_path = BASE_DIR + "/Download/DataEntry.mdb"
    ucanaccess_jars = [
        BASE_DIR + "/Download/UCanAccess/ucanaccess-5.0.0.jar",
        BASE_DIR + "/Download/UCanAccess/lib/commons-lang3-3.8.1.jar",
        BASE_DIR + "/Download/UCanAccess/lib/commons-logging-1.2.jar",
        BASE_DIR + "/Download/UCanAccess/lib/hsqldb-2.5.0.jar",
        BASE_DIR + "/Download/UCanAccess/lib/jackcess-3.0.1.jar",
    ]
    classpath = ":".join(ucanaccess_jars)
    cnxn = jaydebeapi.connect(
        "net.ucanaccess.jdbc.UcanaccessDriver",
        f"jdbc:ucanaccess://{db_path};newDatabaseVersion=V2010",
        ["", ""],
        classpath
        )
    crsr = cnxn.cursor()

    success = False
    check_list1 = ['BigAutoField', 'AutoField', 'TextField', 'CharField', 'BigIntegerField', 'IntegerField', 'DateTimeField', "DateField", 'BooleanField', 'ForeignKey', 'FloatField']
    check_list2 = ['NUMBER', 'FLOAT', 'MEMO', 'MEMO', 'FLOAT', 'NUMBER', 'DATETIME', 'DATETIME', 'TEXT', 'MEMO', 'FLOAT']
    Model = apps.get_model('Backend', table)
    sql = 'create table ' + table + '('
    ins = 'insert into ' + table + '('
    values = []

    all_fields = Model._meta.get_fields()
    for field in all_fields:
        field_type = field.get_internal_type()
        index = check_list1.index(field_type)
        if (table == 'Task' and field.name.find('_task')>=0) == False:
            sql += field.name + ' ' + check_list2[index] + ','
            ins += field.name + ','

            if field_type == 'ForeignKey':
                if field.related_model.__name__ == 'Classification':
                    values.append(field.name + '__value')

                elif field.related_model.__name__ == 'Account':
                    values.append(field.name + '__name')
                
                elif field.related_model.__name__ == 'Company':
                    values.append(field.name + '__stock_code')

                elif field.related_model.__name__ == 'Task':
                    sql += 'company_id TEXT, year FLOAT, report_period_id TEXT, report_type_id TEXT, assigner_id TEXT, recipient_id TEXT,'
                    ins += 'company_id, year, report_period_id, report_type_id, assigner_id, recipient_id,'
                    arr = [field.name, 'task__company__stock_code', 'task__year', 'task__report_period__value', 'task__report_type__value', 'task__assigner__name', 'task__recipient__name']
                    values = [*values, *arr]
                else:
                    values.append(field.name)

            else:
                values.append(field.name)
    sql = sql[0:len(sql)-1] + ')'
    ins = ins[0:len(ins)-1] + ')'

    #drop table
    try:
        crsr.execute("DROP TABLE " + table)
        cnxn.commit()
    except:
        print('table not existed')

    #create table again
    crsr.execute(sql)
    cnxn.commit()

    #select
    rows = Model.objects.all().values(*values) if filter_list == None else  Model.objects.filter(filter_list).values(*values)
    try:
        for row in rows:
            cmd = ins + ' values('
            for val in values:
                cmd += 'Null,' if row[val]==None or row[val] == '' else ('"' + str(row[val]).replace('"', '') + '",')
            cmd = cmd[0:len(cmd)-1] + ')'
            crsr.execute(cmd)

        success = True
    except:
        success = False
    cnxn.commit()
    crsr.close()
    cnxn.close()
    return success


#=============================================================================
#--- Export data ---
@api_view(['GET'])
def export_table_api(request, table):
    try:
        export_table(table, None)
    
    except OSError as e: 
        return Response(e)  

    return Response(status=status.HTTP_204_NO_CONTENT)


#=============================================================================
#--- Export data ---
def export_data(filter_list):
    import subprocess
    folder = os.path.join(BASE_DIR, "Download")
    subprocess.call(["rm", "-rf", folder + '/DataEntry.mdb'])
    subprocess.call(["cp", "-r", '/home/stackops/DataEntry.mdb', folder])

    obj = Etl_Log()
    obj.type = 'database export'
    obj.etl_date = datetime.now().date()
    obj.start_time = datetime.now()
    check_list1 = ['Account', 'Task', 'Report_Item', 'Company', 'Item_Change']
    check_list2 = ['BS', 'BP', 'CF']
    
    from django.db import connection
    tables = connection.introspection.table_names()
    res = True
    for row in tables:
        if row in check_list1 or row[:2] in check_list2:
            res = export_table(row, filter_list)
            if res == False:
                break;

    obj.end_time = datetime.now()
    obj.status = 1 if res == True else 0
    obj.save()
    return res


#=============================================================================
#--- Export data api ---

@api_view(['GET'])
def export_data_api(request):
    filter = request.query_params['filter'] if request.query_params.get('filter') != None else None
    filter_list = None
    if filter != None:
        filter_list = Q()
        for key, value in ast.literal_eval(filter).items():
            filter_list.add(Q(**{key: value}), Q.AND)

    res = export_data(filter_list)
    if res == True:
        return Response(status=status.HTTP_204_NO_CONTENT)
    else: 
        return Response(status=status.HTTP_400_BAD_REQUEST)    # Re-raise other IOErrors


#=============================================================================
#--- Item Change ---
@api_view(['GET'])
def salary_summary(request, filter):
    import pandas as pd
    from psycopg2.extras import RealDictCursor
    import copy

    try:  
        val = filter.split(",")
        if len(val) == 1:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        fdate = datetime.strptime(val[0], '%Y%m%d')
        tdate = datetime.strptime(val[1], '%Y%m%d')

        pg_conn = psycopg2.connect(connection)
        pg_curs = pg_conn.cursor(cursor_factory=RealDictCursor)
  
        sql = 'select recipient_id, report_name_id, b.type_id, count(a.id) count, \
        sum(CASE WHEN status_id = 157 THEN null ELSE into_money END) expectation, \
        sum(CASE WHEN status_id = 157 THEN into_money ELSE null END) reality, \
        sum(CASE WHEN percentage = null THEN 0 ELSE percentage / 100.00 END) point '
        sql += 'from public."Task" a join public."Company" b on a.company_id = b.id '
        sql += 'where cast(assign_date as date) >= \'' + str(fdate) + '\' and cast(assign_date as date) <= \'' + str(tdate) + '\''
        sql +=  ' group by  recipient_id, report_name_id, b.type_id'

        pg_curs.execute(sql)
        results = pg_curs.fetchall()
        rows = []
        count = 0

        for row in results:
            Model, serializer_class = get_serializer('Account')
            recipient = serializer_class(Account.objects.get(pk=row['recipient_id']))
            Model, serializer_class = get_serializer('Classification')
            report_name = serializer_class(Classification.objects.get(pk=row['report_name_id']))
            type  = serializer_class(Classification.objects.get(pk=row['type_id']))
            count += 1
            row['recipient'] = recipient.data
            row['report_name'] = report_name.data
            row['type'] = type.data
            row['id'] = str(count)
            rows.append(row)

        return Response({'total_rows': len(rows), 'full_data': True, 'rows': rows})

    except IOError as e: # Will only catch IOErrors
        return Response(e)    # Re-raise other IOErrors
    except OSError as e: # Will only catch OSErrors
        return Response(e)


#=============================================================================
#--- Item Change ---
@api_view(['GET'])
def salary_calculation(request, filter):
    import pandas as pd
    from psycopg2.extras import RealDictCursor
    import copy

    try:
        val = filter.split(",")
        if len(val) == 1:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        fdate = datetime.strptime(val[0], '%Y%m%d')
        tdate = datetime.strptime(val[1], '%Y%m%d')

        pg_conn = psycopg2.connect(connection)
        pg_curs = pg_conn.cursor(cursor_factory=RealDictCursor)
  
        sql = 'select recipient_id, count(a.id) count, \
        sum(CASE WHEN status_id = 157 THEN null ELSE into_money END) expectation, \
        sum(CASE WHEN status_id = 157 THEN into_money ELSE null END) reality, \
        sum(CASE WHEN percentage = null THEN 0 ELSE percentage / 100.00 END) point '
        sql += 'from public."Task" a '
        sql += 'where cast(assign_date as date) >= \'' + str(fdate) + '\' and cast(assign_date as date) <= \'' + str(tdate) + '\''
        sql +=  ' group by  recipient_id'

        pg_curs.execute(sql)
        results = pg_curs.fetchall()
        rows = []
        count = 0

        for row in results:
            Model, serializer_class = get_serializer('Account')
            recipient = serializer_class(Account.objects.get(pk=row['recipient_id']))
            count += 1
            row['recipient'] = recipient.data
            row['id'] = str(count)
            rows.append(row)
        return Response({'total_rows': len(rows), 'full_data': True, 'rows': rows})

    except IOError as e: # Will only catch IOErrors
        return Response(e)    # Re-raise other IOErrors
    except OSError as e: # Will only catch OSErrors
        return Response(e)

    
#=============================================================================
@api_view(['GET', 'POST'])
def delete_report(request):
    data = request.data
    for obj in data:
        try:
            Model = apps.get_model('Backend', obj['connName'])
            element = Model.objects.get(task=obj['id'])
            element.delete()

        except Model.DoesNotExist:
            pass

        try:
            Model = apps.get_model('Backend', 'Item_Change')
            filter = {'task' : obj['id']}
            thelist = Model.objects.filter(**filter)
            for element in thelist:
                element.delete()
        
        except Model.DoesNotExist:
            pass

        try:
            Model = apps.get_model('Backend', 'Task')
            element = Model.objects.get(pk=obj['id'])
            element.delete()
            obj['deleted'] = True

        except:
            pass
                
    return Response(data)

    
#=============================================================================
def backup_database():
    import subprocess

    DB_NAME = 'dataentry'  # your db name
    DB_USER = 'postgres' # you db user
    DB_HOST = "localhost"
    DB_PASSWORD = '2018'# your db password
    dump_success = 1

    print ('Backing up %s database ' % (DB_NAME))
    command = f'pg_dump --host={DB_HOST} ' \
                f'--dbname={DB_NAME} ' \
                f'--username={DB_USER} ' \
                f'--no-password ' \
                f'--file=dataentry.bak '
    try:
        proc = subprocess.Popen(command, shell=True, env={
                    'PGPASSWORD': DB_PASSWORD
                    })
        proc.wait()

    except Exception as e:
            dump_success = 0
            print('Exception happened during dump %s' %(e))

    if dump_success:
        print('backup database successfull')


#=============================================================================
@huey.task()
def process_message(data):
    Model, serializer_class = get_serializer('Price_Live')
    live = Price_Live.objects.filter(company__stock_code=data['symbol']).first()
    if live:
        data['company'] = live.company.id
        data['id'] = live.id
        serializer = serializer_class(live, data = data)
    else:
        company = Company.objects.filter(stock_code=data['symbol']).first()
        if company:
            data['company'] = company.id
            serializer = serializer_class(data = data)
        else:
            print('missing company')
    
    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)


#=============================================================================
@api_view(['GET', 'POST'])
def insert_price_live(request):
    data = request.data.dict()
    process_message(data)
    return Response(status=status.HTTP_201_CREATED)