# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import urllib.parse

hostName = "0.0.0.0"
serverPort = 8888

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        #self.process_request()
        if "?channel=test" in self.path:
            # Redirect to another location (e.g., http://example.com)
            self.send_response(302, 'Found')  # Use 302 for temporary redirection
            self.send_header('Location', 'http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4')
            self.end_headers()
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Nothing!")

    def do_POST(self):
        self.process_request()

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
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
