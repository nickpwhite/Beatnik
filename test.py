#!/usr/bin/python3

# This is a test script to run LinkConverter
from link_converter.LinkConverter import LinkConverter

if __name__ == "__main__":
    linkConverter = LinkConverter()
    links1 = linkConverter.convert_link('https://play.google.com/music/m/Todhdrnwy3w3clgsqttgsbrklqi?t=This_Is_the_Beginning_-_Shakey_Graves')
    links2 = linkConverter.convert_link('https://open.spotify.com/track/0GswbpVTZBVwvE4gZLaX7R')

    print(links1)
    print(links2)
