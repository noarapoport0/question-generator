from dotenv import load_dotenv
from datetime import date, timedelta, time
import pandas as pd
import numpy as np
import time
import json
import gspread
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os
import re
from functions import *
slack_token = os.environ["SLACK_BOT_TOKEN"] # connects to slack
client = WebClient(token=slack_token) # ID of channel that the message exists in

file = 'file path not shown'
folder = 'folder path not shown'
conversation_id = "conversation id not shown"

questions_dataframe = read_questions(file) 
cat_index = [] # tracking indexes that aren't in the categories we want
datascience = ['DataScience']
sql = ['SQL']
dbt = ['DBT']

categories_list = [['DataScience'], ['SQL'], ['DBT']]




categories = list(questions_dataframe['categories'])
for i in range(0, len(categories)):
    if categories[i] not in categories_list: # select indexes of categories that we don't want
        cat_index.append(i)
questions_dataframe = questions_dataframe.drop(questions_dataframe.index[cat_index]) # drop those questions from the dataframe


if questions_dataframe.empty: # make sure there is data inside the JSON file
    print("There is no data in the JSON file.")
old_questions = posted_slack_questions(conversation_id)

questions_list = select_questions(5, questions_dataframe) # select 20 random questions

questions_posted = 0
for i in range(len(questions_list)):
    if questions_list[i].answer not in (old_questions): # make sure question is new and hasn't been posted already
        client.chat_postMessage(channel='#', # post question
            text = "",
            blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": str(i+1) + ") "+ questions_list[i].question
                    }
                }
            ] 
        )
        if questions_list[i].image != "NaN": # if there is an image post image
            client.files_upload(
                channels=['#'],
                file=folder+questions_list[i].image,
            )
        else:
            client.chat_postMessage(channel='#',  # else just post the answer
                text = "",
                blocks= [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": questions_list[i].answer
                        }
                    }
                ] 
            )
        questions_posted += 1
    if questions_posted == 3: # once three questions are posted exit script
        break
    