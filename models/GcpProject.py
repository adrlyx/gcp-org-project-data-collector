class GcpProject():

    def __init__(self, project_name: str, project_id: str, project_display_name: str):
        self.project_id = project_id
        self.members = "N/A"
        self.creator = []
        self.project_name = project_name
        self.project_display_name = project_display_name
        self.project_labels = "N/A"

    def set_members(self, member: str):
        self.members = []
        self.members.append(member)

    def set_creator(self, creator: str):
        self.creator.append(creator)

    def set_labels(self, project_labels: list):
        self.project_labels = project_labels

    def set_billing_account(self, billing_enabled: bool):
        self.billing_enabled = billing_enabled

    def set_metrics_api_request_count(self, request_count: int):
        self.request_count = request_count

    def set_log_bucket_kilobytes(self, log_kilobytes: str):
        self.log_kilobytes = log_kilobytes