#!/usr/bin/python3

import rospy
from geometry_msgs.msg import Pose
import tf
from flexbe_core import EventState, Logger
import robot_module_msgs.msg
import actionlib


class CallT2(EventState):
    
    '''
    Implements a state that reads TF data
    [...]       

    #< t2_out       Data                Send TF data

    ># t2_data      Pose()              Data from target  

    <= continue                         Written successfully
    <= failed                           Failed
    '''

    def __init__(self):
        rospy.loginfo('__init__ callback happened.')   
        super(CallT2, self).__init__(outcomes = ['continue', 'failed'], input_keys = ['t2_data'], output_keys = ['t2_out'])
        
        # After thest change 'panda_2/cart_trap_vel_action_server' to 'cart_trap_vel_action_server' !
        self._topic = 'panda_1/cart_lin_task_action_server'
        self._client = actionlib.SimpleActionClient(self._topic, robot_module_msgs.msg.CartLinTaskAction)

    def on_enter(self, userdata):
        # After test change Pose(position =[1, 1, 1], orientation = [0, 0, 0, 1]) to userdata.pose_data
        test = Pose()
        self.goal_pose = userdata.t2_data
        goal = robot_module_msgs.msg.CartLinTaskGoal([self.goal_pose], 0.05, None)    
        
        self._client.send_goal(goal)
        self._client.wait_for_result()
        Logger.loginfo("Goal sent: {}".format(str(self.goal_pose)))
              
        self.result = self._client.get_result()
        Logger.loginfo("Action Server reply: \n {}".format(str(self.result)))    
        
    
    def execute(self, userdata):
        #self.listener = tf.TransformListener()  
        userdata.t2_out = self.result      
    
        return 'continue'
        

    def on_exit(self, userdata):
        Logger.loginfo('Exiting CartLinTaskAction state')
        return 'continue'


