def get_billing_info(project: object, gcp_discovery_billing: object, logger: object) -> dict:
    """
    It gets the billing info for a project
    
    :param project: the project object
    :param gcp_discovery_billing: The discovery object for the billing API
    :param logger: a logger object
    :return: The billing info for the project
    """
    try:
        request = gcp_discovery_billing.projects().getBillingInfo(name=project.project_name)
        response = request.execute()
    except KeyError:
        logger.error('Something wrong when getting billing info')
        exit()

    return response