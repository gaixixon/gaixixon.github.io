#https://vip.opstream11.com/20230527/43827_cf599ae8/3000k/hls/mixed.m3u8
import os, requests
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs, unquote
import ssl
import random
import time, json, datetime
from selenium import webdriver
import threading

### phim moi stuff
#from getMovieCatalog import get_movie_catalog
from getMovieMeta import get_movie_meta
from getMovieStream import get_movie_stream
from downloadData import downloadData
from searchCatalog import search_catalog
##############

# Enable logging
logging.basicConfig(level=logging.INFO)

ongoing_requests = {}
lock = threading.Lock()

# Manifest definition
MANIFEST =  {"id": "io.stremio.phimmoi",
             "version": "0.1.16",
             "description": "Phim mới nhất",
             "name": "Phim mới",
             "resources": [ "catalog", "meta" , "stream" ],
             "idPrefixes": ["http" , "gxx"],
             "types": ["Phim mới"],
             "catalogs": [
                         {   "name": "Trending",
                            "id": "gxx.trending",
                            "type": "Phim mới",
                            "extraSupported": ["search"]
                        },
                        {   "name": "Phim đề cử",
                            "id": "gxx.phim-de-cu",
                            "type": "Phim mới",
                            "extraSupported": ["search"]
                        },
                        {   "name": "Phim chiếu rạp",
                            "id": "gxx.phim-chieu-rap",
                            "type": "Phim mới",
                            "extraSupported": ["search"]
                        },
                        {   "name": "Phim bộ mới",
                            "id": "gxx.phim-bo-moi",
                            "type": "Phim mới",
                            "extraSupported": ["search"]
                        },
                        {   "name": "Phim lẻ mới",
                            "id": "gxx.phim-le-moi",
                            "type": "Phim mới",
                            "extraSupported": ["search"]
                        },
                       {   "name": "Top xem nhiều",
                            "id": "gxx.top-xem-nhieu",
                            "type": "Phim mới",
                            "extraSupported": ["search"]
                        }                        
                        ]
             }


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
            print(data["url"])

            if data["action"] == "savecatalog":
                with open('catalog.json', 'w') as file:
                    json.dump(data["data"], file, indent=4)
            elif data["action"] == "savemeta":
                with open('meta.json', 'w') as file:
                    json.dump(data["data"], file, indent=4)
            elif data["action"] == "savestream":
                with open('stream.json', 'w') as file:
                    json.dump(data["data"], file, indent=4)
            elif data["action"] == "getmeta":
                print(f"Start geting meta on request for: {data['url']}\r\n################\r\n\r\n")
                META = get_movie_meta(data["url"])
                self.content = json.dumps(META).encode('utf-8')
                self._set_response()

            elif data["action"] == "getstream":
                print(f"Start geting stream on request for: {data['url']}\r\n################\r\n\r\n")
                STREAM = get_movie_stream(data["url"])
                self.content = json.dumps(STREAM).encode('utf-8')
                self._set_response()
            
            elif data["action"] == "searchcatalog":
                print(f"Start searching..for: {data['url']}\r\n################\r\n\r\n")
                SEARCH = search_catalog(data["url"])
                self.content = json.dumps(SEARCH).encode('utf-8')
                self._set_response()
           
 
   
            #self.content = json.dumps(stream).encode('utf-8')
            #self._set_response()
            self.send_response(200)

        except Exception as e:
            #self.send_error(404, "VCL: " + self.path)
            print(e)

    def do_GET(self):
        client_ip = self.client_address[0]
        print("New request from ",client_ip)
        with lock:
            if client_ip in ongoing_requests:
                self.send_response(429) #too many requests
                self.end_headers()
                self.wfile.write(b"Too many reqeusts")
                return
            else:
                ongoing_requests[client_ip] = True

        print ("Requested parameter:####################\r\n",self.path)
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
            
            #check if the link has been served before or not
            try:
                file_path = '/home/ec2-user/stremio/catalog.json'
                with open(file_path, 'r') as file:
                    content = file.read()
                    data = json.loads(content)
                    if catalog_id in data:
                        print("\r\nFinish getting data locally \r\r\n\n")
                        METAS = data[catalog_id]
            except FileNotFoundError:
                print(f"The file {file_path} was not found.")
            except json.JSONDecodeError:
                print("Error decoding JSON. Please ensure the file contains valid JSON data.")

            self.content = json.dumps(METAS).encode('utf-8')
            self._set_response()
            
            print('\r\nFinish getting catalog from locally')

        # HANDLE META REQUEST
        elif len(path_segments) >= 2 and path_segments[0] == "meta":
            # Extract type and ID (e.g., "movie" and "tt1234567")
            _, content_type, content_id = path_segments[:3]
            content_id = unquote(content_id.replace(".json",""))
            
            META = get_movie_meta(content_id)
            self.content = json.dumps(META).encode('utf-8')
            self._set_response()

        # HANDLE STREAM REQUEST
        elif len(path_segments) >= 2 and path_segments[0] == "stream":
            # Extract type and ID (e.g., "movie" and "tt1234567")
            _, content_type, content_id = path_segments[:3]
            content_id = unquote(content_id.replace(".json",""))
            
            STREAM = get_movie_stream(content_id)
            self.content = json.dumps(STREAM).encode('utf-8')
            self._set_response()
 
        else:
            self.send_error(404, "VCL: " + self.path)
            #downloadData()

        with lock:
            del ongoing_requests[client_ip]
            print("Đã xóa lock")
            downloadData()
            
def run(server_class=HTTPServer, handler_class=StremioHandler, port=443):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    httpd.socket = ssl.wrap_socket (httpd.socket, keyfile="/etc/letsencrypt/live/baophuc.net/privkey.pem", certfile='/etc/letsencrypt/live/baophuc.net/fullchain.pem',server_side=True)

    logging.info("Starting Stremio addon server on port %s...", port)
    httpd.serve_forever()

if __name__ == "__main__":
    run()
