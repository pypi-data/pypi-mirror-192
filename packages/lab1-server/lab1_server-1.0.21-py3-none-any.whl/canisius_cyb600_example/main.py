from http.server import BaseHTTPRequestHandler, HTTPServer
import datetime

hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        current_time = datetime.datetime.now().strftime('%A, %B %d, %Y %I:%M:%S %p')
        self.wfile.write("<html><body><h1>The current time is: {}</h1></body></html>".format(current_time).encode())


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
