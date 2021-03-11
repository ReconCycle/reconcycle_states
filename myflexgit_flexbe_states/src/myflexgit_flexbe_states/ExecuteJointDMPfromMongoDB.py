#!/usr/bin/env python


#ros stuf
import rospy


#flexbe stuff
from flexbe_core import EventState, Logger

from flexbe_core.proxy import ProxyActionClient

#mongo stuff
from mongodb_store.message_store import MessageStoreProxy

import time

# Action messages
from robot_module_msgs.msg import JointDMPAction,JointDMPFeedback,JointDMPGoal
from robot_module_msgs.msg import JointMinJerkAction,JointMinJerkFeedback,JointMinJerkGoal

class ExeJointDMP(EventState):

    '''
    Calls qb hand server
    [...]
    
    -- time scale      float	Scale Tau of DMP trajectory
    -- motion_timestep  float		Timestamp data  
    ># goal_hand_pos   string []	Position data input [float] of 1 joint
    #< success     bool 	minjerk action server reply userdata output
    <= continue                 Written successfully
    <= failed                  	Failed
    '''

    def __init__(self, time_scale, motion_timestep, robot_namespace=''):
        super( ExeJointDMP, self).__init__(outcomes = ['continue', 'failed'], input_keys = ['entry name'], output_keys = ['success'])
        Logger.loginfo("INIT...DMP execution")

        self._robot_namespace = robot_namespace


        self._move_joint_topic = self._robot_namespace + '/joint_DMP_action_server'

        self._execute_DMP_topic = self._robot_namespace + '/joint_min_jerk_action_server'

        # Client for reading from mongoDB

        self._client_mongodb  = MessageStoreProxy()
        
        # Action client for moving on start position 

        # Action client for executing DMP

        self._client = ProxyActionClient({ self._move_joint_topic: JointMinJerkAction,self._execute_DMP_topic: JointDMPAction})


     


        self._time_scale=time_scale
        self._timestep = motion_timestep

    def execute(self, userdata):
        result = []
        Logger.loginfo("Execute...TEST")
        try:
            result = self._client.get_result(self._topic)

            Logger.loginfo("Action Server reply: \n {}".format(str(result)))
        except Exception as e:
            Logger.loginfo("No result or server is not active!")
            return 'failed'

        return 'continue'
            
    def on_enter(self, userdata):


        goal = FollowJointTrajectoryGoal()

        goal.trajectory.joint_names=['qbhand1_synergy_joint']


        point=JointTrajectoryPoint()
        point.positions=userdata.goal_hand_pos
        point.time_from_start = self._duration

        goal.trajectory.points=[point]


        Logger.loginfo("Starting sending goal...TEST")

        try:
            Logger.loginfo("Goal sent: {}".format(str(userdata.goal_hand_pos)))
            self._client.send_goal(self._topic,goal)
            while self._client.get_result(self._topic) == None:
                Logger.loginfo("{}".format(robot_module_msgs.msg.JointMinJerkFeedback()))
                time.sleep(0.2)

        except Exception as e:
            # Since a state failure not necessarily causes a behavior failure, it is recommended to only print warnings, not errors.
			# Using a linebreak before appending the error log enables the operator to collapse details in the GUI.
            Logger.loginfo('Failed to send the goal command:\n{}'.format(str(e)))
            self._error = True

    def on_exit(self, userdata):

        Logger.loginfo('Finished sending goal to hand. TEST0')
        if not self._client.get_result(self._topic):
            self._client.cancel_goal(self._topic)
            Logger.loginfo('Cancelled active action goal. No reply data. TEST')
        Logger.loginfo('Finished sending goal to hand. TEST')
        return 'continue'





if __name__ == '__main__':

    print("Testing standalone")

    class userdata():

        def __init__(self,pos):

            self.goal_hand_pos=[pos]

    usertest=userdata(0.1)
    rospy.init_node('test_node')
    test_state=ExeJointDMP(1,0.1,'/panda1')

    #test_state.on_enter(usertest)
    #test_state.on_exit(usertest)
    #test_state.on_exit(usertest)