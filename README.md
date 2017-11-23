# Beatnik
Aggregates links for music streaming services given a song, album, or artist

## LinkConverter
The link converter will accept a link to a song on a streaming service as input and produce links to a matching song on all supported streaming services as output.

## Supported Services
The currently supported services are listed below:
* Google Play Music
* Spotify

## Requirements
* Python >= 3.5.2
* PostgreSQL 9.6

## Setup
1. Clone the repo
2. Setup a python virtual environment
3. Run `pip install -r requirements.txt`
4. Register the app with Spotify and set the `SPOTIPY_CLIENT_ID` and `SPOTIPY_CLIENT_SECRET` environment variables according to what you got from Spotify
5. Set the `GPM_USERNAME` and `GPM_PASSWORD` environment variables to valid Google Account details, note that for accounts with 2fa enabled you need an app password
6. Set the `POSTGRES_USERNAME` and `POSTGRES_PASSWORD` environment variables to the details of a valid PostgreSQL user
7. Create a database in PostgreSQL called `beatnik_dev` and give your PostgreSQL user all permissions on this database
8. Run the development server by calling `python manage.py runserver`
