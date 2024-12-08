import json
import time, random
from urllib.parse import quote

############ selelinum init section
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def sanitize_string(video):
  try:  
    if video["id"] == None: video["id"] = "blank"
    if video["title"] == None: video["title"] = "Blank title"
    if video["poster"] == None: video["poster"] = "https://humenglish.com/wp-content/uploads/2024/07/Untitled-114.jpg"
    return video
  except Exception as e:
    print(e)
global DATA

def check_and_append(cat_id, item):
    global DATA
    print ("cat: ", cat_id)
    print("item: ",item)
    print ("data: ",DATA)
    input()
    
    if len(item["poster"])<1: item["poster"] = "https://i.imgur.com/hIkqk2V.png"
    
    mached_item = True
    for meta in DATA["catalogs"][item]["metas"]:
        try:
            if meta["id"] == item["id"]:
                mached_item = False
                break
        except: pass
    if mached_item:
        DATA["catalogs"][item]["metas"].append(item)
    
def get_movie_catalog(cat=''):
    global DATA  #access to DATA variable from main append
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--headless");
    options.add_argument("--disable-gpu")
    
    agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    options.add_argument(f"user-agent={agent}")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # HUMAN LIKE IT..
    driver.set_window_position(0, 0)
    driver.maximize_window()
    time.sleep(random.randint(0,1))
    driver.execute_script("""window.scroll(50,190)""")
    driver.execute_script("""window.scroll(90,0)""")
    time.sleep(random.randint(0,1))
    driver.execute_script("""window.scroll(10,600)""")
    ##############################
    
    print("getMovieCatalog.py run\r\nRequested id: ",cat)
    
    if cat != 'dfs':
        url = 'https://phimmoichill.sale'
        
    print("Getting movies from this url: ", url)
    
    driver.get(url)

    #html_source = driver.page_source   #html_source = driver.execute_script("return document.body.innerHTML;")
    #BeautifulSoup = BeautifulSoup(html_source, 'html.parser')
    
    '''metas = {"metas":[
                        {"id":"default",
                        "name":"Default",
                        "poster":"https://humenglish.com/wp-content/uploads/2024/07/Untitled-114.jpg",
                        "type":"Phim Cũ"}
                     ]
            }'''
    metas = []
    
    try:  #phim đề cử
        elems = driver.find_elements("xpath",'''/html/body/div[4]/div/div[2]/div/div[2]/div[1]/div/div''')
                                                 
        for el in elems:
            title = el.find_element("xpath",'''.//article/div/a''').get_attribute('title')            
            href = el.find_element("xpath",'''.//article/div/a''').get_attribute('href')
            poster = el.find_element("xpath",'''.//article/div/a/figure/img''').get_attribute("src")
            
            check_and_append("gxx.phim-de-cu",{"cat":"gxx.phim-de-cu","id":href,"name":title,"poster":poster,"type":"Phim Cũ"})
                
    except Exception as e:
        print(e)
        
    try:  #phim chiếu rạp
        elems = driver.find_elements("xpath",'''/html/body/div[4]/div/main/div[1]/div[2]/div[1]/div/div''')
        for el in elems:
            title = el.find_element("xpath",'''.//article/div/a''').get_attribute('title')
            href = el.find_element("xpath",'''.//article/div/a''').get_attribute('href')
            poster = el.find_element("xpath",'''.//article/div/a/figure/img''').get_attribute("src")
            if 'http' not in poster: poster = ""
            check_and_append("gxx.phim-chieu-rap",{"cat":"gxx.phim-chieu-rap","id":href,"name":title,"poster":poster,"type":"Phim Cũ"})
                
    except Exception as e:
        print(e)

    try:  #phim bộ mới
        elems = driver.find_elements("xpath",'''/html/body/div[4]/div/main/section[1]/div[3]/article''')
        for el in elems:
            title = el.find_element("xpath",'''.//div/a''').get_attribute('title')
            href = el.find_element("xpath",'''.//div/a''').get_attribute('href')
            poster = el.find_element("xpath",'''.//div/a/figure/img''').get_attribute("src")
            if 'http' not in poster: poster = ""
            check_and_append("gxx.phim-bo-moi", {"cat":"gxx.phim-bo-moi","id":href,"name":title,"poster":poster,"type":"Phim Cũ"})
                
    except Exception as e:
        print(e)
        

    try:  #phim lẻ mới
        elems = driver.find_elements("xpath",'''/html/body/div[4]/div/main/section[2]/div[3]/article''')
        for el in elems:
            title = el.find_element("xpath",'''.//div/a''').get_attribute('title')
            href = el.find_element("xpath",'''.//div/a''').get_attribute('href')
            poster = el.find_element("xpath",'''.//div/a/figure/img''').get_attribute("src")
            if 'http' not in poster: poster = ""
            check_and_append("gxx.phim-le-moi", {"cat":"gxx.phim-le-moi","id":href,"name":title,"poster":poster,"type":"Phim Cũ"})
                
    except Exception as e:
        print(e)

    try:  #trending
        elems = driver.find_elements("xpath",'''/html/body/div[4]/div/aside/div[1]/section/div/div[2]/div''')
        for el in elems:
            title = el.find_element("xpath",'''.//a''').get_attribute('title')
            href = el.find_element("xpath",'''.//a''').get_attribute('href')
            poster = el.find_element("xpath",'''.//a/div/img''').get_attribute("src")
            if 'http' not in poster: poster = ""
            check_and_append("gxx.trending", {"cat":"gxx.trending","id":href,"name":title,"poster":poster,"type":"Phim Cũ"})
                
    except Exception as e:
        print(e)
    
    try:  #top xem nhiều
        metas["gxx.top-xem-nhieu"] = {"metas":[]}
        elems = driver.find_elements("xpath",'''/html/body/div[4]/div/aside/div[2]/section/div/div/div''')
        for el in elems:
            title = el.find_element("xpath",'''.//a''').get_attribute('title')
            href = el.find_element("xpath",'''.//a''').get_attribute('href')
            poster = el.find_element("xpath",'''.//a/div/img''').get_attribute("src")
            if 'http' not in poster: poster = ""
            check_and_append("gxx.top-xem-nhieu",  {"cat":"gxx.top-xem-nhieu","id":href,"name":title,"poster":poster,"type":"Phim Cũ"})
                
    except Exception as e:
        print(e)
        
    #done scraping...
    
    #input('''Enter to exit''')  #this is to keep browser from being closed
    print("Finished getting data from: ", url,"\r\nThe result is: \r\n")
    driver.quit()
    return metas

    
if __name__ == "__main__":
    url = 'https://phimmoichill.io'
    movies_metas = get_movie_catalog(url)
    print(movies_metas)
