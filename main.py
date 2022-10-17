import sys

from spreadsheet import Spreadsheet

#Backend for accessing all university esports data from
#https://docs.google.com/spreadsheets/d/1jf1ARsXEpiTPVXfrheZZ045ZiiThfl8WCwyWcdglldY/edit#gid=0
#using the Google Sheets API.
#
#Created by Kevin Mattix (kmattix@radford.edu)

def all():
    print(f'\n{SPREADSHEET}\n')

def quit():
    sys.exit('\nApplication terminated.')

def help():
    print(f'\nCommands={", ".join(COMMANDS.keys())}\n')

def search(args):
    universities = SPREADSHEET.searchuniversitybyname(args)
    if universities:
        print()
        for u in universities:
            print(f'{u}\n')
    else:
        print('\nNone found.\n') 

SPREADSHEET = Spreadsheet()
COMMANDS = {
    'all': all,
    'quit': quit,
    'help': help,
}  

def main():
    while True:
        args = input('Search: ').lower().strip()
        if args in COMMANDS:
            COMMANDS[args]()
        else:
            search(args)

if __name__ == '__main__':
    main()