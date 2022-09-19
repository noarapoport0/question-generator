# Question Generator

This is a python script that runs daily and post n = 3 data science questions in the #sigma-testing channel. 

## Setup

Set the following environment variables in a `.env` file. 

```
SLACK_BOT_TOKEN=
```

- [Slack Bot Token](https://api.slack.com/apps/A01K7ESN4AW/oauth?) - Oauth & Permissions section of the slack bot being used
    - If there's no existing slack bot [create one](https://slack.com/help/articles/115005265703-Create-a-bot-for-your-workspace)

## Libraries
Use the package manager to install [pip](https://pip.pypa.io/en/stable/) to install [slack_sdk](https://github.com/slackapi/python-slack-sdk). Install any other missing libraries. 

```bash
pip3 install slack_sdk
```

## File Specific Changes
Copy question_generator.py to a directory and make the changes to the file:

```python
# Update the file path to .env in line 9
load_dotenv('dot env file path')

# Set the conversation ID (slack channel key) in line 15 (if necessary)
conversation_id = ""

# Download the JSON questions file to your local computer and load it to the script in line 17
file = ''

# Set the folder location for where your images are stored in line 20
folder = ''

# Set the slack channel where the question should be posted in lines 105, 119 and 123
channel='#'
```

## Schedule
Test that it runs locally. 

```bash
# Local test run
python3 question_generator.py
```

## Example Run
<img width="819" alt="Screen Shot 2022-08-30 at 11 36 21 AM" src="https://user-images.githubusercontent.com/108364344/187516513-82ee7da5-d504-4ac4-80fd-c321848b69de.png">

