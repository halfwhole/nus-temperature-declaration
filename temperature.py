import requests
from bs4 import BeautifulSoup
from datetime import date
from getpass import getpass

VAFS_URL = "https://vafs.nus.edu.sg/adfs/oauth2/authorize?response_type=code&client_id=97F0D1CACA7D41DE87538F9362924CCB-184318&resource=sg_edu_nus_oauth&redirect_uri=https%3A%2F%2Fmyaces.nus.edu.sg%3A443%2Fhtd%2Fhtd"

TEMP_URL = "https://myaces.nus.edu.sg/htd/htd"

def login(username, password):
    vafsParams = {
        'UserName': username,
        'Password': password,
        'AuthMethod': 'FormsAuthentication'
    }
    vafsResponse = requests.post(VAFS_URL, data=vafsParams)
    jsessionID = vafsResponse.cookies.get('JSESSIONID')
    return jsessionID

def submitTemperature(jsessionID, temperature):
    tempDeclOn = date.today().strftime('%d/%m/%Y')
    tempParams = {
        'actionName': 'dlytemperature',
        'webdriverFlag': '',
        'tempDeclOn': tempDeclOn,
        'declFrequency': 'A',
        'symptomsFlag': 'N',
        'familySymptomsFlag': 'N',
        'temperature': temperature
    }
    tempResponse = requests.post(TEMP_URL, data=tempParams, cookies={'JSESSIONID': jsessionID})
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

if __name__ == '__main__':
    username = input('Username (nusstu\e0123456X): ')
    password = getpass('Password: ')
    temperature = input('Temperature (°C): ')
    print('Submitting temperature of %s°C ... ' % temperature, end='')
    jsessionID = login(username, password)
    tempResponseText = submitTemperature(jsessionID, temperature)
    print('done!')
    tempData = parseTemperatureTable(tempResponseText)
    printData(tempData)
