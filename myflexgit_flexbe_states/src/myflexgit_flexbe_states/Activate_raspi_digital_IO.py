#!/usr/bin/env python


from flexbe_core.proxy import ProxyPublisher

import rospy
from flexbe_core import EventState, Logger
import time
from digital_interface_msgs.msg import DigitalState



class Activate_raspi_digital_IO(EventState):

    '''
    Calls service conected to raspberry GPIO
    [...]
    
    -- service_name  string		Speed data

    ># Digital_IO_value   bool	desired value
    #< success      bool  	check execution
    <= continue                 Written successfully
    <= failed                  	Failed
    '''

    def __init__(self, service_name):
        super(Activate_raspi_digital_IO, self).__init__(outcomes = ['continue', 'failed'], input_keys = ['value',], output_keys = ['success'])

        
        self._pub=ProxyPublisher({service_name: DigitalState})
        #self._client = ProxyActionClient({self._topic: robot_module_msgs.msg.JointMinJerkAction}) # pass required clients as dict (topic: type)
     
        self._service_name = service_name
   

    def execute(self, userdata):
 

        return 'continue'
            
    def on_enter(self, userdata):
        
        state = DigitalState()

        state.value=1
     

        Logger.loginfo("Set digital IO...")

        self._pub.publish(self._service_name,state)

        try:
            #Logger.loginfo("Goal sent: {}".format(str(userdata.goal_joint_pos)))
            self._pub.publish(self._service_name,state)
     

        except Exception as e:
            print(e)
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

            self.value=True


    rospy.init_node('test_node')
    test_state= Activate_raspi_digital_IO('testing')
    print('sleep')
    rospy.sleep(5)
    print('sleep')
    test_state.on_enter(userdata)
    rospy.spin()