from websocket_server import WebsocketServer


class WebSocketServer:

    global rvr
    def __init__(self, host='0.0.0.0', port=8080, cmdCallback=None):
        self.host = host
        self.port = port
        self.cmdCallback = cmdCallback
        self.server = WebsocketServer(port=self.port, host=self.host)
        self.server.set_fn_new_client(self.new_client)
        self.server.set_fn_client_left(self.client_left)
        self.server.set_fn_message_received(self.message_received)

    def new_client(self, client, server):
        print(f"Client connecté: {client['id']}")

    def client_left(self, client, server):
        print(f"Client déconnecté: {client['id']}")

    def message_received(self, client, server, message):
        print(f"Message reçu de {client['id']}: {message}")
        self.cmdCallback(message)
        self.server.send_message(client, f"Echo: {message}")
    def run(self):
        print(f"WebSocket Server démarré à ws://{self.host}:{self.port}")
        self.server.run_forever()

