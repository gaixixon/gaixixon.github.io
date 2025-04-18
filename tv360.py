import time, random
import undetected_chromedriver as uc
#import chromedrive as uc

# Define a custom user agent
agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"

opts = uc.ChromeOptions()
opts.binary_location = "/opt/fuck/chrome132/chrome"
opts.add_argument(f"user-agent={agent}")

from selenium.webdriver.chrome.service import Service
#service = Service("/opt/selenium/chromedriver130")
service = Service("/opt/fuck/chromedriver132/chromedriver")

driver = uc.Chrome(service = service, options=opts, headless=True)

urls = [{"channel":"vtv1","tvid":'#EXTINF:-1 tvg-id="vtv1hd"' , "tvurl":"https://tv360.vn/tv/vtv1-hd?ch=2"},
       {"channel":"vtv3","tvid":'#EXTINF:-1 tvg-id="vtv3hd"' , "tvurl":"https://tv360.vn/tv/vtv3-hd?ch=4"},
       {"channel":"vtv2","tvid":'#EXTINF:-1 tvg-id="vtv2hd"' , "tvurl":"https://tv360.vn/tv/vtv2-hd?ch=3"}
       ]

tv_link=''

def find_m3u8(requests):
    # Search for the m3u8 URL in the requests
    for request in requests:
        #print(request)
        if "MHL" in request:
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
        time.sleep(random.randint(1, 3)) 
        global tv_link
        driver.get(link)
        i=0
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
    time.sleep(random.randint(1, 5))    #sleep to avoid bot detect

driver.quit()

with open('iptv.json','w') as f:
    f.write('[' + tv_link + '{"channel":"test", "link":"http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"}]')
    f.close()
