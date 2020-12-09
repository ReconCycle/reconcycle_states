#!/usr/bin/python3

from genpy.rostime import Duration
import rospy
from flexbe_core import EventState
from sensor_msgs.msg import JointState
import pymongo


class WriteToMongo(EventState):

    '''
    Implements a state that writes data to MongoDB
    [...]
    
    -- calculation  function        The function that performs [...]

    ># input_value  entry_data      Data to write into MongoDB
    ># input_value  entry_name      The name under which the name is written into MongoDB

    <= continue                     Written successfully
    <= failed                       Failed
    '''
    
    def __init__(self):
        rospy.loginfo('__init__ callback happened.')        
        super(WriteToMongo, self).__init__(outcomes = ['continue', 'failed'], input_keys = ['entry_data','entry_name'])

    def execute(self, userdata):
        rospy.loginfo('Execute callback happened.')
        client = pymongo.MongoClient('mongodb://localhost:27017/')  # if server does not run locally, please change it to your needs

        user_base = client["UserData"]
        user_collection = user_base["JointStates"]

        # Switch JointState... below with userdata.entry_data when tests are done
        entry_data = JointState(position=[1,2,3,4,5,6,7], name=['a','b','c','d', 'e', 'f', 'g'])
        
        # Check for the last _id value if index id is used, otherwise comment out
        collection_docs = user_collection.find()
        doc_id_list = []
        for doc in collection_docs:
            doc_id_list.append(doc["_id"])

        if doc_id_list == []:
            self.id_num = 1
        else:
            self.id_num = doc_id_list[-1] + 1       
       
        # Declare document being writen to MongoDB
        # Currently used self.id_num can be canged to userdata.entry_name as document ID!
        state_collections = [{"_id": self.id_num,
                             "header": {"seq": entry_data.header.seq, 
                                        "stamp": {"secs": entry_data.header.stamp.secs, "nsecs": entry_data.header.stamp.nsecs},
                                        "frame_id": entry_data.header.frame_id},
                             "name": entry_data.name,
                             "position": entry_data.position,
                             "velocity": entry_data.velocity,
                             "effort": entry_data.effort}]
            
        # Write to MongoDB
        ins = user_collection.insert_many(state_collections)

        rospy.loginfo("Successfully written: {}".format(state_collections))

        #print("Database list: {}".format(client.list_database_names()))
        #print("Collection list: {}".format(user_base.list_collection_names()))
        #print("Count documents: {}".format(user_collection.count_documents({}) ))
        
        # Uncomment only if you would like to clear collection while index id is used!!!
        #cdocs = user_collection.find()
        #del_list = []
        #for d in cdocs:
        #   del_list.append(d["_id"])
        #for i in del_list:
        #   print(i)
        #   user_collection.delete_one({"_id": i})
             
    def on_enter(self, userdata):
        rospy.loginfo('On Enter callback happened.')

        # entry_data = userdata.entry_data --> Tole bo tipa from sensor_msgs.msg import JointState (JointState.position, JointState.name, ...)
        # entry_name = userdata.entry_name
        
        # -------------- Test dispaly data ---------------- 
        #entry_data = JointState(position=[1,2,3,4,5,6,7],name=['a','b','c','d', 'e', 'f', 'g'])
        #entry_name = 'test_data'

        #print('entry_data = {}'.format(entry_data))
        #print('entry_name = {}'.format(entry_name))
        # ------------------------------------------
    def on_exit(self, userdata):
        rospy.loginfo('Exit callback happened.')
        return 'continue'