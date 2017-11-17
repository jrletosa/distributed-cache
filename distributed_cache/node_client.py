import requests_utils as req
import json


class NodeClient(object):
    
    @staticmethod
    def set(ip, key, value):
        payload = {
            'key': key,
            'value': value
        }
        req.post('http://' + ip + '/set', data=json.dumps(payload))

    @staticmethod
    def set_replica(ip, key, value):
        payload = {
            'key': key,
            'value': value
        }
        req.post('http://' + ip + '/set-replica', data=json.dumps(payload))
        
    @staticmethod
    def get(ip, key):
        res = req.get('http://' + ip + '/get/{}'.format(key))
        return res.json()
        
    @staticmethod
    def update_conf(ip, conf):
        req.post('http://' + ip + '/node-configuration', data=json.dumps(conf))
