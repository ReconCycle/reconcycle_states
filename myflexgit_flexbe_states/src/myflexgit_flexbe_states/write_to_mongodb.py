#!/usr/bin/python3
from genpy.rostime import Duration
import rospy
from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxyActionClient
from sensor_msgs.msg import JointState
import robot_module_msgs.msg

class WriteToMongo(EventState):

    def __init__(self, inputs):
        super(WriteToMongo, self).__init__(outcomes = ['continue', 'failed'], input_keys = ['joint_numbers'], output_keys = ['joint_values'])

        self._in = inputs
        self._joint_trap_vel = '/joint_trap_vel_action_server'
        self._merger = [self._in, self._joint_trap_vel]
        self._topic = ''.join(self._merger)
        self._client = ProxyActionClient({self._topic: robot_module_msgs.msg.JointTrapVelAction}) # pass required clients as dict (topic: type)
        # JointTrapVelAction

		# It may happen that the action client fails to send the action goal.
        self._error = False
    
    def execute(self, userdata):
        if self._error:
            return 'failed'

    
        #if self._client.has_result(self._topic):
        result = self._client.get_result(self._topic)
        rospy.loginfo(result)
        # else:
        #    rospy.loginfo('No >get_result< data!')        

    def on_enter(self, userdata):
        goal_joint = JointState()
        goal = robot_module_msgs.msg.JointTrapVelGoal([goal_joint], 0.05, None)

        try:
            self._client.send_goal(self._topic, goal)
            rospy.loginfo("Goal sent!")
        except Exception as e:
			# Since a state failure not necessarily causes a behavior failure, it is recommended to only print warnings, not errors.
			# Using a linebreak before appending the error log enables the operator to collapse details in the GUI.
            rospy.loginfo('Failed to send the goal command:\n%s' % str(e))
            self._error = True

    def on_exit(self, userdata):
        if not self._client.has_result(self._topic):
            self._client.cancel(self._topic)
        rospy.loginfo('Cancelled active action goal.')

if __name__ == '__main__':
    rospy.init_node("Mynode")
    WriteToMongo('panda_2').execute(None)