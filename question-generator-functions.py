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

def read_questions(file): # reads questions from local folder and puts them into a dataframe
    # read in file from local folder 
    with open(file,'r') as f: 
        data = json.loads(f.read()) # load data using Python json module
    pd.set_option("display.max_colwidth", -1)
    questions_dataframe = pd.json_normalize(data, record_path=['questionsList']) # flattens nested list 'questionsList'
        # stores it in a dataframe
    indexes = []
    indexes = questions_dataframe[questions_dataframe['question'] == ''].index # indexes of empty questions
    indexes = indexes.append(questions_dataframe[questions_dataframe['question'] == "PLACEHOLDER"].index) # indexes of placeholder questions
    questions_dataframe = questions_dataframe.drop(indexes) # delete all empty / placeholder questions
    return(questions_dataframe) # return cleaned dataframe

class Question: # Question class 
    def __init__(self, question, answer, image):
        self.question = question
        self.answer = answer
        self.image = image 

def select_question(dataframe): # function to select a random question object
    random = dataframe.sample() 
    question1 = Question(question = random["question"].to_string(), answer = random["answer"].to_string(), image = random["image"].to_string()) # transform each part to string
    question1.question = question1.question.split("    ")[1]
    question1.answer = question1.answer.split("    ")[1]
    question1.image = question1.image.split("    ")[1]
    return(question1)

    
 # function to test if our question is new 
def read_slack_message(conversation_id, date, slack_client):  # function to read old slack messages
    # date parameter can be changed to any date, default is just today's date
    try:
        # Call the conversations.history method using the WebClient
        # The client passes the token you included in initialization    
        result = slack_client.conversations_history( # finding the slack message
            channel=conversation_id,
            inclusive=True,
            oldest=date,
            limit = 500
        )
        return result
    except SlackApiError as e: # returns error message if there is an issue with the slack api function
        print(f"Error: {e}")

def posted_slack_questions(conversation_id): # function that pulls old slack messages and puts them into a list
    # date parameter can be changed to any date, default is just today's date
    messages = []
    today = date.today() # function that find's today's date
    two_weeks_ago = today - timedelta(days=14)
    oldest_date = time.mktime(two_weeks_ago.timetuple()) # slack function needs timestamp in form of unix to recognize time
    message = read_slack_message(conversation_id, date = oldest_date) # read slack messages dating back to two weeks 
    for i in range(0,60):
        messages.append(message["messages"][i]["text"]) # append messages to list
        # Print message text
    return(messages) # list that contains slack messages from two weeks ago to now

def select_questions(n, dataframe): # function that selects n random questions
    objects = []
    questions = [] # empty array to store question objects
    for i in range(n): 
        random_selection = select_question(dataframe) # select a random question
        objects.append(random_selection) # append to objects list
    for i in range(n):
        questions.append(objects[i].question) # append to list that only contains questions
    res = [index for index, val in enumerate(questions) if val in questions[:index]] # find all indexes where questions are duplicates
    if len(res) != 0: # if there are duplicates, ie, length of res list is > 0
        for i in res:
            del objects[i] # delete all duplicates
    return(objects)
