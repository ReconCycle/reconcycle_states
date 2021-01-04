#!/usr/bin/python3

import actionlib
import rospy
from flexbe_core import EventState, Logger
import robot_module_msgs.msg

class CallJointMinJerk(EventState):

    '''
    Calls JointMinJerkAction server @ 'joint_min_jerk_action_server' topic
    [...]
    
    -- positions	string []	Position data input [float, float, ...] of 7 joints
    -- speed		float		Speed data
    -- timestep	    float		Timestamp data
    #< minjerk_out	[]  		minjerk action server reply userdata output
    <= continue                 Written successfully
    <= failed                  	Failed
    '''

    def __init__(self, positions, speed, timestep):
        super(CallJointMinJerk, self).__init__(outcomes = ['continue', 'failed'], output_keys = ['minjerk_out'])

        # replace 'panda_2/joint_min_jerk_action_server' from dummies with 'joint_min_jerk_action_server'
        #self._topic = 'panda_2/joint_min_jerk_action_server'
        self._topic = '/joint_min_jerk_action_server'
        self._client = actionlib.SimpleActionClient(self._topic, robot_module_msgs.msg.JointMinJerkAction)

        self._client.wait_for_server()
        #self._client = ProxyActionClient({self._topic: robot_module_msgs.msg.JointMinJerkAction}) # pass required clients as dict (topic: type)
        # JointMinJerkAction
        # Input parameters of robot_module_msgs.msg
        self._position = positions
        self._speed = speed
        self._timestep = timestep

    def execute(self, userdata):
        result = ...

        try:
            result = self._client.get_result()
            userdata.minjerk_out = result 
            Logger.loginfo("Action Server reply: \n {}".format(str(userdata.minjerk_out)))
        except Exception as e:
            Logger.loginfo("No result or server is not active!")
            return 'failed'

        return 'continue'
            
    def on_enter(self, userdata):
        # input [float, float, ...] of 7 joints is used for self.goal_minjerk.
        self.goal_minjerk = self._position
        goal = robot_module_msgs.msg.JointMinJerkGoal(self.goal_minjerk, self._speed, self._timestep)
        Logger.loginfo("Starting sending goal...")

        try:
            self._client.send_goal_and_wait(goal, execute_timeout=rospy.Duration(5))
            Logger.loginfo("Goal sent: {}".format(str(self.goal_minjerk)))
        except Exception as e:
			# Since a state failure not necessarily causes a behavior failure, it is recommended to only print warnings, not errors.
			# Using a linebreak before appending the error log enables the operator to collapse details in the GUI.
            Logger.loginfo('Failed to send the goal command:\n{}'.format(str(e)))
            self._error = True

    def on_exit(self, userdata):
        if not self._client.get_result():
            self._client.cancel_goal()
            Logger.loginfo('Cancelled active action goal. No reply data.')
        Logger.loginfo('Finished sending goal to JointMinJerkGoal.')
        return 'continue'
        
