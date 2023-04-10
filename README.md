# pocket2notion

Simple integration to send saved bookmarks from pocket to notion using both APIs

## Introduction

This integration takes information from Pocket API using the retrieve option: <https://getpocket.com/developer/docs/v3/retrieve>
Then uses the Notion API to insert the bookmark into Notion DB using Notion API: <https://developers.notion.com/docs/working-with-databases>

## Pre-requisites

- Create a Notion Integration and add the connection to the Database
<https://developers.notion.com/docs/create-a-notion-integration>
- The database as it is, should have 2 columns:
  - Name, type: title
  - Link / URL, type: URL
- Create a Pocket Dev Application with Retrieve Permission
<https://getpocket.com/developer/>
- The access_token needs can be obtained by running the `pocketOauth.py` python app, it qill print the Request token and wait for the authorization.
- to authorize, you need to call <https://getpocket.com/auth/authorize?request_token=REQUEST_TOKEN&redirect_uri=http://localhost:8000/callback> replacing the REQUEST_TOKEN with the printed one. After the authorizing, the application will print out the Access Token needed to actually get data from Pocket

## Setup
- after fetching the project, rename the config.properties.example to config.properties

## Docker image

To create the docker image you need to run: 

`docker build --rm -t pocket2notion-app .`


