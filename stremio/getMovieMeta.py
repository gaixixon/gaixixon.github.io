def get_movie_meta(url):
    #from bs4 import BeautifulSoup
    from urllib.parse import quote, unquote
    import json
    import time, random

    ############ selelinum init section
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

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
    
    #url = unquote(url) #already unquote in main app
    print('Start getting meta for ',url)
    driver.get(url)
    
    #html_source = driver.page_source   #html_source = driver.execute_script("return document.body.innerHTML;")
    #BeautifulSoup = BeautifulSoup(html_source, 'html.parser')
    
    meta = {
        "meta": {
            "id": "BigBuckBunny",
            "name": "Big Buck Bunny",
            "type": "Phim Cũ",
            "poster": "https://image.tmdb.org/t/p/w600_and_h900_bestv2/uVEFQvFMMsg4e6yb03xOfVsDz4o.jpg",
            "videos": [],
            "posterShape": "regular",
            "logo": "https://fanart.tv/fanart/movies/10378/hdmovielogo/big-buck-bunny-5054df8a36bfa.png",
            "background": "https://image.tmdb.org/t/p/original/aHLST0g8sOE1ixCxRDgM35SKwwp.jpg",
            "year": 2008,
            "isFree": True
      }
    }
     
    elem = driver.find_element("xpath",'''/html/body/div[4]/div/main/section[1]/div/div[1]/div''')
    meta["meta"]["id"] = url
    meta["meta"]["name"] = elem.find_element('xpath','.//div[2]/div/h1').text
    meta["meta"]["type"] = "Phim Cũ"
    meta["meta"]["poster"] = driver.find_element('xpath','//*[@id="content"]/div/div[1]/div/div[1]/img').get_attribute('src')
    meta["meta"]["background"] = driver.find_element('xpath','//*[@id="content"]/div/div[1]/div/div[1]/img').get_attribute('src')
    meta["meta"]["logo"] = driver.find_element('xpath','//*[@id="content"]/div/div[1]/div/div[1]/img').get_attribute('src')

    ### now episodes...
    elems = driver.find_elements("xpath",'''//*[@id="listsv-1"]/li''')
    
    ep=0
    for el in elems:
        vid = el.find_element("xpath", '''.//a''').get_attribute("href")
        vtitle = "Tập " + el.find_element("xpath", '''.//a''').get_attribute("title")
        ep+=1
        meta["meta"]["videos"].append({"id":vid , "title":vtitle , "thumbnail": meta["meta"]["poster"], "season":1 , "episode" : ep})
        
    print(meta) 
    #input('''Enter to exit''')  #this is to keep browser from being closed
    driver.quit()
    return meta

    
if __name__ == "__main__":
    url = 'https://phimmoichill.io/info/chua-te-cua-nhung-chiec-nhan-nhung-chiec-nhan-quyen-nang-phan-2-c1-pm16201'
    movies_meta = get_movie_meta(url)
    print(movies_meta)
