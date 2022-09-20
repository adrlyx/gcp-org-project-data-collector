def get_top_org_folders_from_gcp(parent: str, gcp_discovery_cloudresourcemanager: object) -> dict:
    """
    > This function takes a parent folder ID and returns a list of all the top-level folders in that
    parent folder.
    
    :param parent: The parent resource name. Must be of the form organizations/{organization_id}
    :param gcp_discovery_cloudresourcemanager: The discovery service for the Cloud Resource Manager API
    :return: A list of folders
    """
    request = gcp_discovery_cloudresourcemanager.folders().list(parent=parent)
    response = request.execute()

    return response