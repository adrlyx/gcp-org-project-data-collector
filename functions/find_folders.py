from models.Folder import Folder


def find_folders(folder: object, temp_folders: list, all_folders: list, cloudresourcemanager: object):
    """
    It takes a folder object, a list of temporary folders, a list of all folders, and a
    cloudresourcemanager object. It then makes a request to the cloudresourcemanager API to get a list
    of folders under the folder object. If the folder object is not in the list of all folders, it adds
    it to the list of all folders. If the response from the API contains a list of folders, it creates a
    folder object for each folder in the list and adds it to the list of temporary folders. If the list
    of temporary folders is not empty, it calls the function again for each folder in the list of
    temporary folders.
    
    :param folder: the folder object that we want to search for subfolders
    :param temp_folders: This is a list of folders that are found in the current folder
    :param all_folders: This is a list of all the folders in the organization
    :param cloudresourcemanager: the API object that we created earlier
    """
    temp_folders = []
    
    request = cloudresourcemanager.folders().list(parent=folder.folder_name)
    response = request.execute()
    
    if folder not in all_folders:
        all_folders.append(folder)

    if 'folders' in response.keys():
        for each in response['folders']:
            folder_obj = Folder(each['name'], each['displayName'])
            temp_folders.append(folder_obj)

    if temp_folders:
        for folder in temp_folders[:]:
            find_folders(folder, temp_folders, all_folders, cloudresourcemanager)
            temp_folders.remove(folder)
