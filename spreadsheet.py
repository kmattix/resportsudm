#Backend for accessing all university esports data from
#https://docs.google.com/spreadsheets/d/1jf1ARsXEpiTPVXfrheZZ045ZiiThfl8WCwyWcdglldY/edit#gid=0
#using the Google Sheets API.
#
#Created by Kevin Mattix (kmattix@radford.edu)

from __future__ import print_function

from university import University

import os.path
from difflib import get_close_matches

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class Spreadsheet:
    #if modifying these scopes, delete the file token.json
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    #the ID and range of a spreadsheet
    SHEET_ID = '1jf1ARsXEpiTPVXfrheZZ045ZiiThfl8WCwyWcdglldY'
    RANGE = '!A4:Q'

    def __init__(self):
        self.entries = {}
        self.refresh()
    

    def refresh(self):
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
        except HttpError as err:
            print(err)

    def getuniversitybyname(self, name: str):
        '''Takes exact university name string and returns the resulting University.'''
        for key, value in self.entries.items():
            if(key == name.lower()):
                return value

    def searchuniversitybyname(self, name: str) -> list:
        '''Takes a search string and returns the resulting University list.'''
        results = []
        found = get_close_matches(name.lower(), self.entries.keys(), 3, 0.5)
        for s in found:
            results.append(self.entries[s])
        return results

    def __str__(self) -> str:
        result = ''
        for u in self.entries.values():
            result += f'{u.name}\n'
        return result + f'Total [{len(self.entries)}]\n'