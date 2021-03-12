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

from robot_module_msgs.msg import JointSpaceDMP


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
        super( ExeJointDMP, self).__init__(outcomes = ['continue', 'failed'], input_keys = ['entry_name'], output_keys = ['success'])
        Logger.loginfo("INIT...DMP execution")

        self._robot_namespace = robot_namespace


        self._move_joint_topic = self._robot_namespace + '/joint_min_jerk_action_server'
        self._execute_DMP_topic = self._robot_namespace + '/joint_DMP_action_server'


        # Client for reading from mongoDB

        self._client_mongodb  = MessageStoreProxy()
        
        # Action client for moving on start position 

        # Action client for executing DMP

        self._client = ProxyActionClient({ self._move_joint_topic: JointMinJerkAction,self._execute_DMP_topic: JointDMPAction})


     


        self._time_scale=time_scale
        self._timestep = motion_timestep
        self._duration = 6
        
    def on_enter(self, userdata):

        Logger.loginfo("Reading from DMP from MongoDB base: \n {}".format('DMP name'+userdata.entry_name))




      

    def execute(self, userdata):

        #Read from mongo db 
     
        Logger.loginfo("Reading _id: {} DMP from mongoDB: ... \n ".format(userdata.entry_name))  
 

        try:
   
            data_from_db = self._client_mongodb.query_named(userdata.entry_name, JointSpaceDMP._type)
            
            DMP=data_from_db[0]
        except rospy.ServiceException as e:
    
            Logger.loginfo("MongoDB is not reachable...")
            self.reachable = False
            return 'failed'

        #Move robot on DMP starting postion y0
        Logger.loginfo("Move robot on DMP starting postion y0...")

       
        
        start_goal = JointMinJerkGoal(DMP.y0.position, self._duration, self._timestep)
        

        try:
            Logger.loginfo("Start position sent: {}".format(DMP.y0.position))


            self._client.send_goal(self._move_joint_topic,start_goal)
            timeout = time.time()
            while self._client.get_result(self._move_joint_topic) == None:

                feedback = self._client.get_feedback(self._move_joint_topic)
                Logger.loginfo("{}".format(feedback))
                time.sleep(0.5)
                # 12 secs timeout
                if time.time()-timeout > 12:
                    break

        except Exception as e:
            # Since a state failure not necessarily causes a behavior failure, it is recommended to only print warnings, not errors.
			# Using a linebreak before appending the error log enables the operator to collapse details in the GUI.
            Logger.loginfo('Failed to send the starting point command:\n{}'.format(str(e)))
            self._error = True
            return 'failed'

        #Execute DMP 
        Logger.loginfo("Execute DMP ...")

        
        dmp_goal = JointDMPGoal(DMP)
        

        try:
            #Logger.loginfo("DMP sent: {}".format(DMP))


            self._client.send_goal(self._execute_DMP_topic,dmp_goal)
            timeout = time.time()
            while self._client.get_result(self._execute_DMP_topic) == None:
                time.sleep(0.5)
                feedback = self._client.get_feedback(self._execute_DMP_topic)
                
                
                Logger.loginfo("{}".format(str(feedback.joints.position)))

                
                # 12 secs timeout
                if time.time()-timeout > 12:
                    break

            return 'continue'

        except Exception as e:
            # Since a state failure not necessarily causes a behavior failure, it is recommended to only print warnings, not errors.
			# Using a linebreak before appending the error log enables the operator to collapse details in the GUI.
            Logger.loginfo('Failed to send DMP:\n{}'.format(str(e)))
            self._error = True
            return 'failed'      




            
   

    def on_exit(self, userdata):

        Logger.loginfo('Finished sending goal to hand. TEST0')
        if not self._client.get_result(self._execute_DMP_topic):
            self._client.cancel(self._execute_DMP_topic)
            Logger.loginfo('Cancelled active action goal. No reply data. TEST')
        Logger.loginfo('Finished sending goal to hand. TEST')
        return 'continue'





if __name__ == '__main__':

    print("Testing standalone")

    class userdata():

        def __init__(self,name):

            self.entry_name=name

    usertest=userdata("trj1")
    rospy.init_node('test_node')
    test_state=ExeJointDMP(1,0.1,'/panda1')

    test_state.on_enter(usertest)
    test_state.execute(usertest)
    #test_state.on_exit(usertest)