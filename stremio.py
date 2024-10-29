from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl
import time, json, datetime
import urllib.parse


def readFile(path):
    with open('/home/ec2-user/stremio/' + path , 'r') as f:
        data = json.load(f)
        f.close()
        return data

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        param = self.path.split('/')
        print('''




              THIS IS YOUR REQUESTED URL:
              ''',param,'''
              ######################''') 
        
        try: catalog = self.path.split('/')[2]
        except Exception: catalog = None 
        try: category = self.path.split('/')[3]
        except Exception: category = None
        try: req = self.path.split('/')[4]
        except: req = None
        tv_list = readFile('iptv_list.json')

        if catalog == 'manifest.json':
            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.send_header('Access-Control-Allow-Origin','*')
            self.send_header('Access-Control-Request-Method','*')
            self.send_header('Access-Control-Allow-Headers','*')
            self.end_headers()
            self.wfile.write(bytes('''{
                "id": "com.stremio.gxx",
                    "version": "0.0.7",
                        "name": "Live IPTV",
                            "description": "Watch live IPTV Add-on",
                                "resources": ["catalog", "meta", "stream"],
                                    "types": ["series"],
                                        "catalogs": [{"type":"series","id": "livetv","name": "LiveTV by gxx",
                                                          "extra": [{ "name": "search", "isRequired": false },
                                                                                      { "name": "genre", "isRequired": false }]
                                                                                                      }]
                                                                                                      }''',"utf-8"))

        elif '/stremio/catalog/' in self.path:
            catalog = {"metas" : []}
            previous_item = ''
            meta = {}
            for item in tv_list:
                if item["group_title"] != previous_item and len(meta)>0 :
                    catalog["metas"].append(meta)
                
                if 1==1:
                    meta = {}
                    meta["id"] = item["group_title"]
                    meta["name"] = item["group_title"]
                    meta["poster"] = item["tvg_logo"]
                    meta["banner"] = item["tvg_logo"]
                    meta["posterShape"] = "regular"
                    meta["type"] = "series"
                    meta["genres"] = [item["group_title"]]
                    previous_item = item["group_title"]
            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.send_header('Access-Control-Allow-Origin','*')
            self.send_header('Access-Control-Allow-Headers','*')
            self.end_headers()
            self.wfile.write(json.dumps(catalog).encode('utf-8'))

        elif '/stremio/meta/' in self.path:
            meta = {}
           
            for item in tv_list:
                if item["group_title"].lower()+".json"  == urllib.parse.unquote(req).lower():
                    if len(meta) == 0:
                        meta["type"] = "series"
                        meta["id"] = item["group_title"]
                        meta["name"] = item["group_title"]
                        meta["poster"] = item["tvg_logo"]
                        meta["videos"] = []
                        meta["genres"] = [item["group_title"]]
            
                    meta["videos"].append({"id":item["title"] , "title":item["title"]})
            meta = {"meta" : meta}
            self.sendOutput(meta)

        elif '/stremio/stream/' in self.path:
            streams = {"streams" : []}
            
            for item in tv_list:
                if item["title"].lower()+".json"  == urllib.parse.unquote(req).lower() :
                    streams["streams"].append({"name":item["title"] , "url": item["link"]})

            self.sendOutput(streams)

        else:
            self.send_error(400)

    def sendOutput(self,data):
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.send_header('Access-Control-Allow-Origin', '*') 
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))


##############################################################
httpd = HTTPServer(('0.0.0.0', 443), RequestHandler)
httpd.socket = ssl.wrap_socket (httpd.socket, 
        keyfile="/etc/letsencrypt/live/baophuc.net/privkey.pem", 
        certfile='/etc/letsencrypt/live/baophuc.net/fullchain.pem',
        #keyfile="cert.pem",
        #certfile="key.pem",
        server_side=True)

print ('server run at https:443')
httpd.serve_forever()
