from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Backend.models import *
from django.db.models import Sum, Count, F, Value
from django.db.models import Q
import ast

def get_prev_period(current, pre, year):
    period = current
    current_period = Classification.objects.get(pk=current)
    if current_period.code == '5': #year
        year = year - pre
    else:
        code = int(current_period.code) - pre
        i = 0
        while code <=0:
            i += 1
            code = code + 4
        
        year = year -  i
        period = Classification.objects.filter(category='list', classify='report-period', code=code).first()
        period = None if period == None else period.id
    
    return year, period
    

#=============================================================================
def prepare_calculation(element):
    formula = element.formula; chars = "(+-*/)"
    for c in chars:
        formula = formula.replace(c, '$')
    
    #get item, model and serializer
    keyword = []; period_list = []; item_list = []
    chars = ['CDKT','KQKD', 'LCTT-TT','LCTT-GT']; mapping = ['BS','BP','CFTT','CFGT']
    items = []; ele = {}
   
    for text in list(filter(None, formula.split('$'))):
        strlist = text.split('pre')
        item = Report_Item.objects.filter(item = strlist[0]).first()

        if item != None:
            found = next(iter([o for o in items if o == item.item]), None)
            items.append(item.item) if found == None else False
            index = chars.index(item.report_name)
            name = mapping[index] + item.company_type
            ele[('f' if len(strlist)==1 else 'p') + text] = Sum(name.lower() + '_task__' + 'f' + item.item)
            item_list.append(item)
            keyword.append(text)
            period_list.append(0 if len(strlist)==1 else int(strlist[1]))

    return {'item': element.item, 'formula': element.formula, 'keyword': keyword, 'items': item_list, 'periods': period_list, 'filter': ele}


#=============================================================================
@api_view(['GET'])
def get_fin_item(request):  
    item = request.query_params.get('item') if request.query_params.get('item') != None else None
    year = request.query_params.get('year') if request.query_params.get('year') != None else None
    period = request.query_params.get('period') if request.query_params.get('period') != None else None
    company = request.query_params.get('company') if request.query_params.get('company') != None else None
    type = request.query_params.get('type') if request.query_params.get('type') != None else None
    values = request.query_params.get('values') if request.query_params.get('values') != None else None
    fields = "company,year,report_period,report_period__code,report_type,report_type__code"
    values = fields.split(',') if values == None else (fields + ',' + values).split(',')

    if item == None or year == None or period == None:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    chars = ['CDKT','KQKD', 'LCTT-TT','LCTT-GT']; mapping = ['BS','BP','CFTT','CFGT']
    years = [int(year)]; periods = [int(period)]; items = []; condition = {}; types = []
    
    inlist = [] if type == None else [type]
    if type == None:
        rows = Classification.objects.filter(category='list', classify='report-type') \
        .exclude(code__in = ['CTM-KT','CTM-SX','CTM-CKT']).values('id')
        [inlist.append(row['id']) for row in rows]
            
    for text in item.split(','):
        ele = Report_Item.objects.filter(item=text).first()
        found = next((x for x in types if x == ele.company_type), None)
        types.append(ele.company_type) if found == None else False

        if ele.report_name == 'CSTC':
            found = prepare_calculation(ele)

            for val in found['periods']:
                if val>0:
                    prev_year, prev_period = get_prev_period(int(period), val, int(year))
                    [years.append(prev_year) for y in years if y != prev_year]
                    [periods.append(prev_period) for p in periods if p != prev_period]

            for key in found['filter']:
                condition[key] = found['filter'][key]
            items.append(found)
        else:       
            index = chars.index(ele.report_name)
            name = mapping[index] + ele.company_type
            condition['f' + text] = Sum(name.lower() + '_task__' + 'f' + text)

    obj = {'year': year, 'report_period': period, 'report_type__in': inlist}
    if company == None:
        obj['company__type__code__in'] = types
    else:
        obj['company__in'] = company.split(',')
    
    rows = Task.objects.filter(**obj) \
        .values(*values) \
        .annotate(**condition).order_by("report_type")

    seen = set()
    unique = [seen.add(row['company']) or row for row in rows if row['company'] not in seen]
    for row in unique:
        for ele in items:
            formula = ele['formula']
            for text in ele['keyword']:
                code = 'f' if text.find('pre') == -1 else 'p'
                formula = formula.replace(text, '0' if row[code + text]==None else str(row[code + text]), 1)
            try:
                row['f' + ele['item']] = eval(formula)
            except:
                False

    return Response({'total_rows': len(unique), 'full_data': True, 'rows': unique})


#=============================================================================
@api_view(['GET'])
def get_fin_item_v1(request):  
    item = request.query_params.get('item') if request.query_params.get('item') != None else None
    year = request.query_params.get('year') if request.query_params.get('year') != None else None
    period = request.query_params.get('period') if request.query_params.get('period') != None else None
    type = request.query_params.get('type') if request.query_params.get('type') != None else None
    values = request.query_params.get('values') if request.query_params.get('values') != None else None
    fields = "company,year,report_period,report_period__code,report_type,report_type__code"
    values = fields.split(',') if values == None else (fields + ',' + values).split(',')
    filter = request.query_params['filter'] if request.query_params.get('filter') != None else None
    summary = request.query_params['summary'] if request.query_params.get('summary') != None else None
    exclude = request.query_params['exclude'] if request.query_params.get('exclude') != None else None

    if item == None or year == None or period == None:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    chars = ['CDKT','KQKD', 'LCTT-TT','LCTT-GT']; mapping = ['BS','BP','CFTT','CFGT']
    years = [int(year)]; periods = [int(period)]; items = []; condition = {}; types = []
    
    inlist = [] if type == None else [type]
    if type == None:
        rows = Classification.objects.filter(category='list', classify='report-type') \
        .exclude(code__in = ['CTM-KT','CTM-SX','CTM-CKT']).values('id')
        [inlist.append(row['id']) for row in rows]
            
    for text in item.split(','):
        ele = Report_Item.objects.filter(item=text).first()
        found = next((x for x in types if x == ele.company_type), None)
        types.append(ele.company_type) if found == None else False

        if ele.report_name == 'CSTC':
            found = prepare_calculation(ele)

            for val in found['periods']:
                if val>0:
                    prev_year, prev_period = get_prev_period(int(period), val, int(year))
                    [years.append(prev_year) for y in years if y != prev_year]
                    [periods.append(prev_period) for p in periods if p != prev_period]

            for key in found['filter']:
                condition[key] = found['filter'][key]
            items.append(found)
        else:       
            index = chars.index(ele.report_name)
            name = mapping[index] + ele.company_type
            condition['f' + text] = Sum(name.lower() + '_task__' + 'f' + text)

    filter_list = Q()
    if filter != None:
        for key, value in ast.literal_eval(filter).items():
            filter_list.add(Q(**{key: value}), Q.AND)
    else:
       filter_list.add(Q(**{'company__type__code__in': types}), Q.AND) 
    filter_list.add(Q(**{'year': year}), Q.AND)
    filter_list.add(Q(**{'report_period': period}), Q.AND)
    filter_list.add(Q(**{'report_type__in': inlist}), Q.AND)
    
    rows = Task.objects.filter(filter_list) \
        .values(*values) \
        .annotate(**condition).order_by("report_type")

    if exclude != None:
        exclude_list = Q()
        for key, value in ast.literal_eval(exclude).items():
            exclude_list.add(Q(**{key: value}), Q.AND)
        rows = rows.exclude(exclude_list)

    seen = set()
    unique = [seen.add(row['company']) or row for row in rows if row['company'] not in seen]
    for row in unique:
        for ele in items:
            formula = ele['formula']
            for text in ele['keyword']:
                code = 'f' if text.find('pre') == -1 else 'p'
                formula = formula.replace(text, '0' if row[code + text]==None else str(row[code + text]), 1)
            try:
                row['f' + ele['item']] = eval(formula)
            except:
                False

    if summary == 'count':
        unique = {'count': len(unique)}
    return Response({'total_rows': len(unique), 'full_data': True, 'rows': unique})


#=============================================================================
def analyze_formula(main_item, main_formula):
    formula = main_formula; chars = "(+-*/)"
    for c in chars:
        formula = formula.replace(c, '$')

    #get item, model and serializer
    keyword = []; period_list = []; item_list = []
    chars = ['GIA','TKGIA', 'TKLENH','DTNNLENH', 'DTNNTT']
    mapping = [Price_Live, Stock_Price, Stock_Order, Foreign_Order, Foreign_Deal]
    items = []; models = []; keys = []; condition = []

    for idx, text in enumerate(list(filter(None, formula.split('$')))):
        strlist = text.split('sum')
        item = Report_Item.objects.filter(item = strlist[0]).first()

        if item != None:
            found = next(iter([o for o in items if o == item.item]), None)
            items.append(item.item) if  found == None else False
            index = chars.index(item.report_name)
            models.append(mapping[index])
            condition.append({main_item + text + '|' + str(idx): Sum('f' + item.item)})
            keys.append(main_item + text + '|' + str(idx))
            item_list.append(item)
            keyword.append(text)
            period_list.append(0 if len(strlist)==1 else int(strlist[1]))

    return {'item': main_item, 'formula': main_formula, 'keyword': keyword, 'items': item_list, 'periods': period_list, 'models': models, 'keys': keys, 'filter': condition}


#=============================================================================
@api_view(['GET'])
def get_ta_item(request):  
    item = request.query_params.get('item') if request.query_params.get('item') != None else None
    items = []; matches = []; sum_keys = []

    for text in item.split(','):
        ele = Report_Item.objects.filter(item=text).first()
        if ele.formula == None:
            break
        
        found = analyze_formula(text, ele.formula)
        sum_keys = sum_keys + found['keys']
        items.append(found)

        for idx, val in enumerate(found['periods']):
            Model = found['models'][idx]; dates = []
            if val>0:
                arr = Task_Stock.objects.filter(status=157).values('stock_date').distinct('stock_date').order_by('-stock_date')[:val]
                [dates.append(date['stock_date']) for date in arr]

                query = Model.objects.filter(stock_date__in = dates) \
                .values("company") \
                .annotate(**found['filter'][idx])
                matches.append(query)
            else:
                query = Model.objects \
                .values("company") \
                .annotate(**found['filter'][idx])
                matches.append(query)

    # merge query set           
    from itertools import chain
    query = list(chain(*matches))

    #group by
    from collections import defaultdict
    from operator import itemgetter
    d = defaultdict(lambda: defaultdict(int))
    group_keys = ['company', 'company']
    seen = set()
    sum_keys = [seen.add(val) or val for val in sum_keys if val not in seen]

    for item in query:
        for key in sum_keys:
            d[itemgetter(*group_keys)(item)][key] += (item[key] if key in item else 0)
    rows = [{**dict(zip(group_keys, k)), **v} for k, v in d.items()]

    #calculate formula
    for row in rows:
        for ele in items:
            formula = ele['formula']
            for idx, text in enumerate(ele['keyword']):
                formula = formula.replace(text, '0' if row[ele['keys'][idx]]==None else str(row[ele['keys'][idx]]), 1)
            try:
                row['f' + ele['item']] = eval(formula)
            except:
                False

    return Response({'total_rows': len(rows), 'full_data': True, 'rows': rows})


#=============================================================================
@api_view(['POST'])
def screener_performance(request):
    stocks = request.data['list']
    statistic = request.data['statistic']
    _summary = request.data['summary']
   
    dates = Task_Stock.objects.filter(stock_date__gte=request.data['date'], status=157).distinct('stock_date').order_by('stock_date').values('stock_date')
    arr = []; j = 1; start_date = None
    for i, val in enumerate(dates):
        obj = {'date': val['stock_date'].strftime('%Y-%m-%d'), 'short': val['stock_date'].strftime('%d/%m')}
        if i == 0:
            start_date = obj['date']
            obj['label'] = 'START'
        elif i >=1 and i <=5:
            obj['label'] = str(i) + 'D'
        elif i < len(dates) - 1:
            if statistic == 'weekly':
                if i % 5 == 0:
                    j = j + 1
                    obj['label'] = str(j) + 'W' 
                else:
                    obj['label'] = None
            else:
                obj['label'] = str(i) + 'D'   
        elif i == len(dates) - 1:
            obj['label'] = 'END'
        arr.append(obj) if obj['label'] != None else False

    result = []
    for stock in stocks:
        obj = {'stock_code': stock}
        for row in arr:
            date = row['date']
            row = Stock_Price.objects.filter(company__stock_code=stock, stock_date=date).values('f02751').first()
            if row == None:
                obj[date] = None
            else:
                if _summary == 'detail':
                    obj[date] = row['f02751'] if date == start_date else str(round((row['f02751'] - obj[start_date])*100/obj[start_date], 2)) + '%'
                else:
                    obj[date] = row['f02751'] if date == start_date else round((row['f02751'] - obj[start_date])*100/obj[start_date], 2)
        result.append(obj)
    if _summary == 'detail':
        return Response({'total_rows': len(result), 'full_data': True, 'rows': {'data': result, 'dates': arr}})
    
    summary = []
    for i, val in enumerate(arr):
        if i > 0:
            overall = 0; adv1 = 0; adv2 = 0; dec1 = 0; dec2 = 0; unchange = 0
            date = val['date']
            for row in result:
                value = 0 if row[date] == None else row[date]
                overall += value
                adv1 += 1 if value >0 else False
                adv2 += value if value > 0 else  False
                dec1 += 1 if value <0 else False
                dec2 += value if value <0 else False
                unchange += 1 if value == 0 else False
            
            obj = {'item': val['label'], 
                'overall': None if overall == 0 else str(round(overall,2)) + '%',
                '#adv': None if adv1 == 0 else adv1,
                '%adv': None if adv2 == 0 else str(round(adv2,2)) + '%',
                '#dec': None if dec1 == 0 else dec1,
                '%dec': None if dec2 == 0 else str(round(dec2,2)) + '%',
                'unchange': None if unchange == 0 else unchange,
            }
            summary.append(obj)

    return Response({'total_rows': len(summary), 'full_data': True, 'rows': summary})


#=============================================================================
def get_value_priority(item, year, period, company, type):  
    if item == None or year == None or period == None:
        return None

    chars = ['CDKT','KQKD', 'LCTT-TT','LCTT-GT']; mapping = ['BS','BP','CFTT','CFGT']
    #years =  [int(year)]; periods = [int(period)]; items = []; condition = {}; types = []
    years =  year.split(','); periods = period.split(','); items = []; condition = {}; types = []
    
    inlist = [] if type == None else [type]
    if type == None:
        rows = Classification.objects.filter(category='list', classify='report-type') \
        .exclude(code__in = ['CTM-KT','CTM-SX','CTM-CKT']).values('id')
        [inlist.append(row['id']) for row in rows]
            
    for text in item.split(','):
        ele = Report_Item.objects.filter(item=text).first()
        found = next((x for x in types if x == ele.company_type), None)
        types.append(ele.company_type) if found == None else False

        if ele.report_name == 'CSTC':
            found = prepare_calculation(ele)

            for val in found['periods']:
                if val>0:
                    prev_year, prev_period = get_prev_period(int(period), val, int(year))
                    [years.append(prev_year) for y in years if y != prev_year]
                    [periods.append(prev_period) for p in periods if p != prev_period]

            for key in found['filter']:
                condition[key] = found['filter'][key]
            items.append(found)
        else:       
            index = chars.index(ele.report_name)
            name = mapping[index] + ele.company_type
            condition['f' + text] = Sum(name.lower() + '_task__' + 'f' + text)

    #obj = {'year': year, 'report_period': period, 'report_type__in': inlist}
    obj = {'year__in': years, 'report_period__in': periods, 'report_type__in': inlist}
    if company == None:
        obj['company__type__code__in'] = types
    else:
        obj['company__in'] = company.split(',')
    
    rows = Task.objects.filter(**obj) \
        .values("company", "year", "report_period", "report_period__code", "report_type", "report_type__code") \
        .annotate(**condition).order_by("report_type")

    seen = set()
    unique = [seen.add(row['company']) or row for row in rows if row['company'] not in seen]
    for row in unique:
        for ele in items:
            formula = ele['formula']
            for text in ele['keyword']:
                code = 'f' if text.find('pre') == -1 else 'p'
                formula = formula.replace(text, '0' if row[code + text]==None else str(row[code + text]), 1)
            try:
                row['f' + ele['item']] = eval(formula)
            except:
                row['f' + ele['item']] = None

    return unique


#=============================================================================
@api_view(['GET'])
def valuation(request):
    def get_market(o):
        if o['company__listed_on'] == None:
            return None
        else:
            return 'hose' if o['company__listed_on'].lower()=='hsx' else o['company__listed_on'].lower()

    import numpy as np
    dates = Stock_Price.objects.filter(task__status=157).values('stock_date').distinct('stock_date')
    industries = Stock_Price.objects.filter(task__status=157).values('company__industry').distinct('company__industry')
    
    prices = Stock_Price.objects.filter(task__status=157) \
        .values('id', 'stock_date', 'stock_date__year','company','company__stock_code','company__name','company__industry', 'company__type__code', 'company__listed_on','f02751', 'f02765') \
        .order_by('stock_date', 'company')

    year = None
    arr = None
    items = ['02898', '02900', '00107', '00153', '00104', '02958', '02959', '00495', '00555', '00493', '02961', '02962', '01638', '01739', '01635', '02964', '02965', '00967', '01082', '00965']
    types = ['SX', 'NH', 'CK', 'BH']
    markets = ['hose', 'hnx', 'upcom', 'otc']
    
    for obj in prices:
        if year != obj['stock_date__year']:
            year = obj['stock_date__year']
            arr = get_value_priority(",".join(items), str(year-1), '146', None, None)
           
        arr1 = [o for o in arr if o['company'] == obj['company']]
        ele = None if len(arr1)==0 else arr1[0]
        index = types.index(obj['company__type__code'])

        if ele != None:
            obj['eps'] = ele['f' + items[index*5]] #ele['f02898']
            obj['bv'] =  ele['f' + items[index*5 + 1]]   #ele['f02900']
            obj['pe'] = None if obj['eps'] == None else obj['f02751'] / obj['eps']
            obj['pb'] = None if obj['bv'] == None else obj['f02751'] / obj['bv']
            obj['number_share'] = None if ele['f' + items[index*5 + 2]] == None else ele['f' + items[index*5 + 2]] / 10000
            obj['lnst'] = ele['f' + items[index*5 + 3]]
            obj['vcsh'] = ele['f' + items[index*5 + 4]]
        else:
            obj['eps'] = None
            obj['bv'] = None
            obj['pe'] = None
            obj['pb'] = None
            obj['number_share'] = None
            obj['lnst'] = None
            obj['vcsh'] = None

    for date in dates:
        arr = [o for o in prices if date['stock_date'] == o['stock_date'] \
            and (0 if o['pe']==None else o['pe']) >0 \
            and (0 if o['number_share']==None else o['number_share']) >0 \
            and (0 if o['pb']==None else o['pb']) >0]

        for market  in markets:
            arrm = [o for o in arr if market==get_market(o)]
            sum_vhtt = sum([o['f02765'] for o in arrm])
            sum_lnst = sum([o['lnst'] for o in arrm])
            date['pem' + market] = None if sum_lnst==0 else sum_vhtt / sum_lnst
            sum_vcsh = sum([o['vcsh'] for o in arrm])            
            date['pbm' + market] = None if sum_vcsh==0 else sum_vhtt / sum_vcsh

        for industry in industries:
            arr1 = [o for o in arr if o['company__industry'] == industry['company__industry']]
            sum_vhtt = sum([o['f02765'] for o in arr1])
            sum_lnst = sum([o['lnst'] for o in arr1])
            date[str(industry['company__industry'])] = None if sum_lnst==0 else sum_vhtt / sum_lnst
            sum_vcsh = sum([o['vcsh'] for o in arr1])            
            date[str(industry['company__industry']) + '_pb'] = None if sum_vcsh==0 else sum_vhtt / sum_vcsh

    count = 0
    batch = []
    for obj in prices:
        market = get_market(obj)
        ele = [o for o in dates if o['stock_date'] == obj['stock_date']][0]
        row = Stock_Price.objects.get(pk=obj['id'])
        row.f02966 = obj['eps']
        row.f02967 = obj['bv']
        row.f02968 = obj['pe']
        row.f02969 = obj['pb']
        row.f02978 = obj['lnst']
        row.f02979 = obj['vcsh']

        row.f02970 = ele[str(obj['company__industry'])]
        row.f02971 = None if market==None else ele['pem' + market]
        row.f02974 = None if obj['eps']==None or row.f02970==None  else obj['eps']*row.f02970
        row.f02975 = None if obj['eps']==None or row.f02971==None else obj['eps']*row.f02971
        
        row.f02972 = ele[str(obj['company__industry']) + '_pb']
        row.f02973 = None if market==None else ele['pbm' + market]
        row.f02976 = None if obj['bv']==None or row.f02972==None else obj['bv']*row.f02972
        row.f02977 = None if obj['bv']==None or row.f02973==None else obj['bv']*row.f02973
        
        count += 1
        batch.append(row)
        if count % 1000 == 0:
            Stock_Price.objects.bulk_update(batch, ['f02966', 'f02967', 'f02968', 'f02969', 'f02970', 'f02971', 'f02972', 'f02973', 'f02974', 'f02975', 'f02976', 'f02977', 'f02978', 'f02979'])
            batch = []
            print(count)
        elif count == len(prices):
            Stock_Price.objects.bulk_update(batch, ['f02966', 'f02967', 'f02968', 'f02969', 'f02970', 'f02971', 'f02972', 'f02973', 'f02974', 'f02975', 'f02976', 'f02977', 'f02978', 'f02979'])
            print(count)
        
    return Response(status=status.HTTP_204_NO_CONTENT)