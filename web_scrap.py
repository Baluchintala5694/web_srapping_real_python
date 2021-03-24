import os
import time

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def go_to_each_course(dir_name, link):
    # driver.get("https://realpython.com/lessons/python-booleans-overview/")
    driver.get(link)
    time.sleep(5)
    # get all list of videos from the courses page
    # list_course_videos = set(driver.find_elements_by_xpath("//a[contains(@href,'/lessons/')]" and "//a[@class='text-muted']"))
    list_course_videos = driver.find_elements_by_xpath("//a[contains(@href,'/lessons/')]")
    print(f"no of videos found under course:{dir_name}:{len(list_course_videos)}")

    for each_video in list_course_videos:
        time.sleep(5)
        video_link = str(each_video.get_attribute("href"))
        # filename= https://realpython.com/lessons/python-booleans-overview/
        file_name = video_link.split('/')[-2]
        print(video_link, file_name)
        each_video.click()
        wait = WebDriverWait(driver, 20)
        wait.until(expected_conditions.presence_of_element_located((By.TAG_NAME, 'iframe')))
        video_link_id = driver.find_element_by_tag_name("iframe").get_attribute("src")
        link_to_down = process_request(video_link_id)
        # print(video_link_id)
        # https://player.vimeo.com/video/519262361?autoplay=1&quality=auto
        file_path = str(dir_name.strip() + "/" + file_name.strip() + ".mp4")
        print(file_path)
        time.sleep(5)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        file = requests.get(link_to_down)
        with open(file_path, 'wb') as fn:
            fn.write(file.content)
        time.sleep(10)


# video link: https://player.vimeo.com/video/519262361
# file path should be /lesssons/<course_name>/video name
def process_request(video_link):
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

    # response_out = requests.get('https://player.vimeo.com/video/519262361', headers=headers, cookies=cookies)
    response_out = requests.get(video_link, headers=headers, cookies=cookies)

    txt = response_out.text
    lis = txt.split('"')
    for i in range(len(lis)):
        if "vod-progressive.akamaized.net" in lis[i]:
            print("mp4 file link got is:", str(lis[i]))
            return lis[i]  # search the first link to download video and return the link.


############################START of SCRIPT################################
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()
driver.implicitly_wait(10)
####login to site
driver.get("https://realpython.com/")
driver.find_element_by_link_text("Sign‑In").click()
driver.find_element_by_name("login").send_keys("potipireddisrikanth@gmail.com")
driver.find_element_by_name("password").send_keys("srikanth2310")
driver.find_element_by_name("jsSubmitButton").click()

# goto courses page to get list of courses.
driver.get("https://realpython.com/courses/")
course = "//div[@class='card-body d-flex flex-column']"
get_courses_list = driver.find_elements_by_xpath(course)
total_courses = len(get_courses_list)
print(f"Total no of courses found:{total_courses}")
map_courses = {}

# load all courses names and links to dictionary.
for i in get_courses_list:
    time.sleep(5)
    course_name = i.find_element_by_tag_name("h2").text
    course_dir_name = str(course_name.split(':')[0]).replace(" ", "_")
    course_link = i.find_element_by_tag_name("a").get_attribute("href")
    map_courses[course_dir_name] = course_link
    # output of map_course: Records_and_Sets https://realpython.com/courses/records-sets-ideal-data-structure/
    break

print("Done with loading courses to hash map ")
print(map_courses)

# now iterate over the hash and goto each course,

for dir_name, link in map_courses.items():
    go_to_each_course(dir_name, link)

driver.close()
