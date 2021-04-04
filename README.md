# Beatnik

Beatnik is a service that aggregates links for music streaming services given a song or album. It is currently deployed on Heroku at [https://www.beatnikapp.com/](https://www.beatnikapp.com/).

## Supported Services

The currently supported services are listed below:
- Apple Music
- Soundcloud
- Spotify
- Tidal
- Youtube Music

### Deprecated Services
Google Play Music has been sunset by Google and is no longer supported in Beatnik.

## Requirements
- Python >= 3.6.8
- PostgreSQL 10+
- Pipenv

## Setup

Note, this setup is for developing on the project only, to use it go to [https://www.beatnikapp.com](https://www.beatnikapp.com)

1. Clone the repo
2. Run `pipenv install`
3. Register the app with Spotify and set the `SPOTIPY_CLIENT_ID` and `SPOTIPY_CLIENT_SECRET` environment variables according to what you got from Spotify
4. Get API Keys from Apple for Apple Music and set the `APPLE_KEY_ID`, `APPLE_KEY_ISSUER` and `APPLE_KEY` environment variables
5. Set the `TIDAL_USERNAME` and `TIDAL_PASSWORD` environment variables to the details of a tidal account
6. Set the `POSTGRES_USERNAME` and `POSTGRES_PASSWORD` environment variables to the details of a valid PostgreSQL user
7. Create a database in PostgreSQL called `beatnik_dev` and give your PostgreSQL user all permissions on this database
8. Run migrations with `python manage.py migrate`
9. Run the development server by calling `python manage.py runserver`
