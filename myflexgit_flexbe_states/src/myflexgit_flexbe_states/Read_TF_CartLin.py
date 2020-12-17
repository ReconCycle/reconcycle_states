#!/usr/bin/python3

import rospy
from geometry_msgs.msg import Pose
import tf
from flexbe_core import EventState, Logger
import robot_module_msgs.msg
import actionlib


class ReadT2(EventState):
    
    '''
    Implements a state that reads TF data
    [...]       

    #< t2_data  Pose()              Read a frame from TF

    ># target2_frame  userdata.target2_frame    Transform this frame
    ># source_frame  userdata.target1

    <= continue                     Written successfully
    <= failed                       Failed
    '''

    def __init__(self):
        rospy.loginfo('__init__ callback happened.')   
        super(ReadT2, self).__init__(outcomes = ['continue', 'failed'], input_keys =['target2_frame', 'source_frame'], output_keys = ['t2_data'])
        
  
    def on_enter(self, userdata):
        Logger.loginfo("Started reading TF (CartLin)...")
        self.listener = tf.TransformListener()  
        try:
            if 'target2_frame' in userdata:
                self.target2_frame = userdata.target2_frame
                self.source_frame = userdata.source_frame
            else:
                raise ValueError('Target frame should be specified in userdata as \'target2\' and \'target1\'!')
        except Exception as e:
            Logger.loginfo('Targer frame not in Pose() structure')
        
    def execute(self, userdata):
        try:
            #self.listener.waitForTransform(userdata.target2_frame, userdata.source_frame, rospy.Time.now(), rospy.Duration(4.0))
            (trans, rot) = self.listener.lookupTransform(self.target2_frame, self.source_frame, rospy.Time(0))
            Logger.loginfo("target: {}".format(userdata.target2_frame))
            Logger.loginfo("source: {}".format(userdata.source_frame))
            Logger.loginfo("trans: {}".format(trans))
            Logger.loginfo("rot: {}".format(rot))
        except (tf.LookupException, tf.ConnectivityException):
            return 'failed'

        data = Pose()
        data.position.x = trans[0]
        data.position.y = trans[1]
        data.position.z = trans[2]
        data.orientation.x = rot[0]
        data.orientation.y = rot[1]
        data.orientation.z = rot[2]
        data.orientation.w = rot[3]
        Logger.loginfo("Pose data from tf (CartLin): {}".format(data))
        userdata.t2_data = data
        return 'continue'  

    def on_exit(self, userdata):
        Logger.loginfo('Exiting read TF (CartLin).')
        return 'continue'