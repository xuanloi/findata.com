# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Backend.models import *
import ast

#=============================================================================
def base(ticker, date, number):
  rows = Stock_Price.objects.filter(company__stock_code=ticker, stock_date__lte=date, task__status=157).order_by('-stock_date').values('id','company','stock_date','f02753')[0:number]
  rows = [rows[i] for i in reversed(range(len(rows)))]
  array = []
  for idx, row in enumerate(rows):
    row['f02753'] = row['f02753']/1000
    row['macd']  = None
    row['signal']  = None
    row['signal']  = None
    row['diff']  = None
    row['idx'] = idx + 1
    current = idx + 1
     
    if current == 1:
      row['ema12'] = row['f02753']
      row['ema26'] = row['f02753']
    else:
      row['ema12'] = row['f02753']*(2/(12+1))+ rows[idx-1]['ema12']*(1-(2/(12+1)))
      row['ema12'] = round(row['ema12'], 2)
      row['ema26'] = row['f02753']*(2/(26+1))+ rows[idx-1]['ema26']*(1-(2/(26+1)))
      row['ema26'] = round(row['ema26'], 2)

    if current>=26:
      row['macd'] = row['ema12'] - row['ema26']
      if current == 26:
        row['signal']  = row['macd']
      else:
        row['signal'] =round(row['macd']*(2/(9+1))+rows[idx-1]['signal']*(1-(2/(9+1))),2)

      row['macd'] = round(row['macd'], 2)
      if current>=34:
        row['diff'] = round(row['signal'] - row['macd'], 2)
    row['f02916'] = row['macd']
    row['f02917'] = row['signal']
    array.append(row)
  return array


#=============================================================================
@api_view(['GET'])
def macd(request):
  filter = request.query_params['filter'] if request.query_params.get('filter') != None else None
  date =  ast.literal_eval(filter)['stock_date']
  rows = []
  array = Stock_Price.objects.filter(stock_date=date, task__status=157).values('company__stock_code')
  for row  in array:
    arr = base(row['company__stock_code'], date, 34)
    rows.append(arr[len(arr) - 1])
  return Response({'total_rows': len(rows), 'full_data': True, 'rows': rows})
