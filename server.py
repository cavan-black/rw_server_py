from http.server import BaseHTTPRequestHandler, HTTPServer
from os import read
import json
import cgi

hostName = "localhost"
serverPort = 80

class MyServer(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", 'application/json')
        self.end_headers()
        
    def do_GET(self):
        self.do_HEAD()
        f = open('file.json', 'r', encoding='utf-8').read()
        self.wfile.write(bytes(f, "utf-8"))

    def do_POST(self):
        if self.check_content():
            length = int(self.headers.get('content-length'))
            message = json.loads(self.rfile.read(length))
            self.clear_file()
            self.do_HEAD()
            with open('file.json', 'w') as writefile:
                json.dump(message, writefile)
            self.wfile.write(json.dumps(message).encode())
        else:
            return

    def check_content(self) -> bool:
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return False
        else:
            return True

    def clear_file(self):
        with open('file.json', 'w') as clearfile:
            clearfile.write("{}")

if __name__ == "__main__":      
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
