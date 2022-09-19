# Master Sheet Run Summary

This is a python script that queries a google sheet and post the summary to slack. The google sheet contains the category of a sigma workbook, the workbook's name, the URL of the workbook and a summary of what the workbook contains. This is useful for monitoring the sigma workbooks, and getting the main information needed on them.

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
Copy master_sheet_run_summary.py to a directory and make the changes to the file:

```python
# Update the file path to .env in line 8
load_dotenv('dot env file path')

# Load google service account in line 12
sa = gspread.service_account('')

# Set the slack channel in line 52 (if necessary)
channel='#',
```

## Schedule
Test that it runs locally. 

```bash
# Local test run
python3 master_sheet_run_summary.py
```