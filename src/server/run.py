import redis
import json

class Server(object):
    """
    Either creates server or connects to existing server
    """

    def __init__(self, handler, host="localhost", port=6379, sender="cvproj", receiver="cvproj"):
        print(receiver, handler)
        self.r = redis.Redis(host=host, port=port, socket_keepalive=True)
        self.pubsub = self.r.pubsub()
        self.pubsub.subscribe(**{receiver:handler})
        self.pubsub.run_in_thread()
        self.channel = sender

    def send(self, data):
        self.r.publish(self.channel, data)

    def send_json(self, data):
        self.r.publish(self.channel, json.dumps(data))

    def listen(self):
        for item in self.pubsub.listen():
            yield item

    def listen_json(self):
        for item in self.pubsub.listen():
            yield json.loads(item)

