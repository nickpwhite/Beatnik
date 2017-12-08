import os

from apple_music_api.AppleMusicApi import AppleMusicApi

if __name__ == "__main__":
    appleMusicApi = AppleMusicApi(key_id=os.environ['APPLE_KEY_ID'], issuer=os.environ['APPLE_KEY_ISSUER'], key_filename=os.environ['APPLE_KEY_PATH'])
    response = appleMusicApi.get_album("1265893523")

    print(response['data'][0])

    response2 = appleMusicApi.get_track("900032829")

    print(response2['data'][0])

    response3 = appleMusicApi.search("Project Freedom Joey DeFrancesco", limit=1, types="albums")

    print(response3['results']['albums']['data'][0])
