import requests
import time
import datetime
import os

import configparser

#Read the te properties file
config = configparser.ConfigParser()
config.read('config.properties')

consumer_key = config['pocket']['consumer_key'] # your Pocket API consumer key in the config.properties file
access_token = config['pocket']['access_token'] # your Pocket API access token in the config.properties file

# define the interval between script runs (in seconds)
interval = 20

# define the filename to use for saving the last execution timestamp
timestamp_file = 'last_timestamp.txt'

# load the last execution timestamp from the file (or set to 0 if file doesn't exist)
if os.path.exists(timestamp_file):
    with open(timestamp_file, 'r') as f:
        last_timestamp = int(f.read().strip())
else:
    human_timestamp = '2023-04-09 10:30:00'
    # convert the human-readable timestamp to a datetime object
    dt = datetime.datetime.strptime(human_timestamp, '%Y-%m-%d %H:%M:%S')
    # convert the datetime object to a Unix timestamp
    last_timestamp = dt.timestamp()


# define the endpoint and parameters for the Pocket API
endpoint = 'https://getpocket.com/v3/get'
params = {
    'consumer_key': consumer_key,
    'access_token': access_token,
    'detailType': 'complete', # include full details, including tags
    'sort': 'newest', # sort bookmarks by newest first
    'since': int(last_timestamp) # get bookmarks added or updated since last execution
}

while True:
    # send a POST request to the Pocket API and handle errors
    print('Starting new Cycle')

    try:
        response = requests.post(endpoint, json=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f'Error fetching Pocket data: {e}')
        continue
    print('Executed request')

    # extract the list of bookmarks from the response
    try:
        bookmarks = response.json()['list']
    except (KeyError, ValueError):
        print('Error parsing Pocket data')
        continue

    # print the title and tags for each new bookmark
    print('Checking if there are bookmarks')
    print('bookmarks...', bookmarks)
    if bookmarks:   
        for bookmark in bookmarks.values():
            print ("Bookamark: ", bookmark)
            #if bookmark['status'] == '0':
            if 'time_added' in bookmark: 
                print('time added-', bookmark['time_added'])
                if float(bookmark['time_added'])> float(last_timestamp):
                    print(bookmark['given_title'], ':', bookmark['given_url'])
                    tags = bookmark.get('tags', {}).values()
                    if tags:
                        print('Tags:', ', '.join(tag['tag'] for tag in tags))
                    else:
                        print('No tags')
                        

                    # update the last timestamp to the latest added or updated bookmark
                    last_timestamp = bookmark['time_added']

    
        
        # save the last timestamp to a file
        with open(timestamp_file, 'w') as f:
            f.write(str(last_timestamp))
        bookmarks=''    


    # wait for the specified interval before running the script again
    print('Finished this Cycle')
    time.sleep(interval)
    print('Starting Cycle again')
