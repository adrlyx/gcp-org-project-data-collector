from datetime import datetime
from datetime import date, timedelta

def get_last_weeks_api_request_count(project_name: str, discovery_monitoring: object) -> int:
    """
    > This function takes a project name and a discovery monitoring object as input and
    returns the total number of API requests made to the project over the last two weeks
    
    :param project_name: The name of the project you want to get the API request count for
    :param discovery_monitoring: The discovery object for the monitoring API
    :return: The number of API requests made in the last two weeks.
    """
    now = datetime.now()
    today = date.today()
    two_week_ago = date.today() - timedelta(days=14)
    time_string = now.strftime("%H:%M:%S")

    end_time = str(today) + 'T' + str(time_string) + 'Z'
    start_time = str(two_week_ago) + 'T' + str(time_string) + 'Z'

    data = {
        "name": project_name,
        "filter": "metric.type = \"serviceruntime.googleapis.com/api/request_count\"",
        "interval_endTime": end_time,
        "aggregation_alignmentPeriod" : "86400s",
        "aggregation_crossSeriesReducer": "REDUCE_SUM",
        "aggregation_groupByFields": [
            "resource.label.\"project_id\""
        ],
        "aggregation_perSeriesAligner": "ALIGN_SUM",
        "interval_startTime": start_time
    }

    request = discovery_monitoring.projects().timeSeries().list(**data)
    response = request.execute()

    api_request_count = 0

    if 'timeSeries' in response.keys():
        result_list = response['timeSeries'][0]['points']
        for interval in result_list:
            requests = interval['value']['int64Value']
            api_request_count = ( int(requests) + api_request_count )

    return api_request_count