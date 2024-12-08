from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl
import time, json, datetime
import urllib.parse


class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_header('Content-Type', 'text/html; charset=utf-8')

    def do_GET(self):
        if '?channel=' not in self.path:
            self.send_response(400)
            self._set_headers()
            self.end_headers()
            self.wfile.write('Lỗi'.encode('utf-8'))
        else:
            self.processGET() 
 
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        self.wfile.write(response.getvalue())

    def processGET(self):
        params = urllib.parse.parse_qs(self.path.split('?')[1])
        try:
            with open('/home/ec2-user/iptv/iptv.json','r') as f:
                iptv_list = json.load(f)
                f.close()

            for item in iptv_list:
                if item['channel'] == params['channel'][0]:
                    self.send_response(302)
                    self.send_header('Location' , item['link'])
                    self.end_headers()

            self.send_response(402)
            self._set_headers()
            self.end_headers()
            self.wfile.write('Không tìm thấy kênh'.encode('utf-8'))


        except Exception as e:
            self.send_response(500)
            self._set_headers()
            self.end_headers()
            self.wfile.write('Không biết lỗi gì'.encode('utf-8'))

httpd = HTTPServer(('0.0.0.0', 443), RequestHandler)

httpd.socket = ssl.wrap_socket (httpd.socket, 
        keyfile="/etc/letsencrypt/live/baophuc.net/privkey.pem", 
        certfile='/etc/letsencrypt/live/baophuc.net/fullchain.pem',
        #keyfile="cert.pem",
        #certfile="key.pem",
        server_side=True)

print ('server run at https:443')
httpd.serve_forever()
