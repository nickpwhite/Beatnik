# This is a test script to run LinkConverter
from link_converter.LinkConverter import LinkConverter

if __name__ == "__main__":
    linkConverter = LinkConverter()
    links1 = linkConverter.convert_link('https://play.google.com/music/m/Todhdrnwy3w3clgsqttgsbrklqi?t=This_Is_the_Beginning_-_Shakey_Graves')
    links2 = linkConverter.convert_link('https://open.spotify.com/track/0GswbpVTZBVwvE4gZLaX7R')
    links3 = linkConverter.convert_link('https://open.spotify.com/track/0KDn1UsD2ym34dCT4P9ebj')
    links4 = linkConverter.convert_link('https://open.spotify.com/album/439SsuO2Esw1G67Xuw1HPS')
    links5 = linkConverter.convert_link('https://open.spotify.com/track/2Sm1PY9pcoQzFDL1NJsJj8')

    print(links1)
    print(links2)
    print(links3)
    print(links4)
    print(links5)
