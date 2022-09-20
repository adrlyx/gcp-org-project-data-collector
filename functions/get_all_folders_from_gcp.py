from tqdm import tqdm
from models.Folder import Folder
from functions.find_folders import find_folders


def get_all_folders_from_gcp(
        response: dict,
        all_folder_obj: list,
        all_folders: list,
        temp_folders: list,
        org_top_folders:list,
        gcp_discovery_cloudresourcemanager: object
        ) -> list:
    """
    This function takes in the response from the GCP API call, a list of all folders, a list of
    temporary folders, a list of top level folders, and the GCP discovery API object. It then loops
    through the response and creates a folder object for each folder in the response. It then loops
    through the top level folders and calls the find_folders function on each one
    
    :param response: The response from the GCP API call to get the top level folders
    :param all_folder_obj: This is a list of all the folders in the organization
    :param all_folders: This is a list of all the folders in the organization
    :param temp_folders: This is a list of all the folders that are currently being searched
    :param org_top_folders: This is a list of the top level folders in the organization
    :param gcp_discovery_cloudresourcemanager: This is the discovery object that we created earlier
    :return: A list of all folders in the organization
    """
    for folder in response['folders']:
        folder_obj = Folder(folder['name'], folder['displayName'])
        org_top_folders.append(folder_obj)
        all_folder_obj.append(folder_obj)

    bar_format='{l_bar}{bar:40}{r_bar}{bar:-10b}'

    for folder_obj in tqdm(org_top_folders, bar_format=bar_format, desc="Collecting data from GCP  ", position=0, leave=True):
        find_folders(folder_obj, temp_folders, all_folders, gcp_discovery_cloudresourcemanager)

    return all_folders