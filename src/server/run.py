import redis
import json

class Server(object):
    """
    Either creates server or connects to existing server
    """

    def __init__(self, host="localhost", port=6379, topic="cvproj"):
        self.r = redis.Redis(host=host, port=port, socket_keepalive=True)
        self.pubsub = self.r.pubsub()
        self.channel = topic

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

