class Config(object):
    
    def __init__(
            self,
            node_id,
            node_ip,
            linked_node_id,
            linked_node_ip):
        
        self.node_id = node_id
        self.node_ip = node_ip
        self.linked_node_ip = linked_node_ip
        self.node_ips = {
            self.node_id: self.node_ip,  # this node's ID and IP
            linked_node_id: linked_node_ip  # neighbour's ID and IP
        }
        
    def add_nodes(self, conf):
        current_len = len(self.node_ips)
        self.node_ips.update(conf)
        return current_len != len(self.node_ips)
