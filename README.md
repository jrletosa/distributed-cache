# distributed-cache
Simple distributed cache in Python

## Run tests locally
```bash
rake test_local
```

## Build
To build and create a docker container with the application in it:

```bash
rake build
```

## Launch Cluster
To launch a cache cluster, run:

```bash
rake launch[3]
```

The command allows to specify the number of nodes to be launched (3 in this example).

When a cluster is launched, a docker network is created and each docker is run so that they are attached to the created network.

Each container requires the following environment variables to start:

* NODE_ID: ID of the node.
* NODE_IP: IP of the node.
* LINKED_NODE_ID: ID of some other node in the cluster.
* LINKED_NODE_IP: IP of the LINKED_NODE_ID node.

## Client
See client/cache_client.py for examples of how to use the client.

The client is able to perform three operations:

* Get: Get the corresponding value for a key. This operation can be executed against any of the nodes of the cluster, i.e. the serving node will return the searched value even if it is not present  in its local storage.
* Set: Set a key-pair value in the storage. This operation can be executed against any of the nodes of the cluster, i.e. the serving node is able to redistribute the new incoming data to other nodes.
* Dump: Get a copy of the local node's storage. Useful for testing.

## Data availability
To make sure the cluster does not loose any data even if one of the nodes is lost, the service performs two write operations for every SET request. Once the right node *i* has been identified to store the data based on the hash function, the cluster stores the data in the node i and sends a request to the *(i + 1) % num_machines* node to store a replica of the data.

## Node discovery
Every node in the system only requires its node ID and IP and the corresponding ID and IP for one (any) of the other nodes in the cluster.
At startup, each node propagates its current configuration to the specified linked node. On top of that, each node propagates its current configuration to all the known nodes every time a configuration update is received by other node and locally updated. Whenever a node receives a configuration with no new values, it stops propagating to other nodes.

With this mechanism, all nodes in the cluster eventually have a complete list of all the nodes in the cluster.

This solution also makes possible to start new nodes at any time.

## Inter communication
Communication between the system components is performed over HTTP.

## Known issues

### Concurrency

Storage uses a simple in-memory Python dictionary. This means implementation is not thread-safe and multiple requests at the same time may crash the service. In order to have a more robust implementation, other solutions should be implemented, such as having shared-memory objects.

#### Data Redistribution

Whenever a new node is added to the cluster, the nodes try to redistribute the data again across the cluster. There is an initial implementation in place but, due to lack of time, this is sometimes failing when a node tries to redistribute the data and the nodes configuration has not yet completed.
