import requests
from pprint import pprint
url = "https://tiktok-download-video1.p.rapidapi.com/getVideo"

def tiktok_save(link):
    querystring = {"url":link}
    headers = {
	"X-RapidAPI-Key": "17dbfa8196mshaf581fe25e635b6p198459jsn92d13b8f090d",
	"X-RapidAPI-Host": "tiktok-download-video1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    try:
        result = ("video",response.json()["items"][0]["video_versions"][0]["url"])
    except:
        result = ("rasm yo'q")
    
    return result