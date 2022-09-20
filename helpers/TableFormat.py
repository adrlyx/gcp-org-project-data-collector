from prettytable import PrettyTable


class TableFormat:

    def __init__(self):
        self.pretty_table = PrettyTable([
            'Folder Name',
            'Folder ID',
            'DisplayName',
            'ProjectName',
            'ProjectId',
            'User/Owner',
            'Labels',
            'BillingEnabled',
            '2Weeks API RequestCount',
            '1M Log Bytes Ingested'
        ])

    def add_row(self, row_list: list )-> list:
        empty_list = []
        empty_list.append(row_list)
        for row in empty_list:
            self.pretty_table.add_row(row)

        return self.pretty_table

    def sort_by(self):
        self.pretty_table.sortby = '2Weeks API RequestCount'