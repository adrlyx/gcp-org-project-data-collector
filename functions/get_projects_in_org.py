from models.GcpProject import GcpProject
from functions.get_billing_info import get_billing_info
from functions.get_metrics import get_last_weeks_api_request_count
from functions.get_last_month_default_log_bucket_bytes import get_last_month_default_log_bucket_bytes
from tqdm import tqdm


def get_projects_in_org(
    org: str,
    bar_format: str,
    logger: object,
    credentials: object,
    gcp_discovery_cloudresourcemanager: object,
    gcp_discovery_billing_account: object,
    gcp_discovery_monitoring: object,
    ) -> list:
    """
    This function takes in an organization, a progress bar format, a logger, credentials, and two GCP
    discovery objects, and returns a list of lists containing information about the projects in the
    organization
    
    :param org: The organization ID
    :param bar_format: This is the progress bar format
    :param logger: This is the logger object that we created earlier
    :param credentials: The credentials object that you created in the previous step
    :param gcp_discovery_cloudresourcemanager: The Cloud Resource Manager API object
    :param gcp_discovery_billing_account: The billing account discovery service
    :param gcp_discovery_monitoring: The monitoring API object
    :return: A list of lists.
    """
    table_data = []

    request = gcp_discovery_cloudresourcemanager.projects().list(parent=org, pageSize=50)
    response = request.execute()

    response_all = {
        'projects': [] 
    }

    for project in response['projects']:
        response_all['projects'].append(project)

    try:
        nextPageToken = response['nextPageToken']
    except KeyError:
        nextPageToken = None
    except TypeError:
        nextPageToken = None

    while nextPageToken!=None:
        try:
            request = gcp_discovery_cloudresourcemanager.projects().list(
                parent=org,
                pageSize=50,
                pageToken=nextPageToken
            )
            response = request.execute()
            for project in response['projects']:
                response_all['projects'].append(project)
            nextPageToken = response['nextPageToken']
        except KeyError:
            break

    for project_info in tqdm(response_all['projects'], bar_format=bar_format, desc ="Getting projects from org  ", position=0, leave=True):
        project = GcpProject(
            project_info['name'],
            project_info['projectId'],
            project_info['displayName']
            )

        project_billing_info = get_billing_info(
            project,
            gcp_discovery_billing_account,
            logger
            )

        GcpProject.set_billing_account(
            project,
            project_billing_info['billingEnabled']
            )

        GcpProject.set_metrics_api_request_count(
            project,
            get_last_weeks_api_request_count(
                project.project_name,
                gcp_discovery_monitoring
                )
            )

        GcpProject.set_log_bucket_kilobytes(
            project,
            get_last_month_default_log_bucket_bytes(
                project,
                gcp_discovery_monitoring
            )
        )

        if 'labels' in project_info.keys():
            project.set_labels(project_info['labels'])

        request = gcp_discovery_cloudresourcemanager.projects().getIamPolicy(
            resource=project.project_name)
        response = request.execute()

        if 'bindings' in response.keys():
            for binding_one in response['bindings']:
                for members in binding_one['members']:
                    if members.startswith('user'):
                        project.set_members(members)

        if project.members == "N/A":
            table_data.append([
                "No folder",
                org,
                project.project_display_name,
                project.project_name,
                project.project_id,
                project.members,
                project.project_labels,
                project.billing_enabled,
                project.request_count,
                project.log_kilobytes
            ])
        else:
            table_data.append([
                "No folder",
                org,
                project.project_display_name,
                project.project_name,
                project.project_id,
                project.members[0],
                project.project_labels,
                project.billing_enabled,
                project.request_count,
                project.log_kilobytes
            ])

    return table_data