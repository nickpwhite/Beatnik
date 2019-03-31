# Beatnik
Beatnik is a service that aggregates links for music streaming services given a song, album, or artist. It is currently deployed on Heroku at [https://www.beatnikapp.com/](https://www.beatnikapp.com/)

## apple_music_api
An API client for the Apple Music API which implements only the basic functionality necessary (getting data for a song/album given a link and search).

## beatnik
Contains the Django files that comprise the models and views, as well as URL routing logic and application settings.

## link_converter
This python package contains the functionality for getting a list of links to a given song or album given a link to it on one service

### LinkConverter
The link converter will accept a link to a song or album on a streaming service as input and produce links to a matching song on all supported streaming services as output.

### LinkParser
The link parser will accept a link to a song or album as input, parse the link, and produce information in the form `(type, title, artist)` where `type` is one of `track` or `artist`.

## tests
Unit tests, run them with `python manage.py test`

## Supported Services
The currently supported services are listed below:
* Apple Music
* Google Play Music
* Soundcloud
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
