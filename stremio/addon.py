import os, requests
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs, unquote
import ssl
import random
import time, json, datetime
from selenium import webdriver
import threading

from getMovieStream import get_movie_stream

##############

# Enable logging
log_path = '/tmp/stremio.log'
logging.basicConfig(filename = log_path, 
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s"
                    )

#ongoing_requests = {}
#lock = threading.Lock()



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

            if data["action"] == "getstream":
                print(f"Start geting stream on request for: {data['url']}\r\n################\r\n\r\n")
                STREAM = get_movie_stream(data["url"])
                self.content = json.dumps({"gxx":200, "info":"Link is ok", "url":STREAM}).encode('utf-8')
                self._set_response()
             
   
            #self.content = json.dumps(stream).encode('utf-8')
            #self._set_response()

        except Exception as e:
            #self.send_error(404, "VCL: " + self.path)
            print(e)
            self.content = json.dumps({"gxx":"6969", "info":"Lỗi getlink"}).encode('utf-8')
            self._set_response()

    def do_GET(self):
        self.send_error(404, "VCL: " + self.path)

def run(server_class=HTTPServer, handler_class=StremioHandler, port=443):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    httpd.socket = ssl.wrap_socket (httpd.socket, keyfile="/etc/letsencrypt/live/baophuc.net/privkey.pem", certfile='/etc/letsencrypt/live/baophuc.net/fullchain.pem',server_side=True)

    logging.info("Starting Stremio addon server on port %s...", port)
    httpd.serve_forever()

if __name__ == "__main__":
    while True:
        try:
            run()
        except Exception as e:
            logging.info(f"Server crashsssssssssssssssssssssssssssss {e}")
            logging.exception("Server crash")
            time.sleep(5)
            run()
