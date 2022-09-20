from datetime import date, datetime


def get_last_month_default_log_bucket_bytes(project_name: object, gcp_discovery_monitoring: object, logger: object) -> dict:

    now = datetime.now()
    today = date.today()
    time_string = now.strftime("%H:%M:%S")

    end_time = str(today) + 'T' + str(time_string) + 'Z'

    data = {
        "name": project_name.project_name,
        "filter": "resource.type=\"global\" AND metric.type=\"logging.googleapis.com/billing/log_bucket_bytes_ingested\" AND metric.label.log_bucket_id=\"_Default\" AND metric.label.log_bucket_location=\"global\"",
        "interval_endTime": end_time,
        "aggregation_alignmentPeriod" : "2629743s",
        "aggregation_crossSeriesReducer": "REDUCE_NONE",
        "aggregation_groupByFields": [
            "resource.label.\"project_id\""
        ],
        "aggregation_perSeriesAligner": "ALIGN_SUM",
    }

    try:
        request = gcp_discovery_monitoring.projects().timeSeries().list(**data)
        response = request.execute()
    except KeyError:
        logger.error('Something wrong when getting billing info')
        exit()


    total_log_bucket_bytes = 0
    if 'timeSeries' in response.keys():
      result_list = response['timeSeries']

      for metric in result_list:
        if metric['metric']['labels']['resource_type'] == 'project':
          continue
        else:
          total_log_bucket_bytes = total_log_bucket_bytes + int(metric['points'][0]['value']['int64Value'])

    total_log_bucket_kilbytes = round(total_log_bucket_bytes/1024)

    return str(total_log_bucket_kilbytes) + "KiB"