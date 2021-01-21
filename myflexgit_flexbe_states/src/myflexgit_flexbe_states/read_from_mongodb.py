#!/usr/bin/python3

import rospy
import mongodb_store_msgs.srv as dc_srv
import mongodb_store.util as dc_util
from mongodb_store.message_store import MessageStoreProxy
from flexbe_core import EventState, Logger
from sensor_msgs.msg import JointState

class ReadFromMongo(EventState):

    '''
    Implements a state that writes data to MongoDB
    [...]

    ># entry_name string/int      The name under which the name is written into MongoDB

    #< joints_data JointState()    The data read from mongoDB from specific _id (entry_name)

    <= continue                     Written successfully
    <= failed                       Failed
    '''
    

    #-- calculation  function        The function that performs [...]
    def __init__(self):      
        super(ReadFromMongo, self).__init__(outcomes = ['continue', 'failed'], input_keys = ['entry_name'], output_keys = ['joints_data'])
        self.reachable = True

        self.msg_store = MessageStoreProxy()

    def execute(self, userdata):
        pos = JointState()
        try:
            data_from_db = self.msg_store.query_named(str(userdata.entry_name), JointState._type)

            Logger.loginfo("Data read: \n {}".format(data_from_db))
            Logger.loginfo("Position data: \n {}".format(data_from_db(position)))

        except rospy.ServiceException as e:
            Logger.loginfo("MongoDB is not reachable...")
            self.reachable = False
            return 'failed'

        userdata.joints_data = data_from_db(position)
        Logger.loginfo("Reading _id: {} from mongoDB: ... \n {}".format(userdata.entry_name, userdata.joints_data))      
        return 'continue'  
            
    def on_enter(self, userdata):
        Logger.loginfo("Starting read from MongoDB...")

    def on_exit(self, userdata):
        if self.reachable:
            Logger.loginfo("Finished reading from MongoDB.")
        else:
            Logger.loginfo("Could not read from MongoDB!")
        
