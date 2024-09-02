import time, random
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# Define a custom user agent
agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"

opts = uc.ChromeOptions()
opts.add_argument(f"user-agent={agent}")

driver = uc.Chrome(options=opts, headless=True)

urls = [{"channel":"cspan","tvid":'#EXTINF:-1 tvg-id="vtv1hd"' , "tvurl":"https://thetvapp.to/tv/cspan-live-stream/"}
       ]

tv_link=''

def find_m3u8(requests):
    # Search for the m3u8 URL in the requests
    for request in requests:
        print(request)
        if "m3u8" in request:
            return request
    return None

def get_m3u8_requests():
    try:
        # Execute JavaScript to capture network requests
        requests = driver.execute_script("""
            var performance = window.performance || window.webkitPerformance || window.msPerformance || window.mozPerformance;
            if (!performance) {
                return [];
            }
            var entries = performance.getEntriesByType("resource");
            var urls = [];
            for (var i = 0; i < entries.length; i++) {
                urls.push(entries[i].name);
            }
            return urls;
        """)
        #print('raw request')
        #print(requests)
        return requests
    except Exception as e:
        print("An error occurred:", e)
        return None
    finally:
        print("")

def gettv(channel , link):
    try:
        print('start to get tv channel ' + channel)
        global tv_link
        driver.maximize_window()
        driver.get(link)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[id='loadVideoBtn']"))).click()
        driver.save_screenshot("search.png")

        i=99
        while i<100:
            i+=1
            # Call the function to get GET requests
            m3u8_requests = get_m3u8_requests()
   
            # Extract the desired URL
            if m3u8_requests:
                m3u8_found = find_m3u8(m3u8_requests)
                if m3u8_found:
                    print("m3u8 link found: ", m3u8_found)
                    tv_link+='{"channel":"' + channel + '","link":"' + m3u8_found + '"},'
                    break
                else:
                    print(".m3u8 not found.. keep trying..")
            else:
                print("No GET requests found.")
                break

    except Exception as e:
        print("Error: " , e)
    finally:
        print('') #driver.quit() should only be used once, on exit the app

for url in urls:
    gettv(url["channel"] , url["tvurl"])
    time.sleep(random.randint(1, 15))    #sleep to avoid bot detect

driver.quit()

with open('theTVapp.json','w') as f:
    f.write('[' + tv_link + '{"channel":"test", "link":"http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"}]')
