import requests
import sys
from bs4 import BeautifulSoup
from datetime import datetime
from getopt import getopt
from getpass import getpass

VAFS_URL = "https://vafs.nus.edu.sg/adfs/oauth2/authorize?response_type=code&client_id=97F0D1CACA7D41DE87538F9362924CCB-184318&resource=sg_edu_nus_oauth&redirect_uri=https%3A%2F%2Fmyaces.nus.edu.sg%3A443%2Fhtd%2Fhtd"
TEMP_SUBMIT_URL = "https://myaces.nus.edu.sg/htd/htd"
TEMP_GET_URL = "https://myaces.nus.edu.sg/htd/htd?loadPage=viewtemperature&actionToDo=NUS"

def login(username, password):
    vafsParams = {
        'UserName': username,
        'Password': password,
        'AuthMethod': 'FormsAuthentication'
    }
    vafsResponse = requests.post(VAFS_URL, data=vafsParams)
    jsessionID = vafsResponse.cookies.get('JSESSIONID')
    if not jsessionID:
        raise Exception('Incorrect login credentials')
    return jsessionID

def submitTemperature(jsessionID, temperature):
    tempDeclOn = datetime.now().strftime('%d/%m/%Y')
    declFrequency = datetime.now().strftime('%p')[0] # 'A' for AM, 'P' for PM
    tempParams = {
        'actionName': 'dlytemperature',
        'webdriverFlag': '',
        'tempDeclOn': tempDeclOn,
        'declFrequency': declFrequency,
        'symptomsFlag': 'N',
        'familySymptomsFlag': 'N',
        'temperature': temperature
    }
    tempResponse = requests.post(TEMP_SUBMIT_URL, data=tempParams, cookies={'JSESSIONID': jsessionID})
    return tempResponse.text

def getTemperature(jsessionID):
    tempResponse = requests.get(TEMP_GET_URL, cookies={'JSESSIONID': jsessionID})
    return tempResponse.text

def parseTemperatureTable(tempResponseText):
    def parseTemperatureRow(row):
        cells = row.find_all('td')
        return [', '.join(cell.text.strip().split(' , ')) for cell in cells]

    soup = BeautifulSoup(tempResponseText, 'html.parser')
    tempTable = soup.find_all('table')[3]
    tempTableBody = tempTable.find('tbody')
    tempTableRows = tempTableBody.find_all('tr')
    tempData = [parseTemperatureRow(row) for row in tempTableRows]
    return tempData

def printData(tempData):
    spacingFormat = '{:<5} {:<25} {:<15} {:<10} {:<20} {:<15} {:<10} {:<20}'
    print(' ' * 51 + 'AM' + ' ' * 46 + 'PM')
    print(spacingFormat.format('S.No', 'Date', 'Temperature °C', 'Symptoms', 'Household Symptoms', 'Temperature °C', 'Symptoms', 'Household Symptoms'))
    print('-' * 125)
    for row in tempData:
        print(spacingFormat.format(*row))

def readIsCheck():
    optdict, _ = getOptdictArgs()
    return '-c' in optdict

def readTemperature():
    if readIsCheck(): return None
    _, args = getOptdictArgs()
    if not args:
        raise Exception('No temperature given')
    return args[0]

def getOptdictArgs():
    optlist, args = getopt(sys.argv[1:], 'c')
    optdict = dict(optlist)
    return optdict, args

def readUsernamePassword():
    with open('config.txt', 'r') as f:
        d = dict(line.strip().split(': ') for line in f.readlines())
        if 'username' in d and 'password' in d:
            return d['username'], d['password']

    username = input('Username (nusstu\e0123456): ')
    password = getpass('Password: ')
    return username, password


if __name__ == '__main__':
    try:
        temperature = readTemperature()
    except Exception as e:
        print('Please provide your temperature as an argument.')
        exit()

    username, password = readUsernamePassword()
    try:
        jsessionID = login(username, password)
    except Exception as e:
        print('Your login credentials are invalid.')
        exit()

    isCheck = readIsCheck()
    if isCheck:
        tempResponseText = getTemperature(jsessionID)
    else:
        tempResponseText = submitTemperature(jsessionID, temperature)
        print('Submitted temperature of %s°C' % temperature)

    tempData = parseTemperatureTable(tempResponseText)
    printData(tempData)
