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

    ># target2  userdata.target2    Transform this frame

    <= continue                     Written successfully
    <= failed                       Failed
    '''

    def __init__(self):
        rospy.loginfo('__init__ callback happened.')   
        super(ReadT2, self).__init__(outcomes = ['continue', 'failed'], input_keys =['target2'], output_keys = ['t2_data'])
        
  
    def on_enter(self, userdata):
        self.listener = tf.TransformListener()  
        try:
            if 'target2' in userdata:
                self.target_frame = userdata.target2
            else:
                raise ValueError('Target frame should be specified in userdata as \'target2\'!')
        except Exception as e:
            Logger.loginfo('Targer frame not in Pose() structure')
        
    def execute(self, userdata):
        (trans, rot) = self.listener.lookupTransform(self.target_frame, self.target_frame, rospy.Time(0))
        Logger.loginfo("target2: {}".format(userdata.target2))
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
        Logger.loginfo("Pose data: {}".format(data))
        userdata.t2_data = data
        return 'continue'  

    def on_exit(self, userdata):
        Logger.loginfo('Exiting lookupTransform of provided target')
        return 'continue'