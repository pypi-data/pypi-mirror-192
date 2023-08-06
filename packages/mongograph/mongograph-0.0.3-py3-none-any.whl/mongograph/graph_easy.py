import os
import sys
from mongograph.mongo_wrapper._mongo_wrapper import DataBaseController

class MongoGraph:
    def __init__(self,connection_string:str):
        try:
            if (os.name != 'nt') and (os.name != 'posix'):
                raise OSError('UNSUITABLE OS ')

            self.__mongo_controller = DataBaseController(mongodb_url=connection_string)
            setup_ack = self.__mongo_controller.setup_databases()
            if setup_ack:
                sys.stdout.write('GRAPH INITIATED')
                
        except Exception as initialization_error:
            raise RuntimeError('INITIALIZATION ERROR'+str(initialization_error))
    
    def get_node_id(self, label:str, property_name:str, property_value):
        try:
            
            node = self.__mongo_controller.get_vertex(vertex_label=label,
                                                         property_name=property_name,
                                                         property_value=property_value)
            if node == {}:
                return None
            else:
                return str(node["_id"])
        except Exception as logic_err:
            raise RuntimeError("FAILED TO GET NODE ID"+str(logic_err))
        
    def add_node(self, label:str, properties:dict):
        try:
            if properties=={}:
                raise RuntimeError("EMPTY DICTIONARY NOT ACCEPTABLE")
            node_id = self.__mongo_controller.create_vertex(vertex_label=label,property_dict=properties)
            sys.stdout.write('ADDED NODE: '+str(node_id))
            return node_id
        except Exception as logic_err:
            raise RuntimeError("FAILED TO ADD NODE"+str(logic_err))
    
    def update_node(self, node_id:str, label:str, properties:dict):
        try:
            if properties=={}:
                raise RuntimeError("EMPTY DICTIONARY NOT ACCEPTABLE")
            update_ack = self.__mongo_controller.update_vertex(vertex_id=node_id,
                                                            vertex_label=label,
                                                            updated_property_dict=properties)
            sys.stdout.write('UPDATED NODE: '+str(node_id)+str(update_ack))
            return update_ack
        except Exception as logic_err:
            raise RuntimeError("FAILED TO UPDATE NODE"+str(logic_err))
    
    def delete_node(self, node_id:str, label:str):
        try:
            delete_ack = self.__mongo_controller.delete_vertex(vertex_id=node_id,
                                                               vertex_label=label)
            sys.stdout.write('DELETED NODE: '+str(node_id)+str(delete_ack))
            return delete_ack
        except Exception as logic_err:
            raise RuntimeError("FAILED TO DELETE NODE"+str(logic_err))
    
    def get_edge_id(self, label:str, from_vertex_id:str, to_vertex_id:str):
        try:
            edge = self.__mongo_controller.get_edge(edge_label=label, from_vertex_id= from_vertex_id, to_vertex_id=to_vertex_id)
            
            if edge == {}:
                return None
            else:
                return str(edge["_id"])
        except Exception as logic_err:
            raise RuntimeError("FAILED TO GET EDGE ID"+str(logic_err))
    
    def add_edge(self, 
                 label:str, 
                 from_node_id:str,
                 to_node_id:str,
                 from_node_label:str,
                 to_node_label:str,
                 properties:dict,
                 direction=None):
        try:
            if properties=={}:
                raise RuntimeError("EMPTY DICTIONARY NOT ACCEPTABLE")
            if direction == None:
                edge_id = self.__mongo_controller.create_edge(edge_label=label, 
                                                            from_vertex_label=from_node_label, 
                                                            to_vertex_label=to_node_label, 
                                                            from_vertex_id=from_node_id, 
                                                            to_vertex_id=to_node_id, 
                                                            property_dict=properties, 
                                                            direction="unidirection")
            else:
                edge_id = self.__mongo_controller.create_edge(edge_label=label, 
                                                            from_vertex_label=from_node_label, 
                                                            to_vertex_label=to_node_label, 
                                                            from_vertex_id=from_node_id, 
                                                            to_vertex_id=to_node_id, 
                                                            property_dict=properties, 
                                                            direction=direction)
            sys.stdout.write('ADDED EDGE: '+str(edge_id))
            return edge_id
        except Exception as logic_err:
            raise RuntimeError("FAILED TO ADD EDGE"+str(logic_err))
    
    def update_edge(self, edge_id:str, label:str, properties:dict):
        try:
            if properties=={}:
                raise RuntimeError("EMPTY DICTIONARY NOT ACCEPTABLE")
            update_ack = self.__mongo_controller.update_edge(edge_id=edge_id,
                                                            edge_label=label,
                                                            updated_property_dict=properties)
            sys.stdout.write('UPDATED EDGE: '+str(edge_id)+str(update_ack))
            return update_ack
        except Exception as logic_err:
            raise RuntimeError("FAILED TO UPDATE EDGE"+str(logic_err))
    
    def delete_edge(self, edge_id:str, label:str):
        try:
            delete_ack = self.__mongo_controller.delete_edge(edge_id=edge_id,
                                                             edge_label=label)
            sys.stdout.write('DELETED EDGE: '+str(edge_id)+str(delete_ack))
            return delete_ack
        except Exception as logic_err:
            raise RuntimeError("FAILED TO DELETE EDGE"+str(logic_err))
    
    def is_connected(self):
        connect_ack = self.__mongo_controller.is_connected()
        return connect_ack

    def close_instance(self):
        ack = self.__mongo_controller.close_connection()
        return ack
    
    