import http.server
import json
import socketserver
import os
import re

IP_NUMBER = '127.0.0.1'
PORT_NUMBER = 8080


class MyRequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        # Redirects to main page
        if self.path == '/':
            self.path = '/Wall-E/index.html'
        elif self.path.find('/Wall-E/order.html') != -1:

            self.path

        # Response to order.html http request
        elif self.path.find('/info') != -1:
            # Get chair name from url param
            split_by_q = self.path.split("?")
            param_str = split_by_q[1]

            parameters = param_str.split("&")
            pname = parameters[0]
            chairType = parameters[1]

            data = ""

            self.send_response(200)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            self.wfile.write(bytes(data, "utf-8"))
            return None
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        print("YEP")
        content_type = self.headers['content-type']
        if not content_type:
            return (False, "Content-Type header doesn't contain boundary")
        boundary = content_type.split("=")[1].encode()
        if boundary.decode('utf-8') == 'UTF-8':
            # We got one of the predefined mazes
            print("HER")
            content_len = int(self.headers['Content-Length'])
            post_body = self.rfile.read(content_len)

            post_string = post_body.decode('utf-8')
            parameters = post_string.split("&")
            mazeUrl = parameters[0].split("=")[1]
            print(mazeUrl)
        else:
            # We got a custom csv
            r, info, path = self.deal_post_data(boundary)
            print(r, info, path)
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def deal_post_data(self, boundary):
        
        remainbytes = int(self.headers['content-length'])
        line = self.rfile.readline()
        remainbytes -= len(line)
        print(line)
        if not boundary in line:
            return (False, "Content NOT begin with boundary")
        line = self.rfile.readline()
        remainbytes -= len(line)
        fn = re.findall(r'Content-Disposition.*name="file"; filename="(.*)"', line.decode())
        if not fn:
            return (False, "Can't find out file name...")
        path = self.translate_path(self.path)
        fn = os.path.join(path, fn[0])
        line = self.rfile.readline()
        remainbytes -= len(line)
        line = self.rfile.readline()
        remainbytes -= len(line)
        try:
            out = open(fn, 'wb')
        except IOError:
            return (False, "Can't create file to write, do you have permission to write?")
                
        preline = self.rfile.readline()
        remainbytes -= len(preline)
        while remainbytes > 0:
            line = self.rfile.readline()
            remainbytes -= len(line)
            if boundary in line:
                preline = preline[0:-1]
                if preline.endswith(b'\r'):
                    preline = preline[0:-1]
                out.write(preline)
                out.close()
                return (True, "Upload success!", "%s" % fn)
            else:
                out.write(preline)
                preline = line
        return (False, "Unexpect Ends of data.")

        


Handler = MyRequestHandler
# Set server to localhost and port 8080
server = socketserver.TCPServer((IP_NUMBER, PORT_NUMBER), Handler)

try:
    server.serve_forever()
except KeyboardInterrupt:
    pass
server.server_close()
