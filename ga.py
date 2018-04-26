import HelloAnalytics as ha
import argparse
from apiclient.discovery import build
import httplib2
from oauth2client import client, file, tools

VIEW_ID = '71224481'

analytics = ha.initialize_analyticsreporting()
# response  = ha.get_report(analytics)
# ha.print_response(response)

# response = analytics.reports().batchGet(
  # body={
    # 'reportRequests': [
    # {
      # 'viewId': VIEW_ID,
      # 'dateRanges': [{'startDate': '10daysAgo', 'endDate': 'yesterday'}],
      # 'metrics': [{'expression': 'ga:pageviews'}]
    # }]
  # }
# ).execute()

response = analytics.reports().batchGet(
  body={
    'reportRequests': [
    {
      'viewId': VIEW_ID,
      'dateRanges': [
          # {'startDate': '10daysAgo','endDate':'yesterday'},
          {'startDate': '2014-11-01', 'endDate': '2018-04-26'}
          ],
      # 'metrics': [{'expression': 'ga:pageviews/ga:sessions','alias':'pv per session'}]
      'metrics': [
          {'expression': 'ga:pageviews'},
          {'expression': 'ga:sessions'}
          ],
      'metricFilterClauses':[{
          'filters':[{
              'metricName': 'ga:sessions',
              'operator': 'GREATER_THAN',
              'comparisonValue': '0'
              }]
          }],
      'orderBys':[
          {'fieldName':'ga:sessions','sortOrder':'ASCENDING'},
          {'fieldName':'ga:pageviews','sortOrder':'ASCENDING'}
          ],
      'dimensions':[
          {'name':'ga:country'},
          # {'name':'ga:sessionCount','histogramBuckets':['1','10','100','200','400']},
          {'name':'ga:pageTitle'}
          ],
      'dimensionFilterClauses':[
          {
              'filters':[
                  {
                      'dimensionName':'ga:country',
                      'operator':'EXACT',
                      'expressions':['Switzerland']
                      }
                  ]
              }
          ]
    }]
  }
).execute()

n=0
for report in response.get('reports', []):
    print('n = %d'%(n))
    n += 1
    columnHeader = report.get('columnHeader', {})
    dimensionHeaders = columnHeader.get('dimensions', [])
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
    rows = report.get('data', {}).get('rows', [])

    for row in rows:
      print '-------------------------------------------'
      dimensions = row.get('dimensions', [])
      dateRangeValues = row.get('metrics', [])

      for header, dimension in zip(dimensionHeaders, dimensions):
        print header + ': ' + dimension

      for i, values in enumerate(dateRangeValues):
        # print 'Date range (' + str(i) + ')'
        for metricHeader, value in zip(metricHeaders, values.get('values')):
          print metricHeader.get('name') + ': ' + value


        
