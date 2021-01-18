from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
import logger
import payloadparser
import gamestate
import provider
from RecoilHandler import RecoilHandler


class GSIServer(HTTPServer):
    def __init__(self, server_address, token, RequestHandler):
        self.recoil_handler = RecoilHandler()
        self.log_file = logger.LogFile(time.asctime())
        self.provider = provider.Provider()
        self.auth_token = token
        self.gamestatemanager = gamestate.GameStateManager()

        super(GSIServer, self).__init__(server_address, RequestHandler)

        self.payload_parser = payloadparser.PayloadParser()


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        body = self.rfile.read(length).decode('utf-8')

        payload = json.loads(body)
        # Ignore unauthenticated payloads
        if not self.authenticate_payload(payload):
            return None

        # self.server.log_file.log_event(time.asctime(), payload)
        self.server.payload_parser.parse_payload(payload, self.server.gamestatemanager)

        # print(self.server.gamestatemanager.gamestate.player.weapons)

        self.server.recoil_handler.update_weapon_if_required(self.server.gamestatemanager.gamestate.player.weapons)

        self.send_header('Content-type', 'text/html')
        self.send_response(200)
        self.end_headers()

    @staticmethod
    def authenticate_payload(payload):
        if 'auth' in payload and 'token' in payload['auth']:
            return payload['auth']['token'] == server.auth_token
        else:
            return False

    def log_message(self, format, *args):
        """
        Prevents requests from printing into the console
        """
        return


server = GSIServer(('localhost', 3000), 'S8RL9Z6Y22TYQK45JB4V8PHRJJMD9DS9', RequestHandler)

print(time.asctime(), '-', 'CS:GO GSI csgogsi starting')

try:
    server.serve_forever()
except (KeyboardInterrupt, SystemExit):
    pass

server.server_close()
print(time.asctime(), '-', 'CS:GO GSI csgogsi stopped')
