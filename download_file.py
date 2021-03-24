#https://curl.trillworks.com/ used to convert curl to python request
import requests

cookies = {
    'vuid': 'pl796185310.706076268',
    'player': '',
}

headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Dest': 'iframe',
    'Referer': 'https://realpython.com/',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
}

response_out = requests.get('https://player.vimeo.com/video/519262361', headers=headers,cookies=cookies)
txt= response_out.text
lis= txt.split('"')
for i in range(len(lis)):
    if "vod-progressive.akamaized.net" in lis[i]:
        print(lis[i])
        r=requests.get(lis[i])
        with open("test4.mp4", 'wb') as file:
            file.write(r.content)



