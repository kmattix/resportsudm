#Backend for accessing all university esports data from
#https://docs.google.com/spreadsheets/d/1jf1ARsXEpiTPVXfrheZZ045ZiiThfl8WCwyWcdglldY/edit#gid=0
#using the Google Sheets API.
#
#Created by Kevin Mattix (kmattix@radford.edu)

from __future__ import print_function

from university import University
from spreadsheet import Spreadsheet

def main():
    spreadsheet = Spreadsheet()
    while(True):
        args = input('Search: ').lower()

        if(args == 'quit'):
            break
        
        if(args != 'all'):
            universities = spreadsheet.searchuniversitybyname(args)
            if universities:
                for u in universities:
                    print(f'\n{u}\n')
            else:
                print('\nNone found.\n')
        else:
            print(spreadsheet)

if __name__ == '__main__':
    main()