from datetime import datetime
from random import choice
from temperature import *

LOG_FILE = 'temp.log'

def hasDeclared(tempData):
    lastDeclaredDate = tempData[0][1].split(', ')[0]
    todayDate = datetime.now().strftime('%d/%m/%Y')
    if lastDeclaredDate != todayDate: return False

    lastTempAM = tempData[0][2]
    lastTempPM = tempData[0][5]

    isAM = datetime.now().hour < 12
    if isAM: return lastTempAM != ''
    else:    return lastTempPM != ''

def getRandomTemperature():
    temp = choice(range(362, 374)) / 10
    tempStr = '%.1f' % temp
    return tempStr

def logMessage(msg):
    with open(LOG_FILE, 'a') as f:
        f.write('%s' % msg)

if __name__ == '__main__':
    logMessage('[%s] ' % datetime.now().strftime('%d/%m/%y %H:%M:%S'))
    username, password = readUsernamePassword()
    jsessionID = login(username, password)
    tempResponseText = getTemperature(jsessionID)
    tempData = parseTemperatureTable(tempResponseText)

    if hasDeclared(tempData):
        logMessage('Already declared temperature\n')
    else:
        temperature = getRandomTemperature()
        tempResponseText = submitTemperature(jsessionID, temperature)
        tempData = parseTemperatureTable(tempResponseText)
        logMessage('Submitted temperature of %s°C\n' % temperature)
