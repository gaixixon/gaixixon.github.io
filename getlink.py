import undetected_chromedriver as uc

# Define a custom user agent
agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"

opts = uc.ChromeOptions()
opts.add_argument(f"user-agent={agent}")

driver = uc.Chrome(options=opts, headless=True)

urls = [{"channel":"vtv1","tvid":'#EXTINF:-1 tvg-id="vtv1hd"' , "tvurl":"https://tv360.vn/tv/vtv1-hd?ch=2"},
       {"channel":"vtv3","tvid":'#EXTINF:-1 tvg-id="vtv3hd"' , "tvurl":"https://tv360.vn/tv/vtv3-hd?ch=4"},
       {"channel":"vtv2","tvid":'#EXTINF:-1 tvg-id="vtv2hd"' , "tvurl":"https://tv360.vn/tv/vtv2-hd?ch=3"}
       ]

tv_link=''

def find_m3u8(requests):
    # Search for the m3u8 URL in the requests
    for request in requests:
        #print(request)
        if "m3u8" in request:
            return request
    return None

def get_get_requests():
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
        #driver.quit()

def gettv(channel , link):
    print('start to get tv channel ' + channel)
    driver.get(link)
    
    while 3>1:
        # Call the function to get GET requests
        get_requests = get_get_requests()

        # Extract the desired URL
        if get_requests:
            global tv_link
            m3u8_found = find_m3u8(get_requests)
            if m3u8_found:
                print("m3u8 link found: ", m3u8_found)
                tvlink+='{"channel":"' + channel + '","link":"' + m3u8_found + '"},'
                break
            else:
                print(".m3u8 not found.. keep trying..")
        else:
            print("No GET requests found.")
            break

for url in urls:
    gettv(url["channel"] , url["tvurl"])

driver.quit()
with open('iptv.json','w') as f:
    f.write('[' + tvlink + '{"channel":"test", "link":"http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"}]')
