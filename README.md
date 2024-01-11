# NickPicker
#### Video Demo: TODO
#### Description:

This is my final project for CS50W

### Features


### TODO:

remove debug=true

from db_src.restore import restore_db
restore_db()
Also elaborate more on this script

Run this from the Django's management shell to use the json files to create the database. Don't forget to run the necessary migrations if you deleted you database.

from db_src.create_json import generate
generate()

Run this from the Django's management shell to download the json files from TMDB's API. You need to have your headers in API_headers.py to execute this. This process is long and you should only do it if you want to mess around with the project. You need your own API key to do this!

In API_headers.py inside db_src directory:

headers = {
    "accept": "application/json",
    "Authorization": <<Insert your bearer API key here!>>
}

remove admin?