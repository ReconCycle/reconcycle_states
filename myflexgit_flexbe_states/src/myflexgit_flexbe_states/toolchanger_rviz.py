#!/usr/bin/env python

import rospy
import tf
from tf import TransformBroadcaster
from rospy import Time
from std_msgs.msg import Float32MultiArray
import numpy as np
from visualization_msgs.msg import Marker
from robot_module_msgs.srv import SetString
from flexbe_core import EventState, Logger
from sensor_msgs.msg import JointState
from robot_module_msgs.msg import JointCommand
import time
import collections

receivedCoords = (0.0, 0.0, 0.0)
receivedEulers = (0.0, 0.0, 0.0)
toolZOffset = 0 
scale = 0.01

class ToolChangerRVIZ(EventState):

    '''
    Uses TransformBroadcaster   
    
    -- tool_name            string  tool name to change tf
    -- destination_name     string  tf to this node
    -- group                string  ns group
    <= continue                     Written successfully
    <= failed                  	    Failed
    '''

    def __init__(self, tool_name, destination_name, group):
        super(ToolChangerRVIZ, self).__init__(outcomes = ['continue', 'failed'])
        # declare tool name
        self.tool_name = tool_name
        self.destination_name = destination_name
        self.b = TransformBroadcaster()
        self.group = group
        self.position_data = [-5.000,-5.000,-5.000,-5.000,-5.000,-5.000,-5.000]
        self.goal_data = [5.000,5.000,5.000,5.000,5.000,5.000,5.000]
            
    def on_enter(self, userdata):
        self.trig = True
        self.j1 = False
        self.j2 = False
        self.j3 = False
        self.j4 = False
        self.j5 = False
        self.j6 = False
        self.j7 = False
        self.sub = rospy.Subscriber('/panda_2/joint_states', JointState, self.callback)
        self.goal_sub = rospy.Subscriber('/panda_2/joint_impedance_controller/command', JointCommand, self.callbacktwo)
        return 'continue'

    def execute(self, userdata):
       
        markerPub = rospy.Publisher('/visualization_marker', Marker, queue_size = 10)
        marker = Marker()
        if not rospy.is_shutdown():
            while self.trig:
                # Prepare TFMessage            
                translation = (receivedCoords[0], receivedCoords[1], receivedCoords[2] + toolZOffset * scale)       
                rotation = receivedEulers
                rotation = tf.transformations.quaternion_from_euler(rotation[0], rotation[1], rotation[2])
                self.b.sendTransform(translation, rotation, Time.now(), str(self.tool_name), str(self.destination_name))
                
                # Prepare Marker message
                marker.header.stamp = Time.now()
                marker.header.frame_id = str(self.tool_name)
                marker.ns = str(self.group)
                marker.id = 0
                marker.type = 9
                marker.pose.position.z = 0
                marker.pose.orientation.z = 1.5
                marker.scale.z = 0.05
                marker.color.b = 1.0
                marker.color.a = 1.0
                marker.text = "TOOL"
                markerPub.publish(marker)

            return 'continue'

        
    def on_exit(self, userdata):
        self.sub.unregister()
        self.goal_sub.unregister()
        return 'continue'

    def callback(self, msg):
        if str(msg.position[2])[0] == '-':
            self.position_data[0] = str(round(msg.position[2],2))[0:4]
            self.position_data[1] = str(round(msg.position[3],2))[0:4]
            self.position_data[2] = str(round(msg.position[4],2))[0:4]
            self.position_data[3] = str(round(msg.position[5],2))[0:4]
            self.position_data[4] = str(round(msg.position[6],2))[0:4]
            self.position_data[5] = str(round(msg.position[7],2))[0:4]
            self.position_data[6] = str(round(msg.position[8],2))[0:4]
        else:
            self.position_data[0] = str(round(msg.position[2],2))[0:3]
            self.position_data[1] = str(round(msg.position[3],2))[0:3]
            self.position_data[2] = str(round(msg.position[4],2))[0:3]
            self.position_data[3] = str(round(msg.position[5],2))[0:3]
            self.position_data[4] = str(round(msg.position[6],2))[0:3]
            self.position_data[5] = str(round(msg.position[7],2))[0:3]
            self.position_data[6] = str(round(msg.position[8],2))[0:3]

        if self.goal_data[0] == self.position_data[0]:
            self.j1 = True

        if  self.goal_data[1] == self.position_data[1]:
            self.j2 = True
        
        if  self.goal_data[2] == self.position_data[2]:
            self.j3 = True
        
        if  self.goal_data[3] == self.position_data[3]:
            self.j4 = True

        if  self.goal_data[4] == self.position_data[4]:
            self.j5 = True

        if  self.goal_data[5] == self.position_data[5]:
            self.j6 = True

        if  self.goal_data[6] == self.position_data[6]:
            self.j7 = True
        
        if self.j1 and self.j2 and self.j3 and self.j4 and self.j5 and self.j6 and self.j7:
            time.sleep(3)
            self.trig = False
            
    def callbacktwo(self, msg):
        if str(msg.pos[0])[0] == '-':
            self.goal_data[0] = str(msg.pos[0])[0:4]
            self.goal_data[1] = str(msg.pos[1])[0:4]
            self.goal_data[2] = str(msg.pos[2])[0:4]
            self.goal_data[3] = str(msg.pos[3])[0:4]
            self.goal_data[4] = str(msg.pos[4])[0:4]
            self.goal_data[5] = str(msg.pos[5])[0:4]
            self.goal_data[6] = str(msg.pos[6])[0:4]

        else:
            self.goal_data[0] = str(msg.pos[0])[0:3]
            self.goal_data[1] = str(msg.pos[1])[0:3]
            self.goal_data[2] = str(msg.pos[2])[0:3]
            self.goal_data[3] = str(msg.pos[3])[0:3]
            self.goal_data[4] = str(msg.pos[4])[0:3]
            self.goal_data[5] = str(msg.pos[5])[0:3]
            self.goal_data[6] = str(msg.pos[6])[0:3]