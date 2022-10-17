from inspect import _void
from university import University

import os.path
from time import time
from difflib import get_close_matches

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

#Object that represents the Esports Program Master List
#https://docs.google.com/spreadsheets/d/1jf1ARsXEpiTPVXfrheZZ045ZiiThfl8WCwyWcdglldY/edit#gid=0

class Spreadsheet:
    #if modifying these scopes, delete the file token.json
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    #the ID and range of a spreadsheet
    SHEET_ID = '1jf1ARsXEpiTPVXfrheZZ045ZiiThfl8WCwyWcdglldY'
    RANGE = '!A4:Q'

    #how many seconds before the object can go before refreshing the data
    TIMEOUT_SECONDS = 120

    def __init__(self):
        self.entries = {}
        self.refresh()
        
    def refresh(self) -> None:
        creds = None
        #the file token.json stores the user's access and refresh tokens, and is
        #created automatically when the authorization flow completes for the first
        #time
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', Spreadsheet.SCOPES)
        #if there are no (valid) credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', Spreadsheet.SCOPES)
                creds = flow.run_local_server(port=0)
            #save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            service = build('sheets', 'v4', credentials=creds)

            #call the sheets api
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=Spreadsheet.SHEET_ID,
                                        range=Spreadsheet.RANGE).execute()
            values = result.get('values', [])
            
            self.entries = {}
            for row in values:
                self.entries.update({row[0].lower() : University(row)})

            self.lastrefresh = time()
        except HttpError as err:
            print(err)

    def getuniversitybyname(self, name: str) -> University:
        '''Takes exact university name string and returns the resulting University.'''
        self.__checktimeoutrefresh()
        for key, value in self.entries.items():
            if(key == name.lower()):
                return value

    def searchuniversitybyname(self, name: str) -> list[University]:
        '''Takes a search string and returns the resulting University list.'''
        self.__checktimeoutrefresh()
        results = []
        found = get_close_matches(name.lower(), self.entries.keys(), 3, 0.5)
        for s in found:
            results.append(self.entries[s])
        return results

    def __checktimeoutrefresh(self) -> None:
        if time() - self.lastrefresh >= Spreadsheet.TIMEOUT_SECONDS:
            self.refresh()

    def __str__(self) -> str:
        self.__checktimeoutrefresh()
        result = ''
        for u in self.entries.values():
            result += f'{u.name}\n'
        return result + f'Total [{len(self.entries)}]'