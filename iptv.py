# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time, json, datetime
import urllib.parse
import logging
logging.basicConfig(filename='/tmp/pyserver.log', level=logging.DEBUG,
                    encoding="utf-8",
                    filemode="a",
                    format="{asctime} - {levelname} - {message}",
                    style="{",
                    datefmt="%Y-%m-%d %H:%M",
                    )

hostName = "0.0.0.0"
serverPort = 8888

try:
    with open('iptv.json','r') as f:
        iptv_list = json.load(f)
        f.close()
    logging.debug('read iptv file ok')    
except Exception as e:
    logging.debug('red iptv file failed')

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        #self.process_request()
        
        try:
            params = urllib.parse.parse_qs(self.path.split('?')[1])
            for item in iptv_list:
                if item['channel'] == params['channel'][0]:
                    # Redirect to another location (e.g., http://example.com)
                    self.send_response(302, 'Found')  # Use 302 for temporary redirection
                    self.send_header('Location', item['link'])
                    self.end_headers()
                    break
            self.send_error(403, "Forbidden")
            logging.debug('ok %s', params)
            return
        except Exception as e:
            #self.send_error(403,"I don't know")
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"You requested: \n")
            self.wfile.write(bytes(self.path + "\n","utf-8"))
            logging.debug('lỗi không thấy kênh: %s', e)
            return


    #def do_POST(self):
        #self.process_request()

    def process_request(self):

        # Parse the query string parameters (for GET requests)
        if self.path.split('?')[1]:
            params = urllib.parse.parse_qs(self.path.split('?')[1])
        else:
            # Handle POST requests (read the request body)
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            params = urllib.parse.parse_qs(post_data)


        # Process the parameters and generate the response
        if params:
            response_body = "You requested parameters: " + str(params) + "\r"
            for key, value in params.items():
                response_body += f"key: {key} => value: {value[0]}; "
            #response_body = response_body[:-2]  # Remove the trailing semicolon and space
        else:
            response_body = "Hello!"

        # Set the response headers
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Send the response body
        self.wfile.write(bytes(response_body, 'utf-8'))
        self.wfile.write(bytes("<h1>aa</h1>","utf-8"))



if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    #print("Server started http://%s:%s" % (hostName, serverPort))
    logging.debug("Server started on http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except Exception as e:
        logging.error("server die: " , exc_info=True)
        logging.debug("Lỗi: %s", e)
    #except KeyboardInterrupt:
        #pass

    #webServer.server_close()
    #print("Server stopped.")
