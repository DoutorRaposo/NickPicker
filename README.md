# NickPicker
#### Video Demo: TODO
#### Description:

This is my final project for CS50W. It is a website that serves as a movie picker for Nicolas Cage movies. You answers a few questions and get back a series of recommendations. You can also look up movies in the search bar, see the movie list by genre or check out all movies. Every movie has a personal page with more details.

## Distinctiveness and Complexity:

I believe this project is distinct enough from the other exercises in this cours: by using several models, combining server-side rendering (on movie pages, search bar and genre/all set) with client-side rendering (in the test questions and results), I believe it is complex enough to utilize all the knowledge (and more!) provided by the previous projects.

## Features:

- Take a quick test to find the recommended movies! You can select preferred genre, decade, age certification and order by popular vote and/or favorite keywords
- Responsive layout for tablet, smartphones and desktop devices
- Random movie: click a button and be surprised with a movie recommendation!
- All the movies or by genre
- Query for a movie using the search bar for a movie using keywords, genres, director or cast names

## How to run:

There are two ways of running: 

> python manage.py runserver
>
> docker-compose up*

 After running, you can open the webpage and explore all the features that I listed above. The main feature is the quiz on the main page. Take it and see if you can find a movie to watch!

*By using the dockerfile I provided, which comes with a few details to look for that I explained below.

### Runserver or Docker-compose:

You don't need to use docker necessarily, but I use it to easily be able to check the responsiveness on other devices in my network. Note that I'm using port 10000 because I use the 8000 in my local network for other services. The internal port of the docker is 8000, though, and using address 0.0.0.0. Just be sure to check the settings for allowed hosts if using docker!

### Database restore:

If by any reason you mess up the database, restore it by opening Django Shell and running (if you deleted the database, please migrate first!):

> from db_src.restore import restore_db
>
> restore_db()

If you wish to update the database with the latest information from TMDB (if you have an API key), you can recreate the JSON files that are used for restoring the database by opening the Django Shell and running:

> from create_json import generate
>
> generate()

But to do this, you need a TMDB_API_Key as an enviroment variable or in an .env file in the root of the project.

## Description of custom files and folders:

### db_src

#### JSON files
db_src contains several json files: combined.json, genres_movies.json and genres_tv.json. Those files consist of a JSON version of the database, just so we can quickly restore the database if needed.

#### Python modules
db_src also is a module in itself that contains the restore.py file (responsible for clearing the DB in the Django Shell and putting everything in the JSON files in the Django models).
The create_json.py is responsible for downloading the database from TMDB if you want to update. However, as noted, this requires and TMDB_API_KEY as a enviroment variable or a dotenv file.
With a few adjustments I believe we could even change the actor that the site is based on.

#### movie_picker/context_processors.py

This file gives the context for all the templates that contains the information on the genres, just so that every page that uses the navbar generates all the viable genres

#### nick/templatetags

This module is responsible for filtering some information from the models, such as budget, and converting to money format, for example, for readability.

#### nick/questions.py

This file have all the questions that will be used in the main page. You could add more as long as you follow the pattern of:

- Title
- Type (this is the identity of the question, then you have to customize the "results" view to add the filter for this question)
- a list of options with a value for the answers and the human readable version
- and the SELECT info (img, and or xor, that consists if you are using exclusive answers or multiple choice)

#### Dockerfile and docker-compose.yaml

Just creates a docker image that is enabled to run on the local network for testing on other devices (as long as your firewall is configured as well!)

#### Static files:

The images folders contains all assets that are not external such as background and gifs
CSS files include a standard reset file, some alterations to bootstrap and the general styles.css.

The script.js have all the logic for the quiz: rendering questions, transitions between questions, if you can select one answers or several, if there is an answers that deselects others and the function to fetch results and render the results card (and the transitions between them).

A note on script.js is that the served version removes the comments to spare space, but there is a version with all the comments in src-js. I've used babel to convert one file to another just so the comments are removed and the file is smaller.

#### Alterations on "default" files

With django rest framework installed, I altered the settings.py to enable it and added other allowed hosts for device testing.

The admin.py have all the options just for testing with the models. Did a few tricks for testing, such as custom list display fields, search fields, adding count for ManyToMany models by overwriting the superclass, etc.

Models.py includes the titles, directors, company, keywords and genre. Some of these models have a valid() method that filters to only movies that are released and are not below 2 in vote average.

There are several views:

- first of all, they use the template.html so we have the navbar in all pages
- index is the main page. The decorator ensures that CSRF cookies exists even if for some reason they don't appear (maybe the protocol or if the request comes from external host). This is were most of the javascript works
- get_movies can show every movie or by genre (two paths that render the same view but customized)
- get_title show a single movie
- random_title redirects to a random get_title page
- search allow the user to query all movies by using various fields from the Title model
- get_questions just generates a JsonResponse with all the questions in questions.py
- results will filter the valid Title data with the answers from the questions. You can customize max number of results
- TitleViewSet is the DRF responsible for serializing all the valid titles so we can feed the results in the 'result' view


Urls.py includes every view plus a note from DRF that enables router registered for the titles API.

