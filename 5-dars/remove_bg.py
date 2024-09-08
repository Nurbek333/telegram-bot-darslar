import requests


def removebg(FILE_NAME):
    rasm=''
    API_KEY ='JUYsXt9937U2gdSsxQ2ky7HH'


    response = requests.post(
    'https://api.remove.bg/v1.0/removebg',
    data={
        'image_url': FILE_NAME,
        'size': 'auto',
        #'bg_image_url':'image/url'
    },
    files = {
        #'bg_image_file':open("background.jpg","rb"),
    },
    headers={'X-Api-Key': API_KEY},
)
    if response.status_code == requests.codes.ok:
      
        rasm = response.content
    else:
        print("Error:", response.status_code, response.text)
    return rasm