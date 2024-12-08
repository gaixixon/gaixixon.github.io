def get_movie_stream(url):
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
    ###############################3333333

    #driver.set_window_position(0, 0)
    #driver.maximize_window()
    #url = unquote(url)  #unquoted from main app
    print ('Start getting stream link for :',url)
    
    driver.get(url)
    bot = driver.execute_script("""window.scroll(50,190)""")
    top = driver.execute_script("""window.scroll(90,0)""")
    mid = driver.execute_script("""window.scroll(10,600)""")
    '''
    #html_source = driver.page_source   #html_source = driver.execute_script("return document.body.innerHTML;")
    #BeautifulSoup = BeautifulSoup(html_source, 'html.parser')
    '''
    #el = driver.find_element('xpath','''//li[@id='player-option-1']''')
    #scroll = driver.execute_script("arguments[0].scrollIntoView({behavior:'auto', block:'center'});", el)
    #el.click()
        
    #driver.find_element("xpath" , '''//div[@class="jw-controlbar jw-reset"]''').click()
    #time.sleep(random.randint(4,5))
    #driver.find_element("xpath" , '''//div[@class="jw-skip jw-reset jw-skippable"]''').click()
    #time.sleep(random.randint(4,5))
    #driver.find_element("xpath" , '''//div[@class="jw-skip jw-reset jw-skippable"]''').click()
    #time.sleep(0.5)
    #driver.find_element("xpath" , '''//div[@id="jwplayer"]''').click()
    
    
    streams = {"streams" : []}
    time.sleep(2)
    netlog = driver.execute_script("""var performance = window.performance || window.webkitPerformance || window.msPerformance || window.mozPerformance;if (!performance) {return [];}var entries = performance.getEntriesByType("resource");var urls = [];for (var i = 0; i < entries.length; i++) {urls.push(entries[i].name);}return urls;""")
    i = 0
    for link in netlog:
        if 'm3u8' in link:
            i+=1
            streams["streams"].append ({"title":"Link" + str(i) , "url":link})
            #break
    
    #print(streams) 
    #input('''Enter to exit''')  #this is to keep browser from being closed
    driver.quit()
    return streams

    
if __name__ == "__main__":
    url = 'https://phimmoi.club/xem-phim/dao-hai-tac-one-piece-netflix-tap-1-154103'
    movie_stream = get_movie_stream(url)
    print(movie_stream)
