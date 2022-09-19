import pandas as pd
import numpy as np
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
import gspread


# load google service account 
try:
    sa = gspread.service_account('service acount sheet')
    sh = sa.open("Google Sheet") # Google Sheet we're querying from
    wks = sh.worksheet("Workbooks")
    output = 'Success'
except Exception as e:
    output = 'Fail'
    error_message = e 

if output == 'Success': # Make sure we are connected to the google sheet
    message = 'Connected to google sheets'
else:
    message = 'Connection to google sheets failed' + ':' + str(error_message)

storage_string = "" # create empty string
def create_bullet(name, url, summary, include_summary = True):
        if include_summary == True: # Choose whether to show the summary 
            return('<'+url+'|'+name+'>'+' -- '+summary) # Slack Markdown Syntax
        else:
            return('<'+url+'|'+name+'>')

dataframe = pd.DataFrame(wks.get_all_records()) # put Google Sheet records into a dataframe
dataframe = dataframe.replace(r'^\s*$', np.nan, regex=True)

if dataframe.empty:
    storage_string = "There is no data in the google sheet."
elif dataframe.isnull().values.any():
    storage_string = "There are missing values in the google sheet."
else:
    uniques = counter = 0
    for current_category in np.unique(dataframe['Category']): # iterate through the unique categories in the data
        storage_string += '*' + current_category + '*' + '\n'
        uniques += len(dataframe[dataframe['Category']==current_category]) # count how many workbooks are in this category
        for j in range(counter, uniques):
            storage_string += '\t' + create_bullet(dataframe.iloc[j, 2], dataframe.iloc[j, 1], dataframe.iloc[j, 3], True) + '\n' # add the data to a string
            counter += 1



slack_token = os.environ["SLACK_BOT_TOKEN"] # connect to slack 
client = WebClient(token=slack_token)
client.chat_postMessage(channel='# channel', 
    blocks= [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": storage_string
            }
        }
    ] 
)
