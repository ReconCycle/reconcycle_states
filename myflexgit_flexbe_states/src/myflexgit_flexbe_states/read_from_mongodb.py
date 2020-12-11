#!/usr/bin/python3

from pymongo import database
from genpy.rostime import Duration
import rospy
from flexbe_core import EventState, Logger
from sensor_msgs.msg import JointState
import pymongo


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
        rospy.loginfo('__init__ callback happened.')
        print("INIT")        
        super(ReadFromMongo, self).__init__(outcomes = ['continue'], input_keys = ['entry_name'], output_keys = ['joints_data'])

    def execute(self, userdata):
        print("execute")
        rospy.loginfo('Execute callback happened.')
        client = pymongo.MongoClient('mongodb://localhost:27017/')  # if server does not run locally, please change it to your needs


        # define base created @write_to_mongo -> "UserData"
        user_base = client["UserData"]
        # define collection where data is written to at write_to_mongo -> "JointStates"
        user_collection = user_base["JointStates"]

        # replace " 1 " @selected_id with userdata.entry_name after tests
        selected_id = userdata.entry_name
        # find collection from input_keys -> entry_name
        collection_docs = user_collection.find({"_id": selected_id})

        # declaring output data structure as JointStates() structure
        output_data = JointState()
        
        _header = ...
        _name = ...
        _position = ...
        _velocity = ...
        _effort = ...
        _seq = ...
        _stamp = ...
        _secs = ...
        _nsecs = ...
        _frame_id = ...
        

        for i in collection_docs:
            _header = i['header']
            _name = i['name']
            _position = i['position']
            _velocity = i['velocity']
            _effort = i['effort']

        _seq = _header['seq']
        _stamp = _header['stamp']
        _frame_id = _header['frame_id']

        _secs = _stamp['secs']
        _nsecs = _stamp['nsecs']        
        
 
        # adding data from 'entry_name' _id collection to defined construction
        output_data.header.seq = _seq
        output_data.header.stamp.secs = _secs
        output_data.header.stamp.nsecs = _nsecs
        output_data.header.frame_id = _frame_id
        output_data.name = _name
        output_data.position = _position
        output_data.velocity = _velocity
        output_data.effort = _effort
        
        
        # data output to output_keys -> 'joints_data'
        userdata.joints_data = output_data
        Logger.loginfo("Reading _id: {} from mongoDB: \n {}".format(selected_id, userdata.joints_data))      
        return 'continue'  
            
    def on_enter(self, userdata):
        rospy.loginfo('On Enter callback happened.')

    def on_exit(self, userdata):
        rospy.loginfo('Exit callback happened.')
        