from google.auth import default
from oauth2client.client import GoogleCredentials
from helpers.Logger import Logger
from helpers.TableFormat import TableFormat
from models.GcpDiscovery import GcpDiscovery
from models.BaseConfig import BaseConfig
from functions.get_top_org_folders_from_gcp import get_top_org_folders_from_gcp
from functions.get_all_folders_from_gcp import get_all_folders_from_gcp
from functions.get_project_data_from_folders import get_project_data_from_folders
from functions.get_projects_in_org import get_projects_in_org


if __name__ == '__main__':
    logger = Logger.log()
    bar_format='{l_bar}{bar:40}{r_bar}{bar:-10b}'

    # Init BaseConfig
    base_config = BaseConfig()

    # GCP Credentials
    credentials, project_id = default()
    credentials = GoogleCredentials.get_application_default()

    # Init GCP Discovery
    gcp_discovery = GcpDiscovery(credentials)

    # Init Table
    table = TableFormat()

    # Init empty variables
    all_folder_obj = []
    all_folders = []
    temp_folders = []
    org_top_folders = []

    logger.info("Start")
    # Get all top org folders from GCP
    response_top_folders = get_top_org_folders_from_gcp(
        base_config.organization,
        gcp_discovery.cloudresourcemanager
    )

    # Get all folders from GCP
    all_gcp_folders = get_all_folders_from_gcp(
        response_top_folders,
        all_folder_obj,
        all_folders,
        temp_folders,
        org_top_folders,
        gcp_discovery.cloudresourcemanager
    )

    # Get data from all projects within a folder
    table_data_from_folders = get_project_data_from_folders(
        all_gcp_folders,
        bar_format,
        gcp_discovery.cloudresourcemanager,
        gcp_discovery.billing_account_discovery,
        gcp_discovery.monitoring,
        logger,
        )

    for data in table_data_from_folders:
        table.add_row(data)

    # Get data from all projects within the organization
    table_data_from_org = get_projects_in_org(
        base_config.organization,
        bar_format,
        logger,
        credentials,
        gcp_discovery.cloudresourcemanager,
        gcp_discovery.billing_account_discovery,
        gcp_discovery.monitoring
        )

    for data in table_data_from_org:
        table.add_row(data)

    # Sort table
    table.sort_by()

    # Write to file
    file1 = open('output.txt', 'w')
    file1.write(str(table.pretty_table))
    file1.close()

    logger.info("Done! Data written to output.txt")