#!/usr/bin/python3

import rospy
from geometry_msgs.msg import Pose, PoseStamped
import tf
from flexbe_core import EventState, Logger
import robot_module_msgs.msg


class ReadT1(EventState):
    
    '''
    Implements a state that reads TF data
    [...]       

    #< t1_data  Pose()              Read a frame from TF

    ># target1_frame  userdata.target1    Transform this frame
    ># source_frame  userdata.target2    Transform this frame

    <= continue                     Written successfully
    <= failed                       Failed
    '''

    def __init__(self):
        rospy.loginfo('__init__ callback happened.')   
        super(ReadT1, self).__init__(outcomes = ['continue', 'failed'], input_keys =['target1_frame', 'source_frame'], output_keys = ['t1_data'])
        
  
    def on_enter(self, userdata):
        self.listener = tf.TransformListener()  
        Logger.loginfo("Started reading TF (Cart)...")
        try:
            if 'target1_frame' in userdata:
                self.target1_frame = userdata.target1_frame
                self.source_frame = userdata.source_frame
            else:
                raise ValueError('Target frame should be specified in userdata as \'target1_frame\'!')
        except Exception as e:
            Logger.loginfo('Targer frame not in Pose() structure')
            return 'failed'
        
    def execute(self, userdata):
        try:            
            #self.listener.waitForTransform(userdata.target1_frame, userdata.source_frame, rospy.Time.now(), rospy.Duration(4.0))
            (trans, rot) = self.listener.lookupTransform(self.target1_frame, self.source_frame, rospy.Time(0))
            Logger.loginfo("target: {}".format(userdata.target1_frame))
            Logger.loginfo("source: {}".format(userdata.source_frame))
            Logger.loginfo("trans: {}".format(trans))
            Logger.loginfo("rot: {}".format(rot))
        except (tf.LookupException, tf.ConnectivityException):
            Logger.loginfo("lookup")
            return 'failed'

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