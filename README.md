# - Jokes API -

Small REST API designed to serve a random joke.

## Requirements:
  - python3
  - (optional) docker

## Usage:
 - install dependencies : pip3 install -r requirements.txt
 - add environement variables (see, edit and run setenv.sh)
 - run : python jokes-api.py

## Usage with docker:
 - docker build --tag jokes-api .
 - docker run -it -v ~/dir/jokes.json:/jokes.json -e JSON_FILE_PATH=/jokes.json --rm jokes-api

## Notes
 - JSON_FILE_PATH env. variable must be set to jokes.json full path
 - see example-jokes.json for a JSON file example
 - (optional) by default, run on port '5050' (custom port with 'API_PORT' environement variable)
 - (optional) by default, base URL is '/' (custom path prefix with 'API_BASE_URL' environement variable)

## Available APIs
 - /joke/random [ get a random joke ]
 - /joke/type/list [ list jokes types, see 'type' member in the json structure ]
 - /joke/type/:type [ get a joke with a specific type, see 'type' member in the json structure ]
