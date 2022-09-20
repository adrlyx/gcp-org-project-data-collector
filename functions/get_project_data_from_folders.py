from functions.get_billing_info import get_billing_info
from functions.get_metrics import get_last_weeks_api_request_count
from functions.get_last_month_default_log_bucket_bytes import get_last_month_default_log_bucket_bytes
from models.GcpProject import GcpProject
from tqdm import tqdm

def get_project_data_from_folders(
    all_folders: list,
    bar_format: str,
    gcp_discovery_cloudresourcemanager: object,
    gcp_discovery_billing_account: object, 
    gcp_discovery_monitoring: object,
    logger: object,
    ) -> list:
    """
    This function takes a list of folders, a progress bar format, and the GCP discovery services for
    Cloud Resource Manager, Billing, and Monitoring, and returns a list of lists containing the data for
    each project
    
    :param all_folders: list
    :type all_folders: list
    :param bar_format: str
    :type bar_format: str
    :param gcp_discovery_cloudresourcemanager: This is the object that contains the API call to get the
    list of projects
    :type gcp_discovery_cloudresourcemanager: object
    :param gcp_discovery_billing_account: object
    :type gcp_discovery_billing_account: object
    :param gcp_discovery_monitoring: This is the monitoring object that we created earlier
    :type gcp_discovery_monitoring: object
    :param logger: This is the logger object that we created earlier
    :type logger: object
    :return: A list of lists.
    """

    table_data = []

    for folder in tqdm(all_folders, bar_format=bar_format, desc="Getting data for projects", position=0, leave=True):
        request = gcp_discovery_cloudresourcemanager.projects().list(parent=folder.folder_name)
        response = request.execute()

        if 'projects' in response.keys():
            for project_info in response['projects']:
                project = GcpProject(project_info['name'], project_info['projectId'], project_info['displayName'])

                if 'labels' in project_info.keys():
                    project.set_labels(project_info['labels'])

                request = gcp_discovery_cloudresourcemanager.projects().getIamPolicy(resource=project.project_name)
                response = request.execute()

                if 'bindings' in response.keys():
                    for binding_one in response['bindings']:
                        for members in binding_one['members']:
                            if members.startswith('user'):
                                project.set_members(members)

                project_billing_info = get_billing_info(project, gcp_discovery_billing_account, logger)

                GcpProject.set_billing_account(project, project_billing_info['billingEnabled'])
                GcpProject.set_metrics_api_request_count(project, get_last_weeks_api_request_count(project.project_name, gcp_discovery_monitoring))
                GcpProject.set_log_bucket_kilobytes(project, get_last_month_default_log_bucket_bytes(project, gcp_discovery_monitoring, logger))

                if project.members == "N/A":
                    table_data.append([
                        folder.folder_display_name,
                        folder.folder_name,
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
                        folder.folder_display_name,
                        folder.folder_name,
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