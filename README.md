# Beatnik

Beatnik is a service that aggregates links for music streaming services given a song or album. It is
currently deployed on Heroku at [https://www.beatnikapp.com/](https://www.beatnikapp.com/).

## Supported Services

The currently supported services are listed below:
- Apple Music
- Google Play Music
- Soundcloud
- Spotify
- Tidal

## Requirements
- Python >= 3.6.8
- PostgreSQL 10
- Pip

## Setup

Note, this setup is for developing on the project only, to use it go to
[https://www.beatnikapp.com](https://www.beatnikapp.com)

1. Clone the repo
2. Setup a python virtual environment
3. Run `pip install -r requirements.txt`
4. Register the app with Spotify and set the `SPOTIPY_CLIENT_ID` and `SPOTIPY_CLIENT_SECRET`
environment variables according to what you got from Spotify
5. Set the `GPM_USERNAME` and `GPM_PASSWORD` environment variables to valid Google Account details
with a paid Google Play Music subscription, note that for accounts with 2fa enabled you need an app
password
6. Get API Keys from Apple for Apple Music and set the `APPLE_KEY_ID`, `APPLE_KEY_ISSUER` and
`APPLE_KEY` environment variables
7. Set the `TIDAL_USERNAME` and `TIDAL_PASSWORD` environment variables to the details of a tidal
   account
8. Set the `POSTGRES_USERNAME` and `POSTGRES_PASSWORD` environment variables to the details of a
valid PostgreSQL user
9. Create a database in PostgreSQL called `beatnik_dev` and give your PostgreSQL user all
permissions on this database
10. Run migrations with `python manage.py migrate`
11. Run the development server by calling `python manage.py runserver`
