#!/usr/bin/python3

import rospy
from geometry_msgs.msg import Pose
import tf
from flexbe_core import EventState, Logger
import robot_module_msgs.msg
import actionlib


class ReadT1(EventState):
    
    '''
    Implements a state that reads TF data
    [...]       

    #< t1_data  Pose()              Read a frame from TF

    ># target1  userdata.target     Transform this frame

    <= continue                     Written successfully
    <= failed                       Failed
    '''

    def __init__(self):
        rospy.loginfo('__init__ callback happened.')   
        super(ReadT1, self).__init__(outcomes = ['continue', 'failed'], input_keys =['target1'], output_keys = ['t1_data'])
        
  
    def on_enter(self, userdata):
        self.listener = tf.TransformListener()  
        Logger.loginfo("Started reading TF (Cart)...")
        try:
            if 'target1' in userdata:
                self.target_frame = userdata.target1
            else:
                raise ValueError('Target frame should be specified in userdata as \'target1\'!')
        except Exception as e:
            Logger.loginfo('Targer frame not in Pose() structure')
        
    def execute(self, userdata):
        (trans, rot) = self.listener.lookupTransform(self.target_frame, self.target_frame, rospy.Time(0))
        Logger.loginfo("target1: {}".format(userdata.target1))
        Logger.loginfo("trans: {}".format(trans))
        Logger.loginfo("rot: {}".format(rot))

        data = Pose()
        data.position.x = trans[0]
        data.position.y = trans[1]
        data.position.z = trans[2]
        data.orientation.x = rot[0]
        data.orientation.y = rot[1]
        data.orientation.z = rot[2]
        data.orientation.w = rot[3]
        Logger.loginfo("Pose data from TF (Cart): {}".format(data))
        userdata.t1_data = data
        return 'continue'  

    def on_exit(self, userdata):
        Logger.loginfo('Exiting read TF (Cart).')
        return 'continue'