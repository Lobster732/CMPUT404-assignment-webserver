#  coding: utf-8
import SocketServer
import os

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

# Credit to Thomas Curnow for suggesting using Absoule File paths
# when dealing with backwards navigation security


class MyWebServer(SocketServer.BaseRequestHandler):

    def handle(self):
        path = "www"
        absolutestartpath = os.path.abspath(path)

        self.data = self.request.recv(1024).strip()
        if not self.data:
            return
        print("Got a request of: %s\n" % self.data)

        # Parse the get request from the client
        parts = self.data.split('\r\n')
        request = parts[0].split()
        path += request[1]

        # If client accesses directory, pass them the index file instead
        if path.endswith('/'):
            path += "index.html"
        else:
            # If client accesses a file, try treating it as a directory
            # If it can be open, it is a directory in disguise
            temppath = path + "/index.html"
            try:
                tempfile = open(temppath)

                # Redirect the client to the correct directory path
                self.request.send("HTTP/1.1 301 Moved Permanently\r\n")
                self.request.send("Location: " + request[1] + "/\r\n")

                tempfile.close()
                return
            except:
                pass

        # Credit to Thomas Curnow for suggesting using Absoule File paths
        absfilepath = os.path.abspath(path)
        if absolutestartpath not in absfilepath:
            # We have navigated outside the "www" folder
            self.request.send("HTTP/1.1 404 Not Found\r\n\r\n")
            self.request.send("404 Not Found")
            return

        # Try to open the file. If file is missing, throw 404 error
        try:
            tfile = open(path)
            self.request.send("HTTP/1.1 200 OK\r\n")

            # Send the correct Mime type to the client
            if path.endswith('css'):
                self.request.send("Content-Type: text/css\r\n\r\n")
            elif path.endswith('html'):
                self.request.send("Content-Type: text/html\r\n\r\n")

            # Send the data of the file to the client
            for line in tfile.readlines():
                self.request.send(line)

            tfile.close()
        except:
            # File could not be opened because it was not there
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
