from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#///
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
#from webdriver_manager.chrome import ChromeDriverManager
import time
import json
#///

desired_capabilities = DesiredCapabilities.CHROME
desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

url = 'https://fruitlab.com/video/aTUqTrJrMtj6FgO5?ntp=ggm'

# Set Chrome options
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # To run Chrome in headless mode
options.add_argument("--no-sandbox")
options.add_argument('--disable-dev-shm-usage')
options.add_argument("start-maximized")
options.add_argument("--autoplay-policy=no-user-gesture-required")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--mute-audio")
options.add_argument("--disable-notifications")
options.add_argument("--disable-popup-blocking")
options.add_argument(f'user-agent={desired_capabilities}')
##
options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
##
# Initialize Selenium WebDriver with the service and Chrome options
driver = webdriver.Chrome( options=options)

def get_m3u8_urls(url):
   driver.get(url)
   driver.execute_script("window.scrollTo(0, 10000)")
   time.sleep(20)
   logs = driver.get_log("performance")
   url_list = []

   for log in logs:
       #print(log)
       network_log = json.loads(log["message"])["message"]
       if ("Network.response" in network_log["method"]
           or "Network.request" in network_log["method"]
           or "Network.webSocket" in network_log["method"]):
           if 'request' in network_log["params"]:
               if 'url' in network_log["params"]["request"]:
                   if  'm3u8' in network_log["params"]["request"]["url"] or '.mp4' in network_log["params"]["request"]["url"]:
                       print(network_log["params"]["request"]["url"])
                       url_list.append( network_log["params"]["request"]["url"] )

   driver.close()
   return url_list

if __name__ == "__main__":

   url = "https://fruitlab.com/video/aTUqTrJrMtj6FgO5?ntp=ggm"
   url = "https://tv360.vn/tv/vtv1-hd?ch=2&col=recommend_live&sect=RECOMMEND&page=home"
   url = "https://vtv.vn/truyen-hinh-truc-tuyen/vtv1.htm"
   url_list = get_m3u8_urls(url)
   print:(url_list)
