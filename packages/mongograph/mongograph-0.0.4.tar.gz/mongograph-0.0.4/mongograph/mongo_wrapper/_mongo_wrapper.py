import os
import sys
from pymongo import MongoClient
import bson

class DataBaseController:
    def __init__(self,
                    mongodb_url:str):
        try:
            if (os.name != 'nt') and (os.name != 'posix'):
                raise OSError('UNSUITABLE OS ')

            self.__mongodb_endpoint = mongodb_url
            self.__max_retry_value = int(5)
            connection_ack = self.__initiate_connection()
                
        except Exception as initialization_error:
            raise RuntimeError('INITIALIZATION ERROR') from initialization_error
    
    def __initiate_connection(self):
        try:
            self.__database_client = MongoClient(self.__mongodb_endpoint)
            sys.stdout.write('CONNECTED WITH MONGODB')
            return True
        except Exception as connection_err:
            raise ConnectionError("FAILED TO CONNECT TO MONGODB"+str(connection_err))
    
    def is_connected(self):
        try:
            if self.__database_client.server_info():
                return True
        except Exception as connection_err:
            raise ConnectionError("BROKEN CONNECTION TO MONGODB"+str(connection_err))
    
    def close_connection(self):
        try:
            self.__database_client.close()
            return True
        except Exception as connection_err:
            raise ConnectionError("FAILED TO CLOSE CONNECTION WITH MONGODB"+str(connection_err))
    
    def __stabilise_connection(self):
        try:
            if self.is_connected():
                return True
            else:
                stopper = self.__max_retry_value
                for iteration in range(self.__max_retry_value):
                    connection_ack = self.__initiate_connection()
                    if connection_ack:
                        return True
                    elif iteration==(stopper-1):
                        raise ConnectionError("FAILED TO CONNECT WITH MONGODB"+str(connection_err))
                    else:
                        continue
        except Exception as connection_err:
            raise ConnectionError("FAILED TO CLOSE CONNECTION WITH MONGODB"+str(connection_err))
    
    def setup_databases(self):
        try:
            self.__vertex_collection_dict = {}
            self.__edge_collection_dict = {}
            self.__vertex_db = self.__database_client["vertex"]
            self.__edge_db = self.__database_client["edge"]

            try:
                vertex_collection_list = self.__vertex_db.list_collection_names()
            except Exception as logic_err:
                vertex_collection_list = []
            
            try:
                edge_collection_list = self.__edge_db.list_collection_names()
            except Exception as logic_err:
                edge_collection_list = []

            if (vertex_collection_list) != [] and (vertex_collection_list != None):
                for vertex_name in vertex_collection_list:
                    self.__vertex_collection_dict.update({str(vertex_name):self.__vertex_db[str(vertex_name)]})
            
            if (edge_collection_list) != [] and (edge_collection_list != None):
                for edge_name in edge_collection_list:
                    self.__edge_collection_dict.update({str(edge_name):self.__edge_db[str(edge_name)]})
            return True

        except Exception as logic_err:
            raise ConnectionError("FAILED TO SETUP DATABASES"+str(logic_err))
    
    def __collection_exists(self, collection_name:str, db_name:str):
        if db_name == "vertex":
            if collection_name in list(self.__vertex_collection_dict.keys()):
                return True
            else:
                return False
        elif db_name == "edge":
            if collection_name in list(self.__edge_collection_dict.keys()):
                return True
            else:
                return False
        else:
            return False
    
    def __add_vertex_dict_object(self, collection_name:str):
        if self.__collection_exists(collection_name="vertex",db_name=collection_name):
            return False
        else:
            self.__vertex_collection_dict.update({str(collection_name):self.__vertex_db[str(collection_name)]})
            return True
    
    def __add_edge_dict_object(self, collection_name:str):
        if self.__collection_exists(collection_name="edge",db_name=collection_name):
            return False
        else:
            self.__edge_collection_dict.update({str(collection_name):self.__edge_db[str(collection_name)]})
            return True
    
    def vertex_exists(self, vertex_id:str, vertex_label:str):
        if self.__collection_exists(collection_name=vertex_label, db_name="vertex"):
            result = self.__vertex_collection_dict[vertex_label].find_one({"_id":bson.objectid.ObjectId(vertex_id)})
            if (result != {}) and (result != None):
                return True
            else:
                return False
        else:
            return False
    
    def edge_exists(self, edge_label:str, edge_id=None, from_vertex_id=None, to_vertex_id=None):

        if (edge_id==None) and (from_vertex_id==None) and (to_vertex_id==None):
            raise RuntimeError("EDGE ID AND VERTEX IDS MISSING")

        if self.__collection_exists(collection_name=edge_label, db_name="edge"):
            if edge_id!= None:
                result = self.__edge_collection_dict[edge_label].find_one({"_id":bson.objectid.ObjectId(edge_id)})
                if (result != {}) and (result != None):
                    return True
                else:
                    return False
            elif (from_vertex_id==None) and (to_vertex_id==None):
                result = self.__edge_collection_dict[edge_label].find_one({"from_vertex_id":bson.objectid.ObjectId(from_vertex_id),
                                                                            "to_vertex_id":bson.objectid.ObjectId(to_vertex_id)})
                if (result != {}) and (result != None):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def create_vertex(self, vertex_label:str, property_dict:dict):
        if property_dict == {}:
            raise RuntimeError("EMPTY DICTIONARY IS NOT ACCEPTED")
        
        if self.__collection_exists(collection_name=vertex_label, db_name="vertex"):
            property_dict.update({"label":vertex_label})
            vertex = self.__vertex_collection_dict[vertex_label].insert_one(property_dict)
            if vertex.acknowledged:
                return str(vertex.inserted_id)
        
        else:
            vertex_ack = self.__add_vertex_dict_object(collection_name=vertex_label)
            property_dict.update({"label": vertex_label})
            vertex = self.__vertex_collection_dict[vertex_label].insert_one(property_dict)
            if vertex.acknowledged:
                return str(vertex.inserted_id)
    
    def update_vertex(self, vertex_id:str, vertex_label:str, updated_property_dict:dict):
        if updated_property_dict == {}:
            raise RuntimeError("EMPTY DICTIONARY IS NOT ACCEPTED")
        if self.__collection_exists(collection_name=vertex_label, db_name="vertex"):
            updated_property_dict.update({"label":vertex_label})
            vertex_update_ack = self.__vertex_collection_dict[vertex_label].update_one({"_id":bson.objectid.ObjectId(vertex_id)},
                                                                                       {"$set":updated_property_dict}, 
                                                                                       upsert=False)
            if vertex_update_ack.matched_count == 1:
                return True
            else:
                return False
        else:
            return False

    def delete_vertex(self, vertex_id:str, vertex_label:str):
        if self.vertex_exists(vertex_id=vertex_id, vertex_label=vertex_label):
            result = self.__vertex_collection_dict[vertex_label].delete_one({"_id":bson.objectid.ObjectId(vertex_id)})
            if result.deleted_count > 0:
                return True
            else:
                return False
        else:
            return False

    def get_vertex(self, vertex_label:str, property_name:str, property_value):
        if self.__collection_exists(collection_name=vertex_label, db_name="vertex"):
            result = self.__vertex_collection_dict[vertex_label].find_one({property_name:property_value})
            if (result != {}) and (result != None):
                return result
            else:
                return {}
        else:
            return {}
    
    def create_edge(self, 
                    edge_label:str, 
                    from_vertex_label:str, 
                    to_vertex_label:str, 
                    from_vertex_id:str, 
                    to_vertex_id:str, 
                    property_dict:dict,
                    direction:str):
        if self.vertex_exists(vertex_id=from_vertex_id, 
                                vertex_label=from_vertex_label) and self.vertex_exists(vertex_id=to_vertex_id, 
                                                                                        vertex_label=to_vertex_label):
            if self.__collection_exists(collection_name=edge_label, db_name="edge"):
                if direction in ["unidirection","bidirection"]:
                    property_dict.update({"from_vertex_label":from_vertex_label})
                    property_dict.update({"to_vertex_label":to_vertex_label})
                    property_dict.update({"from_vertex_id":from_vertex_id})
                    property_dict.update({"to_vertex_id":to_vertex_id})
                    property_dict.update({"edge_label":edge_label})
                    property_dict.update({"direction":direction})
                    edge = self.__edge_collection_dict[edge_label].insert_one(property_dict)
                    if edge.acknowledged:
                        return str(edge.inserted_id)
                    
                else:
                    raise RuntimeError("WORNG DIRECTION GIVEN")
            else:
                if direction in ["unidirection","bidirection"]:
                    edge_collection_ack = self.__add_edge_dict_object(collection_name=edge_label)
                    property_dict.update({"from_vertex_label":from_vertex_label})
                    property_dict.update({"to_vertex_label":to_vertex_label})
                    property_dict.update({"from_vertex_id":from_vertex_id})
                    property_dict.update({"to_vertex_id":to_vertex_id})
                    property_dict.update({"label":edge_label})
                    property_dict.update({"direction":direction})
                    edge = self.__edge_collection_dict[edge_label].insert_one(property_dict)
                    if edge.acknowledged:
                        return str(edge.inserted_id)
                else:
                    raise RuntimeError("WORNG DIRECTION GIVEN")
    
    def update_edge(self, edge_id:str, edge_label:str, updated_property_dict:dict):
        if updated_property_dict == {}:
            raise RuntimeError("EMPTY DICTIONARY IS NOT ACCEPTED")
        if self.__collection_exists(collection_name=edge_label, db_name="edge"):
            if self.edge_exists(edge_label=edge_label, edge_id=edge_id):
                #updated_property_dict["label"] = edge_label
                updated_property_dict.update({"label": edge_label})
                edge_update_ack = self.__edge_collection_dict[edge_label].update_one({"_id":bson.objectid.ObjectId(edge_id)},
                                                                                     {"$set":updated_property_dict}, 
                                                                                     upsert=False)
                if edge_update_ack.matched_count == 1:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    
    def delete_edge(self, edge_id:str, edge_label:str):
        if self.edge_exists(edge_id=edge_id, edge_label=edge_label):
            result = self.__edge_collection_dict[edge_label].delete_one({"_id":bson.objectid.ObjectId(edge_id)})
            if result.deleted_count > 0:
                return True
            else:
                return False
        else:
            return False
    
    def get_edge(self, edge_label:str, from_vertex_id:str, to_vertex_id:str):
        if self.__collection_exists(collection_name=edge_label, db_name="edge"):
            result = self.__edge_collection_dict[edge_label].find_one({"from_vertex_id":bson.objectid.ObjectId(from_vertex_id),
                                                                        "to_vertex_id":bson.objectid.ObjectId(to_vertex_id)})
            if (result != {}) and (result != None):
                return result
            else:
                return {}
        else:
            return {}






    










