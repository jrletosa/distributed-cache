import cache
import copy


from consistent_hash import ConsistentHash
from node_client import NodeClient

NUM_HASH_REPLICAS = 3


class Processor(object):    
    def __init__(self, config):
        self.config = config
        self.storage = cache.Storage()
        
    def set(self, key, value):
        ''' Add the pair key-value to the cache cluster. If the data is not supposed
        to be stored in this node according to the hash function, the node calls the
        right node in the cluster.
        '''
        node_id = ConsistentHash(len(self.config.node_ips), NUM_HASH_REPLICAS).get_machine(key)
        if node_id == self.config.node_id:
            self.storage.add(key, value)
            next_node = (node_id + 1) % len(self.config.node_ips)
            # store replica in another node
            NodeClient.set_replica(self.config.node_ips[next_node], key, value)
        else:
            # set in node
            NodeClient.set(self.config.node_ips[node_id], key, value)
        
    def set_replica(self, key, value):
        self.storage.add(key, value)
        
    def get(self, key):
        ''' Get the value associated to key. If the key is not found in this node, the
        node calls the right node in the cluster
        '''
        # Due to data replication, key may be in this node even
        # if the corresponding hash points to a different node
        value = self.storage.get(key)
        if value is not None:
            return value
            
        # if value is not found, search in corresponding node
        node_id = ConsistentHash(len(self.config.node_ips), NUM_HASH_REPLICAS).get_machine(key)
        if node_id == self.config.node_id:
            # The key being searched does not exist in the cluster
            return None
        # get value from machine
        return NodeClient.get(self.config.node_ips[node_id], key)['value']
        
    def update_nodes_configuration(self):
        # update known nodes with this current node's configuration
        node_ips = copy.deepcopy(self.config.node_ips)
        for node_id, node_ip in node_ips.iteritems():
            if node_id != self.config.node_id:
                NodeClient.update_conf(node_ip, node_ips)
        
    def update_configuration(self, conf):
        conf_updated = self.config.add_nodes(conf)
        # update nodes configuration
        if conf_updated:
            self.redistribute_data()
            self.update_nodes_configuration()
    
    def redistribute_data(self):
        cache = copy.deepcopy(self.storage.map)
        for key, value in cache.iteritems():
            # set key and value in the corresponding node
            self.set(key, value)
            # remove data from this node if necessary
            node_id = ConsistentHash(len(self.config.node_ips), NUM_HASH_REPLICAS).get_machine(key)
            if node_id != self.config.node_id and \
                (node_id + 1) % len(self.config.node_ips) != self.config.node_id:
                self.storage.remove(key)
    
    def data_snapshot(self):
        ''' Retrieve the data stored in this node'''
        return self.storage.map
