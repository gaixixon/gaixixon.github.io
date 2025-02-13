#https://vip.opstream11.com/20230527/43827_cf599ae8/3000k/hls/mixed.m3u8
import os, requests
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs, unquote
import ssl
import random
import time, json, datetime
from selenium import webdriver

### phim moi stuff
from getMovieCatalog import get_movie_catalog
from getMovieMeta import get_movie_meta
from getMovieStream import get_movie_stream
##############

# Enable logging
logging.basicConfig(level=logging.INFO)

# Manifest definition

MANIFEST =  {"id": "org.stremio.phimcu",
             "version": "0.1.10",
             "description": "Phim hơi cũ 0.1.10@gxx",
             "name": "Phim cũ",
             "resources": [ "catalog", "meta" , "stream" ],
             "idPrefixes": ["http" , "gxx"],
             "types": ["Phim Cũ"],
             "catalogs": [
                        {   "name": "Phim đề cử",
                            "id": "gxx.phim-de-cu",
                            "type": "Phim Cũ",
                            "extra": [{ "name": "search", "isRequired": False }],
                            "extraSupported": ["search"]
                        },
                        {   "name": "Phim chiếu rạp",
                            "id": "gxx.phim-chieu-rap",
                            "type": "Phim Cũ",
                            "extra": [{ "name": "search", "isRequired": False }],
                            "extraSupported": ["search"]
                        },
                        {   "name": "Phim bộ mới",
                            "id": "gxx.phim-bo-moi",
                            "type": "Phim Cũ",
                            "extra": [{ "name": "search", "isRequired": False }],
                            "extraSupported": ["search"]
                        },
                        {   "name": "Phim lẻ mới",
                            "id": "gxx.phim-le-moi",
                            "type": "Phim Cũ",
                            "extra": [{ "name": "search", "isRequired": False }],
                            "extraSupported": ["search"]
                        },
                        {   "name": "Trending",
                            "id": "gxx.trending",
                            "type": "Phim Cũ",
                            "extra": [{ "name": "search", "isRequired": False }],
                            "extraSupported": ["search"]
                        },
                        {   "name": "Top xem nhiều",
                            "id": "gxx.top-xem-nhieu",
                            "type": "Phim Cũ",
                            "extra": [{ "name": "search", "isRequired": False }],
                            "extraSupported": ["search"]
                        }                        
                        ]
             }
def save_data(data, param1='', param2=''):
    with open('data.json','w') as f:
        if param1 == 'meta':
            DATA["meta"][data["meta"]["id"]] = data
        
        elif param1 == 'catalogs':
            DATA["catalogs"][param2] = data
            
        elif param1 == 'stream':
            try: 
                DATA["stream"][param2] = data
            except: 
                DATA["stream"] = {}
                DATA["stream"][param2] = data
                
        json.dump(DATA,f)
        f.close()

try: 
    with open('data.json', 'r') as f:
        DATA = json.load(f)
        f.close()
except Exception as e:
    DATA = {"catalogs" :{"gxx.phim-de-cu":{},"gxx.phim-chieu-rap":{},"gxx.phim-bo-moi":{},"gxx.phim-le-moi":{},"gxx.trending":{},"gxx.top-xem-nhieu":{}},
            "meta" : {},
            "stream" : {},
            "last_update": (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S.%f")
           }

def check_update():
    #updated_status = DATA["last_update"]["status"]
    try:
        updated_time = DATA["last_update"]
        updated_time = datetime.datetime.strptime(updated_time, "%Y-%m-%d %H:%M:%S.%f")  #convert date-like string to date object
    except:
        updated_time = datetime.datetime.now()
        DATA["last_update"] = updated_time.strftime("%Y-%m-%d %H:%M:%S.%f")
        save_data(DATA)
    
    duration = datetime.datetime.now() - updated_time
    
    if duration >= datetime.timedelta(hours=5):
        print("\r\n***************************************\r\nUpdating.. now \r\n")
        DATA["last_update"] = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S.%f")
        save_data(DATA)

        #get_movie_catalog('gxx.index')              #TAM THO BO DI
        save_data(DATA)

get_movie_catalog() #update once on server start

class StremioHandler(BaseHTTPRequestHandler):
    
    def _set_response(self, content_type="application/json"):
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", len(self.content))
        self.send_header('Access-Control-Allow-Origin','*') 
        self.send_header('Access-Control-Allow-Headers','*')
        #self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        #self.send_header("Pragma", "no-cache")
        #self.send_header("Expires", "0")
        self.end_headers()
        self.wfile.write(self.content)

    def do_POST(self):
      try:
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(post_data)

        if data['cat'] == 'meta':
            print('data received')
            print(data)

            #meta = get_movie_meta(data["url"])
            print('wegot ------------------------------------\r\n\r\n')
            meta = {}
            meta['cat'] = 'meta'
            meta['id'] = 'ufck'
            meta['name'] = 'shit'
            
            print(meta)

            response = requests.post('https://phimcu.gaixixon.workers.dev', json=json.dumps(meta), headers={'Content-Type':'application/json'})  #send data

            print(response.status_code, response.json())

            return

            #self.content = json.dumps(meta).encode('utf-8')
            #self._set_response()

        elif data['cat'] == 'stream':
            stream = get_movie_stream(url)
            stream['cat'] = 'stream'
            requests.post('https://phimcu.gaixixon.workers.dev', data = stream) 
            return

            #self.content = json.dumps(stream).encode('utf-8')
            #self._set_response()

        else:
            self.send_error(404, "VCL: " + self.path)
      except Exception as e:(print(e))


    def do_GET(self):
        print ("Requested parameter:\r\n",self.path)
        # Parse URL path
        parsed_path = urlparse(self.path)
        path_segments = parsed_path.path.strip("/").split("/")
        
        # Handle manifest request
        if parsed_path.path == "/manifest.json":
            self.content = json.dumps(MANIFEST).encode("utf-8")
            self._set_response()
        
        # HANDLE CATALOGS REQUEST
        elif len(path_segments) >= 2 and path_segments[0] == "catalog":
            # Extract type and ID prefix
            _, content_type, catalog_id = path_segments[:3]
            catalog_id = unquote(catalog_id.replace(".json",""))
            
            if "local" == "local":  #get locally saved data
                METAS = DATA["catalogs"][catalog_id]
                print(METAS, "\r\n*******************************************\r\nMetas data LOCALLY retrieved")
                
            else:
                METAS = get_movie_catalog(catalog_id)
                save_data(METAS,"catalogs",catalog_id)
                print(METAS,"\r\n*******************************************\r\nMetas data ONLINE retrieved")
                
            self.content = json.dumps(METAS).encode('utf-8')
            self._set_response()
            
            print('DONE DONE catalog process\r\n')

        # HANDLE META REQUEST
        elif len(path_segments) >= 2 and path_segments[0] == "meta":
            # Extract type and ID (e.g., "movie" and "tt1234567")
            _, content_type, content_id = path_segments[:3]
            content_id = unquote(content_id.replace(".json",""))
            
            #check if content_id existed in database or not
            matched_item = DATA["meta"].get(content_id)
            if matched_item:
                META = matched_item
                print(META)
                print('\r\n*******************************************\r\nAbove meta is retrieved from LOCAL DATABASE')
            else:
                META = get_movie_meta(content_id)
                print(META)
                print('\r\n*******************************************\r\nAbove meta is FRESHLY ONLINE retrieved')
                save_data(META,"meta")
                
            self.content = json.dumps(META).encode('utf-8')
            self._set_response()

            print('DONE DONE meta \r\n')

        # HANDLE STREAM REQUEST
        elif len(path_segments) >= 2 and path_segments[0] == "stream":
            # Extract type and ID (e.g., "movie" and "tt1234567")
            _, content_type, content_id = path_segments[:3]
            content_id = unquote(content_id.replace(".json",""))
            
            #check if STREAM content_id existed in database or not
            try: 
                matched_item = DATA["stream"].get(content_id)
            except: 
                DATA["stream"] = {}
                matched_item = None
                
            if matched_item:
                STREAM = matched_item
                print(STREAM)
                print('\r\n*******************************************\r\nAbove STREAM LINK is retrieved from LOCAL DATABASE')
            else:
                STREAM = get_movie_stream(content_id)
                print(STREAM)
                print('\r\n*******************************************\r\nAbove STREAM is FRESHLY ONLINE retrieved')
                save_data(STREAM,"stream",content_id)
                        
            self.content = json.dumps(STREAM).encode('utf-8')
            self._set_response()

            print('\r\n*******************************************\r\nStart streaming from:')
            print(STREAM)
            print('End stream request!\r\n')
            print('\r\n*******************************************\r\nPeriordicall check and HANDLE DATA UPDATE ON IDLE\r\n')
            check_update()
 
        else:
            self.send_error(404, "VCL: " + self.path)

def run(server_class=HTTPServer, handler_class=StremioHandler, port=443):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    httpd.socket = ssl.wrap_socket (httpd.socket, keyfile="/etc/letsencrypt/live/baophuc.net/privkey.pem", certfile='/etc/letsencrypt/live/baophuc.net/fullchain.pem',server_side=True)

    logging.info("Starting Stremio addon server on port %s...", port)
    httpd.serve_forever()

if __name__ == "__main__":
    run()
