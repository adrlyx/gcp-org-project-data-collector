from googleapiclient import discovery
class GcpDiscovery():

    def __init__(self, credentials: object):
        self.billing_account_discovery = discovery.build('cloudbilling', 'v1', credentials=credentials)
        self.cloudresourcemanager = discovery.build('cloudresourcemanager', 'v3', credentials=credentials)
        self.monitoring = discovery.build('monitoring', 'v3', credentials=credentials)