#handle and save last updated time here
from datetime import datetime
from azure.storage.fileshare import ShareClient
from azure.storage.fileshare import ShareFileClient
from azure.core.exceptions import ResourceNotFoundError


class StateManager:
    def __init__(self, connection_string, share_name='funcstatemarkershare', file_path='funcstatemarkerfile'):
        self.share_cli = ShareClient.from_connection_string(conn_str=connection_string, share_name=share_name)
        self.file_cli = ShareFileClient.from_connection_string(conn_str=connection_string, share_name=share_name, file_path=file_path)

    def post(self, marker_text: datetime):
        try:
            self.file_cli.upload_file(marker_text)
        except ResourceNotFoundError:
            self.share_cli.create_share()
            self.file_cli.upload_file(marker_text)

    def get(self):
        try:
            return self.file_cli.download_file().readall().decode()
        except ResourceNotFoundError:
            return None

class state:
    before_time = datetime.now()

    def __init__(self, connection_string):
        self.var = StateManager(connection_string)

    #converts datetime string to DS type time
    def convert_to_DS_time(date, hour, minute, second):
        parsed_str = date + "T" + hour + "%3A" + minute + "%3A" + second + ".000Z"  
        return parsed_str

    def convert_to_datetime(date_var):
        date = str(date_var[0:10]).split('-')
        time = str(date_var[11:19]).split(':')
        parsed_date = datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2]))
        return parsed_date


    #gets the last updated time from the pickle file
    def get_last_updated(self):     
        try:
            self.after_time = self.var.get()
        except (EOFError, FileNotFoundError) as e:
            self.after_time = datetime.strptime("2021-09-01 05:23:25", "%Y-%m-%d %H:%M:%S")


    #updates new time in the pickle file
    def update_new_time(self):
        self.var.post(self.after_time)        


    