import endpoints
import os

from config import Config


def create_app(config):
    app = endpoints.create_app(config)
    return app


def main():
    node_id = int(os.environ.get('NODE_ID'))
    node_ip = os.environ.get('NODE_IP')
    linked_node_id = int(os.environ.get('LINKED_NODE_ID'))
    linked_node_ip = os.environ.get('LINKED_NODE_IP')
    config = Config(
        node_id,
        node_ip,
        linked_node_id,
        linked_node_ip)
    app = create_app(config)
    app.run(host='0.0.0.0', port=80, server='waitress', threads=1, loglevel='warning')
