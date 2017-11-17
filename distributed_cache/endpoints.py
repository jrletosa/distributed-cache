import errors
import json
import time
import threading

from processor import Processor
from bottle import Bottle, request, response
    

def create_app(config):
    app = Bottle()
    processor = Processor(config)
    
    def update_configuration():
        # wait some time to give time to other nodes to start
        time.sleep(2)
        processor.update_nodes_configuration()
    
    # update nodes configuration on start up.
    # Execute this function in a separate thread so the main thread can 
    # proceed with server initialization
    thread = threading.Thread(target=update_configuration)
    thread.start()

    @app.error()
    @app.error(404)
    def handle_error(error):
        message = str(error.exception) if error.exception else ''
        resp = {
            'type': type(error.exception).__name__
        }
        if issubclass(type(error.exception), errors.CacheException):
            response.status = error.exception.code
            resp.update(error.exception.extra_data)
        else:
            response.status = error.status_code
            resp.update['traceback'] = error.traceback

        response.set_header('Content-type', 'application/json')
        return '%s %s' % (response.status, message)

    @app.route('/ping', method=['GET'])
    def ping():
        return {
            'service': 'cache-node',
            'status': 'OK'
        }
        
    @app.route('/set', method=['POST'])
    def set_data():
        data = json.loads(request.body.read())
        key = data['key']
        value = data['value']
        processor.set(key, value)
        return
        
    @app.route('/set-replica', method=['POST'])
    def set_replica_data():
        data = json.loads(request.body.read())
        key = data['key']
        value = data['value']
        processor.set_replica(key, value)
        return
        
    @app.route('/get/<key>', method=['GET'])
    def get_data(key):
        value = processor.get(key)
        return {'value': value}

    @app.route('/node-configuration', method=['POST'])
    def update_configuration():
        body = json.loads(request.body.read())
        conf = {}
        for node_id in body:
            conf[int(node_id)] = body[node_id]
        processor.update_configuration(conf)

    @app.route('/dump-content', method=['GET'])
    def dump_content():
        return processor.data_snapshot()
    return app
