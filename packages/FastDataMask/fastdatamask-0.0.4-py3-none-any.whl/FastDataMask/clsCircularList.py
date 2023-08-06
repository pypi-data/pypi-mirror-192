#####################################################
#### Written By: SATYAKI DE                      ####
#### Written On: 10-Feb-2023                     ####
#### Modified On 15-Feb-2023                     ####
####                                             ####
#### Objective: This is the main class that      ####
#### contains the core logic of light weight     ####
#### data-maskign of certain data categories.    ####
####                                             ####
#####################################################

import random
import sys
import errno
import math

###############################################
###           Global Section                ###
###############################################

# Disbling Warning
def warn(*args, **kwargs):
    pass

import warnings
warnings.warn = warn

###############################################
###    End of Global Section                ###
###############################################
class clsCircularList:
    def __init__(self):
        self.items = []
        self.current = 0

    def addItem(self, item):
        self.items.append(item)

    def initChar(self):
        self.addItem('a')
        self.addItem('b')
        self.addItem('c')
        self.addItem('d')
        self.addItem('e')
        self.addItem('f')
        self.addItem('g')
        self.addItem('h')
        self.addItem('i')
        self.addItem('j')
        self.addItem('k')
        self.addItem('l')
        self.addItem('m')
        self.addItem('n')
        self.addItem('o')
        self.addItem('p')
        self.addItem('q')
        self.addItem('r')
        self.addItem('s')
        self.addItem('t')
        self.addItem('u')
        self.addItem('v')
        self.addItem('w')
        self.addItem('x')
        self.addItem('y')
        self.addItem('z')

    def initNum(self):
        self.addItem('0')
        self.addItem('1')
        self.addItem('2')
        self.addItem('3')
        self.addItem('4')
        self.addItem('5')
        self.addItem('6')
        self.addItem('7')
        self.addItem('8')
        self.addItem('9')

    def getCurrent(self):
        if len(self.items) == 0:
            return None
        return self.items[self.current]

    def nextItem(self):
        if len(self.items) == 0:
            return None
        self.current = (self.current + 1) % len(self.items)

    def prevItem(self):
        if len(self.items) == 0:
            return None
        self.current = (self.current - 1) % len(self.items)

    def findItem(self, item):
        if len(self.items) == 0:
            return None
        for i in range(len(self.items)):
            if self.items[i] == item:
                return i
        return None

    def maskedItem(self, item):
        self.items = []
        self.current = 0
        val = ''
        upperFlag = False

        inputItem = item
        maskedVal = ''

        uVal = inputItem.isupper()

        if uVal:
            upperFlag = True

        if inputItem.isdigit():
            self.initNum()
            maskedVal = random.randrange(1, 9)
            #print('Number maskedVal:', maskedVal)
        elif inputItem == '.':
            pass
        else:
            self.initChar()
            maskedVal = random.randrange(1, 26)
            #print('Char maskedVal: ', maskedVal)

        if len(self.items) == 0:
            return None

        for i in range(len(self.items)):
            if self.items[i] == inputItem.lower():
                for j in range(maskedVal):
                    val = ''
                    tval = ''
                    xval = self.prevItem()
                    tval = self.getCurrent()

                    if upperFlag == True:
                        val = tval.upper()
                    else:
                        val = tval
                return val
        return None

    def getChar(self, inputStr):
        x = inputStr
        idx = self.maskedItem(x)

        return idx

    def getDate(self, inputStr):
        ### YYYY-MM-DD
        x = inputStr
        idx = self.maskedItem(x, True)

        return idx

    def maskFLName(self, name):
        try:
            strVal = ''

            lst = list(name)

            for l in lst:
                val = self.getChar(l)
                if val is None:
                    strVal = strVal + l
                else:
                    strVal = strVal + val

            return strVal
        except:
            return ''

    # Define the masking function for email addresses
    def maskEmail(self, email):
        try:
            strVal = ''
            parts = email.split("@")
            username = parts[0]
            domain = parts[1]

            lst = list(username)

            for l in lst:
                val = self.getChar(l)
                if val is None:
                    strVal = strVal + l
                else:
                    strVal = strVal + val

            return strVal + "@" + domain
        except:
            return ''

    # Define the masking function for phone numbers
    def maskPhone(self, phone):
        try:
            strVal = ''

            lst = list(phone)
            for l in lst:
                val = self.getChar(l)
                if val is None:
                    strVal = strVal + l
                else:
                    strVal = strVal + val

            return strVal
        except:
            return ''

    # Define the masking function for phone numbers
    def maskSSN(self, ssn):
        try:
            strVal = ''

            lst = list(ssn)
            for l in lst:
                val = self.getChar(l)
                if val is None:
                    strVal = strVal + l
                else:
                    strVal = strVal + val

            return strVal
        except:
            return ''

    def maskDate(self, dateInput):
        try:
            ### YYYY-MM-DD
            maskedYrToken = random.randrange(1, 5)
            strVal = ''

            yr, mn, dt = dateInput.split('-')

            maskedYr = int(yr) + maskedYrToken

            maskedMnToken = random.randrange(1, 12)

            resVal = int(mn) + maskedMnToken

            if resVal > 12:
                maskedMn = maskedMnToken
            else:
                maskedMn = resVal

            if maskedMn == 2:
                maskedDayToken = random.randrange(1, 28)
                resDay = int(dt) + maskedDayToken
            else:
                maskedDayToken = random.randrange(1, 29)
                resDay = int(dt) + maskedDayToken

            if resDay > 31:
                maskedDay = maskedDayToken
            else:
                maskedDay = resDay

            strVal = str(maskedYr).rjust(4,'0') + '-' + str(maskedMn).rjust(2,'0') + '-' + str(maskedDay).rjust(2,'0')

            return strVal
        except:
            return ''

    def maskSal(self, sal):
        try:
            flg = 0
            maskedSal = ''

            flg = random.randrange(0, 1)
            maskedSal = ''

            if flg == 0:
                maskedSal = str(float(sal) * random.randrange(75, 85)/100)
            else:
                maskedSal = str(float(sal) * random.randrange(105, 125)/100)

            return round(float(maskedSal),2)
        except Exception as e:
            x = str(e)
            return 0.00
