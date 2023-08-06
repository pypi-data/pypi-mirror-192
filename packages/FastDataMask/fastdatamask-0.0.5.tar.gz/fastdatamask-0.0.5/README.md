# Masking data in Python.

![Logo.jpeg](Logo.jpeg)

## About this package

This newly created light weight package will invoke the python class that can mask certain categories of data by invoking the right methods. However, you can get back to original data once you mask it. So, you need to use it where you want to test things without any need for getting back to the original data. This application developed using pandas & other useful libraries. This project is for the advanced Python developer & Data Science Newbi's.


## How to use this package

(The following instructions apply to Posix/bash. Windows users should check
[here](https://docs.python.org/3/library/venv.html).)

First, clone this repository and open a terminal inside the root folder.

Create and activate a new virtual environment (recommended) by running
the following:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the requirements:

```bash
pip install -r requirements.txt
```

Run the Augmented Reality-App:

```bash
python playPII.py
```

Make sure that you are properly connected with a functional WebCam or scanned images (Preferably a separate external WebCAM).

Please find the dependent package -

```
numpy==1.24.2
pandas==1.5.3
python-dateutil==2.8.2
FastDataMask==0.0.5

```

## How to use this Package

We need to understand that the current class has some basic limitations. We need to create some wrapper methods to invoke the right masking classifications.

Let's look into them -

```
charList = ccl.clsCircularList()

def mask_email(email):
    try:
        maskedEmail = charList.maskEmail(email)
        return maskedEmail
    except:
        return ''

def mask_phone(phone):
    try:
        maskedPhone = charList.maskPhone(phone)
        return maskedPhone
    except:
        return ''

def mask_name(flname):
    try:
        maskedFLName = charList.maskFLName(flname)
        return maskedFLName
    except:
        return ''

def mask_date(dt):
    try:
        maskedDate = charList.maskDate(dt)
        return maskedDate
    except:
        return ''

def mask_uniqueid(unqid):
    try:
        maskedUnqId = charList.maskSSN(unqid)
        return maskedUnqId
    except:
        return ''
```

From the above, as you can see that you need pass the right text for right sort of masking. You can definitely use this for most of the known use case, which may support your desired data type.

However, this won't support any future date field in this early version.

Let's see the complete code of this config file ->

### playPII.py

```
#####################################################
#### Written By: SATYAKI DE                      ####
#### Written On: 12-Feb-2023                     ####
#### Modified On 16-Feb-2023                     ####
####                                             ####
#### Objective: This is the main calling         ####
#### python script that will invoke the          ####
#### newly created light data masking class.     ####
####                                             ####
#####################################################

import pandas as p
import clsL as cl
from clsConfigClient import clsConfigClient as cf
import datetime
from FastDataMask import clsCircularList as ccl

# Disbling Warning
def warn(*args, **kwargs):
    pass

import warnings
warnings.warn = warn

######################################
### Get your global values        ####
######################################
debug_ind = 'Y'
charList = ccl.clsCircularList()

CurrPath = cf.conf['SRC_PATH']
FileName = cf.conf['FILE_NAME']
######################################
####         Global Flag      ########
######################################

######################################
### Wrapper functions to invoke    ###
### the desired class from newly   ###
### built class.                   ###
######################################
def mask_email(email):
    try:
        maskedEmail = charList.maskEmail(email)
        return maskedEmail
    except:
        return ''

def mask_phone(phone):
    try:
        maskedPhone = charList.maskPhone(phone)
        return maskedPhone
    except:
        return ''

def mask_name(flname):
    try:
        maskedFLName = charList.maskFLName(flname)
        return maskedFLName
    except:
        return ''

def mask_date(dt):
    try:
        maskedDate = charList.maskDate(dt)
        return maskedDate
    except:
        return ''

def mask_uniqueid(unqid):
    try:
        maskedUnqId = charList.maskSSN(unqid)
        return maskedUnqId
    except:
        return ''

def mask_sal(sal):
    try:
        maskedSal = charList.maskSal(sal)
        return maskedSal
    except:
        return ''
######################################
### End of wrapper functions.      ###
######################################

def main():
    try:
        var = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        print('*'*120)
        print('Start Time: ' + str(var))
        print('*'*120)

        inputFile = CurrPath + FileName

        print('Input File: ', inputFile)

        df = p.read_csv(inputFile)

        print('*'*120)
        print('Source Data: ')
        print(df)
        print('*'*120)

        hdr = list(df.columns.values)
        print('Headers:', hdr)

        df["MaskedFirstName"] = df["FirstName"].apply(mask_name)
        df["MaskedEmail"] = df["Email"].apply(mask_email)
        df["MaskedPhone"] = df["Phone"].apply(mask_phone)
        df["MaskedDOB"] = df["DOB"].apply(mask_date)
        df["MaskedSSN"] = df["SSN"].apply(mask_uniqueid)
        df["MaskedSal"] = df["Sal"].apply(mask_sal)

        # Dropping old columns
        df.drop(['FirstName','Email','Phone','DOB','SSN', 'Sal'], axis=1, inplace=True)

        # Renaming columns
        df.rename(columns={'MaskedFirstName': 'FirstName'}, inplace=True)
        df.rename(columns={'MaskedEmail': 'Email'}, inplace=True)
        df.rename(columns={'MaskedPhone': 'Phone'}, inplace=True)
        df.rename(columns={'MaskedDOB': 'DOB'}, inplace=True)
        df.rename(columns={'MaskedSSN': 'SSN'}, inplace=True)
        df.rename(columns={'MaskedSal': 'Sal'}, inplace=True)

        # Repositioning columns of dataframe
        df = df[hdr]

        print('Masked DF: ')
        print(df)

        print('*'*120)
        var1 = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        print('End Time: ' + str(var1))

    except Exception as e:
        x = str(e)
        print('Error: ', x)

if __name__ == "__main__":
    main()

```

Note that the debug indicator is set to "Y". This will generate logs. If you change this to 'N'. No logs will be generated. However, the process will be faster.

You can certainly contact me to add any features. Depending upon my bandwidth, I'll add them. Please share your feedback at my Technical blog site shared below.

## Resources

- To learn more about my website, check out the blog [documentation](https://satyakide.com).
