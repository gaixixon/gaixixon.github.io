import json
import time, random
import requests
from urllib.parse import quote

############ selelinum init section
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

        
def get_movie_catalog(cat=''):    
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
    
    print("getMovieCatalog.py run\r\nRequested id: ",cat)
    
    if cat == '':
        url = 'https://phimmoichill.sale'
        
    print("Getting movies from this url: ", url)
    driver.get(url)
    movie = []
    try:  #phim đề cử                           
        elems = driver.find_elements("xpath",'''/html/body/div[4]/div/div[2]/div/div[2]/div[1]/div/div''')
                                                 
        for el in elems:
            title = el.find_element("xpath",'''.//article/div/a''').get_attribute('title')            
            href = el.find_element("xpath",'''.//article/div/a''').get_attribute('href')
            poster = el.find_element("xpath",'''.//article/div/a/figure/img''').get_attribute("src")
            
            movie.append({"CATALOGS":"gxx.phim-de-cu","URL":href,"TITLE":title,"POSTER":poster})
            
    except Exception as e:
        movie.append({"CATALOGS":"gxx.phim-de-cu", "ERROR":"Lỗi lấy phim đề cử"})
        
    try:  #phim chiếu rạp                     
        elems = driver.find_elements("xpath",'''/html/body/div[4]/div/main/div[1]/div[2]/div[1]/div/div''')
        for el in elems:
            title = el.find_element("xpath",'''.//article/div/a''').get_attribute('title')
            href = el.find_element("xpath",'''.//article/div/a''').get_attribute('href')
            poster = el.find_element("xpath",'''.//article/div/a/figure/img''').get_attribute("src")
            if 'http' not in poster: poster = ""
            
            movie.append({"CATALOGS":"gxx.phim-chieu-rap","URL":href,"TITLE":title,"POSTER":poster})
  
    except Exception as e:
        movie.append({"CATALOGS":"gxx.phim-chieu-rap", "ERROR":"Lỗi lấy phim chiếu rạp"})

    try:  #phim bộ mới
        elems = driver.find_elements("xpath",'''/html/body/div[4]/div/main/section[1]/div[3]/article''')
        for el in elems:
            title = el.find_element("xpath",'''.//div/a''').get_attribute('title')
            href = el.find_element("xpath",'''.//div/a''').get_attribute('href')
            poster = el.find_element("xpath",'''.//div/a/figure/img''').get_attribute("src")
            if 'http' not in poster: poster = ""
            movie.append({"CATALOGS":"gxx.phim-bo-moi","URL":href,"TITLE":title,"POSTER":poster})
                
    except Exception as e:
        movie.append({"CATALOGS":"gxx.phim-bo-moi", "ERROR":"Lỗi lấy phim bộ mới"})
        

    try:  #phim lẻ mới
        elems = driver.find_elements("xpath",'''/html/body/div[4]/div/main/section[2]/div[3]/article''')
        for el in elems:
            title = el.find_element("xpath",'''.//div/a''').get_attribute('title')
            href = el.find_element("xpath",'''.//div/a''').get_attribute('href')
            poster = el.find_element("xpath",'''.//div/a/figure/img''').get_attribute("src")
            if 'http' not in poster: poster = ""
            movie.append({"CATALOGS":"gxx.phim-le-moi","URL":href,"TITLE":title,"POSTER":poster})
                
    except Exception as e:
        movie.append({"CATALOGS":"gxx.phim-le-moi", "ERROR":"Lỗi lấy phim lẻ mới"})
        
    try:  #trending
        elems = driver.find_elements("xpath",'''/html/body/div[4]/div/aside/div[1]/section/div/div[2]/div''')
        for el in elems:
            title = el.find_element("xpath",'''.//a''').get_attribute('title')
            href = el.find_element("xpath",'''.//a''').get_attribute('href')
            poster = el.find_element("xpath",'''.//a/div/img''').get_attribute("src")
            if 'http' not in poster: poster = ""
            movie.append({"CATALOGS":"gxx.trending","URL":href,"TITLE":title,"POSTER":poster})
                
    except Exception as e:
        movie.append({"CATALOGS":"gxx.trending", "ERROR":"Lỗi lấy phim trending"})
        
    try:  #top xem nhiều
        elems = driver.find_elements("xpath",'''/html/body/div[4]/div/aside/div[2]/section/div/div/div''')
        for el in elems:
            title = el.find_element("xpath",'''.//a''').get_attribute('title')
            href = el.find_element("xpath",'''.//a''').get_attribute('href')
            poster = el.find_element("xpath",'''.//a/div/img''').get_attribute("src")
            if 'http' not in poster: poster = ""
            movie.append({"CATALOGS":"gxx.top-xem-nhieu","URL":href,"TITLE":title,"POSTER":poster})
                
    except Exception as e:
        movie.append({"CATALOGS":"gxx.top-xem-nhieu", "ERROR":"Lỗi lấy phim xem nhiều"})
        
    #done scraping...
     
    #input('''Enter to exit''')  #this is to keep browser from being closed
    print("Finished getting data from: ", url,"\r\nThe result is: \r\n")
    driver.quit()
    return movie
    
if __name__ == "__main__":
    movies_metas = get_movie_catalog()
    url = 'https://script.google.com/macros/s/AKfycbw8HZ8DgynbY8KW2e0pGMHRWwzs0nphV_ZFZwUoL_I2njlSNoal7YXfDk-wZkYCANKz/exec'
    
    response = requests.post(url, json={"action":"savecatalog","data":movies_metas})
    print(movies_metas)
