#!/usr/bin/python3

import actionlib
import rospy
from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxyActionClient
from sensor_msgs.msg import JointState
from actionlib_msgs.msg import GoalStatus
import robot_module_msgs.msg

class CallJointTrap(EventState):

    '''
    Calls JointTrapVelAction server @ 'joint_trap_vel_action_server' topic
    [...]

    ># joints_data string/int      The name under which the name is written into MongoDB

    #< joint_values []    The data read from mongoDB from specific _id (entry_name)

    <= continue                     Written successfully
    <= failed                       Failed
    '''

    def __init__(self):
        super(CallJointTrap, self).__init__(outcomes = ['continue', 'failed'], input_keys = ['joints_data'], output_keys = ['joint_values'])

        # replace 'panda_2/joint_trap_vel_action_server' from dummies with 'joint_trap_vel_action_server'
        #self._topic = 'panda_2/joint_trap_vel_action_server'
        self._topic = 'joint_trap_vel_action_server'
        self._client = actionlib.SimpleActionClient(self._topic, robot_module_msgs.msg.JointTrapVelAction)
        #self._client = ProxyActionClient({self._topic: robot_module_msgs.msg.JointTrapVelAction}) # pass required clients as dict (topic: type)
        # JointTrapVelAction

		# It may happen that the action client fails to send the action goal.

    def execute(self, userdata):
        result = ...

        try:
            result = self._client.get_result()
            userdata.joint_values = result 
            Logger.loginfo("Action Server reply: \n {}".format(str(userdata.joint_values)))
        except Exception as e:
            Logger.loginfo("No result or server is not active!")
            return 'failed'

        return 'continue'
            
    def on_enter(self, userdata):
        # JointState() is used for tests. Replace JointState() with userdata.joints_data.
        self.goal_joint = userdata.joints_data #JointState()
        goal = robot_module_msgs.msg.JointTrapVelGoal([self.goal_joint], 0.05, None)
        Logger.loginfo("Starting sending goal...")

        try:
            self._client.send_goal_and_wait(goal, execute_timeout=rospy.Duration(5))
            Logger.loginfo("Goal sent: {}".format(str(self.goal_joint)))
        except Exception as e:
			# Since a state failure not necessarily causes a behavior failure, it is recommended to only print warnings, not errors.
			# Using a linebreak before appending the error log enables the operator to collapse details in the GUI.
            Logger.loginfo('Failed to send the goal command:\n{}'.format(str(e)))
            self._error = True

    def on_exit(self, userdata):
        if not self._client.get_result():
            self._client.cancel_goal()
            Logger.loginfo('Cancelled active action goal.')
        Logger.loginfo('Finished sending goal to JointTrapVelGoal.')
        return 'continue'
        