# this is main script
import json
import os
import pickle
import time

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def take_screen_shot(name):
    screen_shot_name = name + "/" + name + ".png"
    if os.path.exists(screen_shot_name):
        print(f"\tSKIPPING the {screen_shot_name} as already downloaded")
    else:
        S = lambda X: driver.execute_script('return document.body.parentNode.scroll' + X)
        driver.set_window_size(S('Width'), S('Height'))
        driver.find_element_by_tag_name('body').screenshot(screen_shot_name)
        print(f"\tStep1: took screnshot :{screen_shot_name}")


# video link: https://player.vimeo.com/video/519262361
# file path should be /lesssons/<course_name>/video name
def process_request(video_link, file_name_path):
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

    if "https://player.vimeo.com" not in video_link:
        return f"ERROR: with {video_link},{file_name_path}"
    else:
        try:
            response_out = requests.get(video_link, headers=headers, cookies=cookies)
            txt = response_out.text
            lis = txt.split('"')
            for i in range(len(lis)):
                if "vod-progressive.akamaized.net" in lis[i]:
                    print("\tmp4 file link got is:", str(lis[i]))
                    return lis[i]
                # search the first link to download video and return the link.
        except Exception as e:
            print(f"\tprocess_request: Got Exception{e} with video course:{file_name_path} and link is:{video_link}")


def download(path, pod_link):
    # for path,lnk in link_to_down_map.items():
    if os.path.exists(path):
        return f"\tSKIPPING the {path} as already downloaded"
    else:
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            file = requests.get(pod_link)
            with open(path, 'wb') as fn:
                fn.write(file.content)
            return f"\tDone with file download:{path}"
        except Exception as e:
            print(f"\tDownload: Got Exception{e} with course:{path} and link got is{pod_link}")

############################START of SCRIPT################################
options = webdriver.ChromeOptions()
options.add_argument("--window-size=1920,1080")
options.add_argument("--start-maximized")
options.add_argument("--disable-gpu")
options.add_argument('--headless')
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.maximize_window()
driver.implicitly_wait(10)
driver.set_page_load_timeout(10)
driver.get("https://realpython.com/")
driver.find_element_by_link_text("Sign‑In").click()
driver.find_element_by_name("login").send_keys("potipireddisrikanth@gmail.com")
driver.find_element_by_name("password").send_keys("srikanth2310")
driver.find_element_by_name("jsSubmitButton").click()
driver.get("https://realpython.com/courses/")
get_courses_list = driver.find_elements_by_xpath("//h2/a")
total_courses = len(get_courses_list)
print(f"Total no of courses found:{total_courses}")
map_courses = {}
pre_courses = []

# load previous done courses
if os.stat("to_download.txt").st_size != 0:
    with open("to_download.txt", '+r') as rd:
        previous = json.loads(rd.read())
else:
    print("to_download.txt is Empty")
    previous = {}
# link_to_down_map=previous.copy()

for i in previous.keys():
    pre_courses.append(i.split('/')[0])

for i in get_courses_list:
    course_name = i.text
    course_dir_name = str(course_name.split(':')[0]).replace(" ", "_")
    course_link = i.get_attribute("href")
    if course_dir_name in pre_courses:
        print(f"Skipping to load the course:{course_dir_name}")
        continue
    else:
        map_courses[course_dir_name] = course_link
    print("loading courses wait.....")
print("Done with loading all courses....writing to file courses_links.txt ")

with open("courses_links.txt", 'w') as write_links:
    write_links.write(json.dumps(map_courses))

print("Done with loading courses to hash map &wrote to file courses_links.txt ")
# print(map_courses)
remaining=len(map_courses)
try:

    for dir_name, link in map_courses.items():
        print(f"========={dir_name}==========")
        driver.get(link)
        try:
            os.mkdir(dir_name)
        except OSError as error:
            print(f"\t{error}, so not creating new folder")
        take_screen_shot(dir_name)

        list_course_videos = set(driver.find_elements_by_xpath("//p/a[contains(@href,'/lessons/')]"))
        print(f"\t{remaining}.{dir_name}:No of videos found under course:{len(list_course_videos)}")
        map_videos = {}
        for each_video in list_course_videos:
            video_link = str(each_video.get_attribute("href"))
            # time.sleep(2)
            file_name = each_video.text
            if file_name == '':
                file_name = video_link.split('/')[-2]
            map_videos[video_link] = file_name
        print("\t\tStep2: loaded all courses/videos links in hash map", map_videos)
        for v_link, name in map_videos.items():
            driver.get(v_link)
            wait = WebDriverWait(driver, 30)
            wait.until(expected_conditions.presence_of_element_located((By.TAG_NAME, 'iframe')))
            video_link_id = driver.find_element_by_tag_name("iframe").get_attribute("src")
            file_path = str(dir_name.strip() + "/" + name.strip() + ".mp4")
            if os.path.exists(file_path):
                print(f"\t\tSKIPPING the {file_path} as already downloaded")
                continue
            else:
                pod_link = process_request(video_link_id, file_path)
                previous[file_path]=pod_link
                print(download(file_path, pod_link))

        print(f"\t\tStep3:loaded all course/video/video_id link under course link into hashmap{dir_name}")
        remaining -= 1

except Exception as e:
    print(f"error{e}")
finally:
    with open("to_download.txt", "w+") as DV:
        DV.write(json.dumps(previous))

############downloading part############


driver.close()
