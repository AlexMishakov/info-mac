#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
from os import replace
import subprocess
import re

hostName = str(subprocess.check_output("ipconfig getifaddr en0", shell=True))
hostName = re.sub("[b|'|n|\\\]", "", hostName)
serverPort = 7777

class MyServer(BaseHTTPRequestHandler):
    sleep_mod = 1

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        print(self.path)
        if self.path == "/sleep_mode/status":
            self.wfile.write(bytes(str(self.check_sleep_mode()), "utf-8"))
        elif self.path == "/sleep_mode/log":
            self.wfile.write(bytes("<html><head><title>Status macbook</title></head>", "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            status_string = subprocess.check_output("pmset -g log|grep -e \" Notification  \"", shell=True)
            self.wfile.write(bytes(str(status_string).replace("\\n", "<br>").replace("\"", "").replace("\\t", "    "), "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))
        else:
            self.wfile.write(bytes("<html><head><title>Info your mac</title></head>", "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes("<p><a href=\"/sleep_mode/status\">sleep_mode</a></p>", "utf-8"))
            self.wfile.write(bytes("<p><a href=\"/sleep_mode/log\">sleep_mode/log</a></p>", "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))
    
    def check_sleep_mode(self):
        status_string = subprocess.check_output("pmset -g log|grep -e \" Notification  \"", shell=True)
        status_array = str(status_string).split("\\n")
        status_last_array = status_array[-2].split("\\t")
        status = status_last_array[1].replace(" ", "")
        
        if status == "Displayisturnedon":
            self.sleep_mod = 1

        if status == "Displayisturnedoff":
            self.sleep_mod = 0
        
        return self.sleep_mod

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")