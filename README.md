# NickPicker
#### Video Demo: TODO
#### Description:

This is my final project for CS50W

### Features

### TODO:


#### Docker-compose:

You don't need to use docker necessarily, but I use it to easily be able to check the responsiveness on other devices in my network. Note that I'm using port 10000 because I use the 8000 in localhost for other stuff. The internal port of the docker is 8000, though, and using address 0.0.0.0.

#### Database restore:

If by any reason you mess up the database, restore it by opening Django Shell and running (if you deleted the database, please migrate first!):

> from db_src.restore import restore_db
> restore_db()

If you wish to update the database with the latest information from TMDB (if you have a API key), you can recreate the JSON files that are used for restoring the database by opening the Django Shell and running:

> from create_json import generate
> generate()

But to do this, you need a TMDB API Key as an enviroment variable or in an .env file in the root of the project.