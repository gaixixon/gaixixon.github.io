import json
import time, random
import requests
from urllib.parse import quote

############ selelinum init section
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

        
def search_catalog(url):    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
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
    
    
    driver.get(url)
    movie = []
    try:  #phim đề cử                           
        elems = driver.find_elements("xpath",'''/html/body/div[4]/div/main/section/div[2]/article''')
                                                 
        for el in elems:
            title = el.find_element("xpath",'''.//div/a''').get_attribute('title')            
            href = el.find_element("xpath",'''.//div/a''').get_attribute('href')
            poster = el.find_element("xpath",'''.//div/a/figure/img''').get_attribute("src")
            
            movie.append({"CATALOGS":"gxx.top-xem-nhieu","URL":href,"TITLE":title,"POSTER":poster})
            
    except Exception as e:
        movie.append({"CATALOGS":"gxx.phim-de-cu", "ERROR":"Lỗi lấy phim đề cử"})
        
    #done scraping...
    driver.quit()     
    
    print("Finished getting data from: ", url,"\r\nThe result is: \r\n")
    print(movie)
    
    link = 'https://script.google.com/macros/s/AKfycbw8HZ8DgynbY8KW2e0pGMHRWwzs0nphV_ZFZwUoL_I2njlSNoal7YXfDk-wZkYCANKz/exec'
    savecatalog = requests.post(link, json={"action":"savecatalog","data":movie})

    '''
    var metas = [{
                "id":"id",
                "name":"name",
                "poster":"",
                "type":"Phim mới",
                "catalogs":"Phim lẻ",
                "genres":["Tình cảm","Mạo hiểm","19-"]
                }]'''
    metas = {"metas": []}
    for item in movie:
        metas["metas"].append({"id":item["URL"], "name":item["TITLE"], "poster":item["POSTER"], "type":"Phim mới", "catalogs":"Top xem nhiều", "genres":["Tình cảm","Mạo hiểm","19-"]})
    return metas
    
if __name__ == "__main__":
    print('Search movie')
    movies_metas = search_catalog('https://phimmoichill.sale/search/cu%E1%BB%99c+t%C3%ACnh')

    #input('enternow')
