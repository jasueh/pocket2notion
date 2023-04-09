import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
import configparser

#Read the te properties file
config = configparser.ConfigParser()
config.read('config.properties')

consumer_key = config['pocket']['consumer_key'] # your Pocket API consumer key in the config.properties file
access_token = config['pocket']['access_token'] # your Pocket API access token in the config.properties file


# define the endpoint and parameters for the Pocket API
endpoint = 'https://getpocket.com/v3/oauth/request'
params = {
    'consumer_key': consumer_key,
    'redirect_uri': 'http://localhost:8000/callback'
}

# send a POST request to the Pocket API
response = requests.post(endpoint, data=params)

# extract the request token from the response
request_token = response.text.split('=')[1]
print('Request token:', request_token)
        
# define a callback HTTP server to receive the Pocket API response
class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # extract the request token from the query parameters
        request_token = self.path.split('=')[1]

        # send the request token back to the original script
        self.wfile.write(('Request token: ' + request_token).encode())
        
        

# start the callback HTTP server
httpd = HTTPServer(('localhost', 8000), CallbackHandler)
print('Listening on http://localhost:8000/callback...')
httpd.handle_request()

# continue with step 3 and step 4 to authorize your application and obtain an access token

# define the endpoint and parameters for the Pocket API
endpoint = 'https://getpocket.com/v3/oauth/authorize'
params = {
    'consumer_key': consumer_key,
    'code': request_token
}

# send a POST request to the Pocket API
response = requests.post(endpoint, data=params)
print('response:', response)
# extract the access token from the response
access_token = response.text.split('=')[1]

# print the access token
print('Access token:', access_token)
