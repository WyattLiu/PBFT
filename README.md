# Modified PBFT layer for RAC (CRDT) 

Client interface is forking https://github.com/yunhaom94/rKVCRDT

# Structure
bftclient.py -> one of the pbft node (through a safeclient spawn in localhost) -> RAC

# Flow
1. bftclient uses POST to communicate with a pbft node, pbft sees the cmd as a payload which includes the port and hostname the bftclient is listening for callback.
2. After voting is completed and the pbft nodes reached concensus, the request (with client hostname+port) then forwarded to a localhost spawned safeclient.py using socket.
3. The safeclient then communicate using socket with RAC and get the result natively using socket (with client hostname+port).
4. The safeclient then pass the result (with client hostname+port) back with POST to the pbft node
5. The pbft node will directly pass the result back to client using the hostname and port used during the process.

# CLI and arguments

bftclient.py
```sh
python3 ./bftclient.py  127.0.0.1:50000 127.0.0.1:3002
arg1 = RAC address (not using it, just for dev testing)
arg2 = A PBFT node, could be anyone of the group
```
PBFT, it consists node which may require a few npm install XXX to get it working
```sh
node networkNode.js master full 192.168.1.104 this 192.168.1.104:50001
arg1 = master node that can make block -> needed to be master
arg2 = full, store the entire chain, keep as it is
arg3 = my addr
arg4 = master addr
arg5 = RAC address (not using it, just for dev testing)
```
safeclient.py
```sh
python3 safeclient.py 127.0.0.1:50000
arg1 = RAC address
```
Bind to localhost 60003

# Practical Byzantine Fault Tolerance
PBFT is a consensus algorithm [used by some of the biggest Blockchains](https://blockonomi.com/practical-byzantine-fault-tolerance/).

It's known for being a more scalable alternative to the traditional [Proof of Work](https://en.wikipedia.org/wiki/Proof-of-work_system).

## Execution

It is possible to start many nodes in the same machine or in different VMs, the initialization is the same, as follows:

```sh
$ node networkNode.js <node_type> <blockchain_type> <ip_address> <any_master_node_ip>
```

Example:

```sh
node networkNode.js master full 192.168.0.1 192.168.0.2
```

Node type should be either `master` or `network`. Only `master` nodes are allowed to create blocks in PBFT. Any node will take part in the voting though.

Blockchain type should be either `full` or `light`. The `full` type gets the entire blockchain from `master` node, but this is more time and network consuming. `full`'s counter part is `light`, that is fast and lightweight with the main downside of not receiving the entire blockchain (only the last 10 blocks from `master` node).

`any_master_node_ip` should be a reachable `master` node ip address. If it is the first node in the network, use `this`, the node will then start as the first master node. Don't do this if you intend to connect to an active network, as the node will just start its own network and won't connect to any running nodes.

Both the `ip_address` and the `any_master_node_ip` passed in initialization should be only the ip itself (eg. `10.10.0.1`). Do not specify `http://` or the port in the end, this will result in a request error.

To test, you can reach `http://ip:port/` in your browser, it will return a `json` containing information on the node you requested, and the active nodes on the network.

To see the current blockchain, reach `http://ip:port/blockchain`.

To add a block to the blockchain, make a `post` request to `http://ip:port/createBlock` with a `json` payload as follows:
```js
{
	"timestamp": "YYYY-MM-DD HH:MM:SS",		// optional
	"carPlate": "<plate>",
	"block": {
		"data": "any data, can be an array, or json, str..."
	}
}
```

You can define an optional `timestamp` for testing purposes. If not specified, the `timestamp` will be the current time.

The `response` will contain the whole created block that was broadcast to the network, however, this does not mean the block was accepted. You can request the `/blockchain` to any node to check if the block was accepted.

There are a number of reasons for a block to be rejected, you can check the results of the voting process in any node `log`.

## Docker Example

Building docker container for pbft and starting n nodes.

```sh
docker build . pbft/algo
docker-compose scale node=<total-num-of-nodes> #starts n containers
```

Let's see the steps to follow for n=4 nodes with 2 master nodes.

Use `docker ps` for viewing the container ids. To get the ip of the container processes use:

```sh
docker exec -it pbft_node_1 ip addr
docker exec -it pbft_node_2 ip addr
docker exec -it pbft_node_3 ip addr
docker exec -it pbft_node_4 ip addr
```

Copy the container ip:

```sh
docker exec -it pbft_node_1 node networkNode.js master full <container-ip> this
docker exec -it pbft_node_2 node networkNode.js master full <container-ip> <pbft_node_1's_IP>
docker exec -it pbft_node_3 node networkNode.js network full <container-ip> <pbft_node_1or2's_IP>
docker exec -it pbft_node_4 node networkNode.js network full <container-ip> <pbft_node_1or2's_IP>
```
These will start 2 master node and 2 network nodes.

### Interacting with blockchain

#### View

```sh
curl <node_ip>:3002/blockchain # for viewing the blockchain
```

#### Append

```sh
curl -XPOST <master_node_ip>:3002/createblock -H "Content-Type: application/json" -d '{
 "timestamp": "YYYY-MM-DD HH:MM:SS",  // optional
 "carPlate": "<plate>",
 "block": {
  "data": "any data, can be an array, or json, str..."
 }
}' # for creating a new block
```

#### View

```sh
curl <node_ip>:3002/blockchain # for viewing the blockchain after the adding of new block is completed
```

---

Further repositories of the CarChain Project:

[Blockchain Visualizer](https://github.com/LRAbbade/Blockchain-Visualizer)

[CarChain Dashboard](https://github.com/LRAbbade/CarChain-Dashboard)

[Car Simulator](https://github.com/LRAbbade/Car_Simulator)
