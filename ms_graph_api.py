import pyperclip
import webbrowser
from msal import PublicClientApplication
import requests



class Ms_Graph_api:

    def __init__(self):
        app_id = "275b1733-43f3-4993-8d62-ae8776a1f12a"
        app_secret = "FhH8Q~0FomL44EekYhfm4QK5ckUy~UOvnxbNnc-1"
        authority_url = "https://login.microsoftonline.com/consumers/"
        base_url = "https://graph.microsoft.com/v1.0/"
        self.endpoint = base_url +'me'
        scopes = ['User.Read','Calendars.ReadWrite']

       ########################################################
        app = PublicClientApplication(
            app_id,
            authority=authority_url,
        )
        flow = app.initiate_device_flow(scopes = scopes)
        app_code = flow['user_code']
        pyperclip.copy(app_code)
        webbrowser.open(flow['verification_uri'])
        result = app.acquire_token_by_device_flow(flow)
        access_token_id = result['access_token']
        self.headers = {'Authorization': 'Bearer ' + access_token_id}


    def insert_ms_event(self,event):
        requests.post(url = self.endpoint +'/calendar/events' ,headers = self.headers,json = event)


