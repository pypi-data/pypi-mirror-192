# MongoGraph - build Graph DataBase on top of MongoDB

### First of its kind among Python Packages that can be used as a stable client for Graph operations on MongoDB

## Setup:
```

pip install mongograph

```
## Usage:
```

from mongograph import MongoGraph

MONGO_URL="mongodb+srv://user:password@clusterx.xxxxxxx.mongodb.net/?retryWrites=true&w=majority"

graph_client = MongoGraph(connection_string=URL)

ack = graph_client.is_connected()

print("connected: ",ack)

```

### 1. Creating, Updating & Deleting Nodes:
```
#Create a Node
node_properties = {"name":"myName"}
node_id1 = graph_client.add_node(label="user",properties=node_properties)
print(node_id1)

#Update a Node
import datetime
node_properties = {"name":"myNewName", "todayDate":datetime.datetime.now() }
update_ACK = graph_client.update_node(properties={"name":"no name"}, label="user", node_id=node_id1)
print("updated: ",update_ACK)

#Delete a Node
delete_ACK = graph_client.delete_node(node_id=node_id1, label="user")
print("deleted: ",delete_ACK)

```

### 2. Creating, Updating & Deleting Edges:
```
#Create an Edge
node_id2 = graph_client.add_node(label="user",properties={"name":"yourName"})
edge_id = graph_client.add_edge(label="friends",
                                from_node_label="user",
                                to_node_label="user",
                                from_node_id=node_id2,
                                to_node_id=node_id1,
                                properties={"creation":datetime.datetime.now()})

print(edge_id)

#Update an Edge
update_ACK = graph_client.update_edge(label="friends", 
                                        edge_id=edge_id , 
                                        properties={"property1":datetime.datetime.now()})

print("updated: ",update_ACK)


#Delete an Edge
delete_ACK = graph_client.delete_edge(edge_id=edge_id, label="friends") 
print("deleted: ",delete_ACK)

```




