#!/usr/bin/python3

import rospy
from flexbe_core import EventState, Logger
from sensor_msgs.msg import JointState
import pymongo


class WriteToMongo(EventState):

    '''
    Implements a state that writes data to MongoDB
    [...]       

    ># entry_data  JointState()  Data to write into MongoDB (sensor_msgs.msg -> JointState() fromat!)
    ># entry_name  string/int    The name under which the name is written into MongoDB

    <= continue                     Written successfully
    <= failed                       Failed
    '''
    
    #-- calculation  function        The function that performs [...]

    def __init__(self):
        rospy.loginfo('__init__ callback happened.')        
        super(WriteToMongo, self).__init__(outcomes = ['continue', 'failed'], input_keys = ['entry_data','entry_name'])

    def execute(self, userdata):
        rospy.loginfo('Execute callback happened.')
        client = pymongo.MongoClient('mongodb://localhost:27017/')  # if server does not run locally, please change it to your needs

        user_base = client["UserData"]
        user_collection = user_base["JointStates"]


        #---------------------------------------------------------------------------------------
        # Switch JointState... below with userdata.entry_data when tests are done
        #entry_data = JointState(position=[1,2,3,4,5,6,7], name=['a','b','c','d', 'e', 'f', 'g'])
        entry_data = userdata.entry_data
        #---------------------------------------------------------------------------------------


        # Check for the last _id value if index id is used, otherwise comment out when usind entry_name as _id
        # Used only for tests!
        #collection_docs = user_collection.find()
        #doc_id_list = []
        #for doc in collection_docs:
        #    doc_id_list.append(doc["_id"])
        #
        #if doc_id_list == []:
        #    self.id_num = 1
        #else:
        #    self.id_num = doc_id_list[-1] + 1       
       
        self.id_num = userdata.entry_name
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
        Logger.loginfo("Written to _id {} into MongoDB".format(self.id_num))
    
        # Uncomment only if you would like to clear collection in Database (delete all documents)
        #cdocs = user_collection.find()
        #del_list = []
        #for d in cdocs:
        #   del_list.append(d["_id"])
        #for i in del_list:
        #   print(i)
        #   user_collection.delete_one({"_id": i})

        return 'continue'
             
    def on_enter(self, userdata):
        rospy.loginfo('On Enter callback happened.')

    def on_exit(self, userdata):
        rospy.loginfo('Exit callback happened.')