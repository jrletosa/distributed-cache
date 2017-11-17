import nose.tools as nt
import time

from mock import patch
from webtest import TestApp
from distributed_cache import create_app
from distributed_cache.config import Config


class TestCacheService(object):

    @patch('distributed_cache.node_client.NodeClient.update_conf')
    def setup(self, client_mock):
        self.config = Config(
            node_id=0,
            node_ip='192.168.0.10',
            linked_node_id=1,
            linked_node_ip='192.168.0.11')
        app = create_app(self.config)
        self.app = TestApp(app)
        time.sleep(2)
        nt.assert_equals(client_mock.call_count, 1)

    @patch('distributed_cache.consistent_hash.ConsistentHash.get_machine')
    @patch('distributed_cache.node_client.NodeClient.set_replica')
    def test_get_key_from_node(self, client_mock, machine_hash_mock):
        machine_hash_mock.return_value = self.config.node_id
        payload = {
            'key': 'a-key',
            'value': 'a-value'
        }
        res = self.app.post_json('/set', payload)
        nt.assert_equals(res.status_int, 200)
        nt.assert_equals(client_mock.call_count, 1)
        
        # get inserted key value
        res = self.app.get('/get/{}'.format('a-key'))
        nt.assert_equals(payload['value'], res.json['value'])
        
    @patch('distributed_cache.consistent_hash.ConsistentHash.get_machine')
    @patch('distributed_cache.node_client.NodeClient.get')
    def test_get_key_from_another_node(self, client_mock, machine_hash_mock):
        machine_hash_mock.return_value = (self.config.node_id + 1) % len(self.config.node_ips)
        client_mock.return_value = {'value': 'a-value'}
        # get inserted key value
        res = self.app.get('/get/{}'.format('a-key'))
        nt.assert_equals('a-value', res.json['value'])
        
