from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json


def load_clubs():
    driver = webdriver.Chrome()
    url = 'https://terplink.umd.edu/organizations'
    driver.get(url)

    # Currently, UMD has 948 clubs, and button displays 10 clubs at a time
    pages = 0

    while pages < 95:
        try:
            load_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Load More']]"))
            )
            load_more_button.click()
            time.sleep(0.15)
            pages += 1
        except:
            print("Reached end of page.")
            break

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')

    # Extract club urls, names, descriptions
    club_urls = soup.find_all(style='display: block; text-decoration: none; margin-bottom: 20px;')
    club_names = soup.find_all(style='font-size: 1.125rem; font-weight: 600; color: rgb(73, 73, 73); padding-left: 0.313rem; text-overflow: initial; margin-top: 0.313rem; overflow: initial; height: initial;')
    club_desc = soup.find_all(class_='DescriptionExcerpt')
    club_images = soup.find_all(style='color: rgb(255, 255, 255); background-color: rgb(188, 188, 188); user-select: none; display: inline-flex; align-items: center; justify-content: center; font-size: 37.5px; border-radius: 50%; height: 75px; width: 75px; position: absolute; top: 9px; left: 13px; margin: 0.5rem; background-size: 55px;')

    #print(club_imgs, 'hi')

    club_urls = ['https://terplink.umd.edu' + url.get('href') for url in club_urls]
    club_names = [name.string.strip() if name.string is not None else "RANDOM-CLUB" for name in club_names]
    club_desc = [desc.string.strip() if desc.string is not None else "RANDOM-DESC" for desc in club_desc]
    #club_imgs = [img.get('src') for img in club_imgs]
    #club_imgs = [[img.get('alt'), img.get('src')] for img in club_imgs]
    club_imgs = {}
    for img in club_images:
        club_imgs[img.get('alt').strip()] = img.get('src')

    clubs = {}
    for i in range(min(len(club_urls), len(club_names), len(club_desc))):
        clubs[club_names[i]] = { 
            'url' : club_urls[i], 
            'desc' : club_desc[i], 
            'img' : "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fclipartix.com%2Fwp-content%2Fuploads%2F2018%2F09%2Fyellow-clipart-2018-16.png&f=1&nofb=1&ipt=9d3484d1173bd3f2f21d9a996820b4864e47c6a70b8924cec28c38fa956db789&ipo=images" if club_names[i] not in club_imgs else club_imgs[club_names[i]]
        }

    # print(json.dumps(clubs, indent=4))
    driver.quit()
    return clubs

# json_data = json.dumps(load_clubs(), indent=4)

# with open('clubs.json', 'w') as file:
#     file.write(json_data)

# print(f"Data saved to clubs.json")

if __name__ == "__main__":

    clubs = load_clubs()
    print('Scraped', len(clubs), 'clubs')
    json_data = json.dumps(clubs, indent=4)
    with open('clubs.json', 'w') as file:
        file.write(json_data)