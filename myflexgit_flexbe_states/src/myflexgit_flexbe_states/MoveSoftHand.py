#!/usr/bin/env python


from flexbe_core.proxy import ProxyPublisher
import actionlib
import rospy
from flexbe_core import EventState, Logger
import robot_module_msgs.msg
from trajectory_msgs.msg import JointTrajectory,JointTrajectoryPoint
import time




class MoveSoftHand(EventState):

    '''
    Calls JointMinJerkAction server @ '/joint_min_jerk_action_server' topic
    [...]
    
    -- motion_duration  float		Speed data
    -- motion_timestep  float		Timestamp data  
    ># goal_joint_pos   string []	Position data input [float, float, ...] of 7 joints
    #< minjerk_out      sting []  	minjerk action server reply userdata output
    <= continue                 Written successfully
    <= failed                  	Failed
    '''

    def __init__(self, motion_duration, motion_timestep):
        super(MoveSoftHand, self).__init__(outcomes = ['continue', 'failed'], input_keys = ['goal_hand_pos'], output_keys = ['success'])

        # actionlib client @joint_min_jerk_action_server
        #FOR NOW #self._client = actionlib.SimpleActionClient('joint_min_jerk_action_server', robot_module_msgs.msg.JointMinJerkAction)
        self._pub=rospy.Publisher('/qbhand1/control/qbhand1_synergy_trajectory_controller/command', JointTrajectory, queue_size=10)
        #self._client = ProxyActionClient({self._topic: robot_module_msgs.msg.JointMinJerkAction}) # pass required clients as dict (topic: type)
        # JointMinJerkAction
        # Input parameters of robot_module_msgs.msg
        self._duration = motion_duration
        self._timestep = motion_timestep

    def execute(self, userdata):
        result = []

        try:
            result = self._client.get_result()
            userdata.minjerk_out = result 
            Logger.loginfo("Action Server reply: \n {}".format(str(userdata.minjerk_out)))
        except Exception as e:
            Logger.loginfo("No result or server is not active!")
            return 'failed'

        return 'continue'
            
    def on_enter(self, userdata):
        # input [float, float, ...] of 7 joints is used for userdata.goal_joint_pos.
        goal = JointTrajectory()

        goal.joint_names(['qbhand1_synergy_joint'])
        point=JointTrajectoryPoint()

        goal.points

        Logger.loginfo("Starting sending goal...")

        try:
            Logger.loginfo("Goal sent: {}".format(str(userdata.goal_joint_pos)))
            self._client.send_goal(goal)
            while self._client.get_result() == None:
                Logger.loginfo("{}".format(robot_module_msgs.msg.JointMinJerkFeedback()))
                time.sleep(0.2)

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





if __name__ == '__main__':

    print("Testing standalone")

    class userdata():

        def __init__(self):

            self.goal_joint_pos=[0.5]


    rospy.init_node('test_node')
    test_state=MoveSoftHand(3,0.1)
    test_state.on_enter(userdata)