#!/usr/bin/python3
from utils import sign_url
from http.server import BaseHTTPRequestHandler
from jinja2 import Template
import os
from ssl import PROTOCOL_TLS_SERVER, SSLContext
from socketserver import TCPServer
from loguru import logger
import time
import sys

template = Template("""<!DOCTYPE html>
 <html>
                <head>
                            <link href="https://fonts.googleapis.com/css2?family=Comfortaa:wght@300..700&display=swap" rel="stylesheet">
 
                              <link rel="preconnect" href="https://fonts.googleapis.com">
                        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
                    <script src="https://app.mode.com/embed/embed.js"></script>
                    <style>
                      .tb { border-collapse: collapse; }
                      .tb th, .tb td { padding: 5px; border: solid 1px #777; text-align: center;}
                      .tb th { background-color: lightblue; }
                      body {background-color: #191924;}
                      h1 { color: white;}
                      h1 {  font-family: "Comfortaa", sans-serif;
  font-optical-sizing: auto;
  font-weight: 700;
  font-style: normal;}
                      <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
                        <a href="https://app.mode.com/solutionssandbox/reports/663318dbd45e/embed?access_key=5f2a773c9d022ce36df7df50&max_age=&signature=[xxx]" class="mode-embed">Mode Analytics</a><script src="https://app.mode.com/embed/embed.js"></script>
                    </style>
                    <!-- UIkit CSS -->
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/uikit@3.19.1/dist/css/uikit.min.css" />

                    <!-- UIkit JS -->
                    <script src="https://cdn.jsdelivr.net/npm/uikit@3.19.1/dist/js/uikit.min.js"></script>
                    <script src="https://cdn.jsdelivr.net/npm/uikit@3.19.1/dist/js/uikit-icons.min.js"></script>
                </head>
                <body>
                <h1> Q1-2024 Learnsoity Support On-Hold Feature Requests Review </h1>
                <hr class="uk-divider-icon" /> 
                <iframe
                    src="{{ signed_url }}"
                    width="100%"
                    height="1800"
                    frameborder="0"
                    </iframe>
                        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>

                </body>
                </html>
                                """)


class ReportServer(BaseHTTPRequestHandler):

    def createResponse(self, response):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(response.encode("utf-8"))

    def do_GET(self):

        if self.path.endswith("/"):
            logger.info('Navigiating to Home page')
            response = template.render(
                signed_url=sign_url(
                    url=f"https://app.mode.com/solutionssandbox/reports/663318dbd45e/embed?\
?access_key={os.getenv('ACCESS_KEY')}\
&run=now\
&timestamp={time.time()}/",
                    key=os.getenv('ACCESS_KEY'),
                    secret=os.getenv('ACCESS_SECRET')               )
            )
            self.createResponse(response)


def main(host, port):
    context = SSLContext(PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="ca-public.pem", keyfile="ca-private.pem")
    server_address = (host, port)
    handler = ReportServer

    with TCPServer(server_address, handler) as httpd:
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
        logger.success(
                "Server started https://%s:%s. Press Ctrl-c to quit." %
                (server_address[0], server_address[1]))
        try:
            httpd.serve_forever()

        except KeyboardInterrupt:
            logger.warning('Shut Down Command Recieved - Shutting Down Server')
            httpd.server_close()


if __name__ == "__main__":
    if sys.argv:
        try:
            logger.info('Starting Server')
            main(sys.argv[0], sys.argv[1])
        except Exception as e:
            logger.error(f'Unable to Start Server {e}')
            raise e from e
    else:
        print('Please Provide a Host and Port On Invocation')
        sys.exit(1)
