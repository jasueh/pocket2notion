import os
import requests
from pprint import pprint
import configparser

config = configparser.ConfigParser()
config.read('config.properties')

# Set up Notion API keys and database ID
NOTION_API_KEY = config['notion']['api_key'] 
NOTION_DATABASE_ID = config['notion']['db_id'] 
NOTION_URL = config['notion']['url'] 



# Create a new page in the Notion database
def create_database_item(title, description):
    headers = {
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {NOTION_API_KEY}",
    }

    data = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Name": {"title": [{"text": {"content": title}}]},
            "Link / URL": {"url": description}
        }
    }

    response = requests.post(f"{NOTION_URL}/pages", headers=headers, json=data)
    pprint(response.json())

# Insert elements into the Notion database
#create_database_item("First Item", "http://google.com")
#create_database_item("Second Item", "http://google.com")