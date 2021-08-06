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
            status_string = subprocess.check_output("pmset -g log|grep -e \" Notification  \"", shell=True).decode('ascii')
            self.wfile.write(bytes(str(status_string).replace("\n", "<br>"), "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))
        elif self.path == "/battery/status":
            self.wfile.write(bytes(str(self.battery_status()), "utf-8"))
        elif self.path == "/stop":
            exit()
        else:
            html_file = open("assets/index.html", "r").read()
            self.wfile.write(bytes(html_file, "utf-8"))
    
    def check_sleep_mode(self):
        status_string = subprocess.check_output("pmset -g log|grep -e \" Notification  \"", shell=True).decode('ascii')
        status_array = str(status_string).split("\n")
        status_last_array = status_array[-2].split("\t")
        status = status_last_array[1]
        status =  re.sub("\s\s+", " ", status) 
        
        if status == "Display is turned on ":
            self.sleep_mod = 1

        if status == "Display is turned off ":
            self.sleep_mod = 0
        
        return self.sleep_mod

    def battery_status(self):
        status_string = subprocess.check_output("pmset -g batt | grep -Eo \"\d+%\" | cut -d% -f1", shell=True)
        return status_string.decode('ascii')

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")