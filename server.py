#  coding: utf-8
import SocketServer

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):

    def handle(self):
        path = "www"

        self.data = self.request.recv(1024).strip()
        if not self.data:
            return
        print("Got a request of: %s\n" % self.data)

        parts = self.data.split('\r\n')
        request = parts[0].split()
        path += request[1]

        if path.endswith('/'):
            path += "index.html"
        else:
            temppath = path + "/index.html"
            try:
                tempfile = open(temppath)
                self.request.send("HTTP/1.1 301 Moved Permanently\r\n")
                self.request.send("Location: " + request[1] + "/\r\n")
                tempfile.close()
                return
            except:
                pass

        try:
            tfile = open(path)
            self.request.send("HTTP/1.1 200 OK\r\n")

            if path.endswith('css'):
                self.request.send("Content-Type: text/css\r\n\r\n")
            elif path.endswith('html'):
                self.request.send("Content-Type: text/html\r\n\r\n")

            for line in tfile.readlines():
                self.request.send(line)

            tfile.close()
        except:
            self.request.send("HTTP/1.1 404 Not Found\r\n\r\n")
            self.request.send("404 Not Found")


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
