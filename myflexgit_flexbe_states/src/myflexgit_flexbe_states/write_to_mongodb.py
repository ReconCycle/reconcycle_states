#!/usr/bin/env python

import rospy
import mongodb_store_msgs.srv as dc_srv
#import mongodb_store.util as dc_util 
from mongodb_store.message_store import MessageStoreProxy
from flexbe_core import EventState, Logger
from sensor_msgs.msg import JointState
import StringIO

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
        self.reachable = True

        self.msg_store = MessageStoreProxy()

    def execute(self, userdata):
        #---------------------------------------------------------------------------------------
        # userdata.entry_data in JointState format, userdata.entry_name as store id name
        entry_data = userdata.entry_data
        entry_name = str(userdata.entry_name)
        #---------------------------------------------------------------------------------------

        # Write to MongoDB        
        Logger.loginfo("Writing to mongoDB _id: {}...".format(entry_name))

        pos = JointState(position=entry_data)
        
        try: 
            if self.msg_store.query_named(entry_name, JointState.position):
                client= self.msg_store.update_named(entry_name, pos)
            else:
                client = self.msg_store.insert_named(entry_name, pos)
                   
            Logger.loginfo("Written successfully!")

        except rospy.ServiceException as e:
            Logger.loginfo("MongoDB is not reachable...")
            self.reachable = False
    
        return 'continue'
             
    def on_enter(self, userdata):
        Logger.loginfo('Starting write to MongoDB...')

    def on_exit(self, userdata):
        if self.reachable:
            Logger.loginfo("Finished writting to MongoDB!")
        else:
            Logger.loginfo("Could not write to MongoDB!")
