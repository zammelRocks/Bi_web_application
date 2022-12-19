import pandas as pd
import re
import requests


# getting data from API + print data type gotten
def get_data_API(url):
    response_api = requests.get(url)
    data_from_api = response_api.json()
    # print(type(data_from_api))
    return data_from_api



# getting the right information from the json response:
# json to dataframe

def retrieve_fields_from_json(data_from_api):
    records = data_from_api["records"]
    # print(records)
    listOfFields = []
    for input in records:
        listOfFields.append(input["fields"])
    # print(listOfFields)
    df = pd.DataFrame(listOfFields)
    #print(df)
    return df


def visualize_null_values(dataFrame):
    print(dataFrame.isnull())


def eliminating_null_values(dataFrame):
    for col in dataFrame.columns:
        dataFrame[col].fillna(f"No {col} Provided", inplace=True)
    return dataFrame


def valid_mail_by_regex(dataFrame):
    # regex form of mails
    pattern = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    # index
    i = 0
    # summing number of mails valid
    sumMail = 0
    # use : re.fullmatch(regex, email) to match mail with formate
    for col in dataFrame['mail']:
        # state is true if the value fits the regex
        state = bool(re.fullmatch(pattern, col))

        i += 1
        # if col value matches regex defined it's assigned to true
        # print(col," ***** the value state is ****** ", state)
        if state:
            # print(f"=> row number {i} : " , col )
            sumMail = sumMail + 1

    return sumMail


def valid_link_by_regex(dataFrame):

    sumLinks = 0
    links = 0

    for coltype in dataFrame['site_internet']:
        # index
        links = links + 1

        # verify if string begins with https
        x = re.search("^http.*$", coltype)
        if x:
            # print(f"=> row number {links} : ",coltype)
            sumLinks = sumLinks + 1
    return sumLinks

def Home_Delivery_count(df):
    sumLivraison = 0
    liv = 0
    for colservices in df['services']:
        liv = liv + 1
        # verify if string begins Livraisons à domicile
        x = re.search("^Livraisons à domicile.*$", colservices)
        if x:
            # print(f"=> row number {links} : ",colservices)
            sumLivraison = sumLivraison + 1
    return sumLivraison

def Corr_typeB_services(df):
    crossTab = pd.crosstab(df['type_de_commerce'], df['services'])
    return crossTab

def load_lottieur1(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()