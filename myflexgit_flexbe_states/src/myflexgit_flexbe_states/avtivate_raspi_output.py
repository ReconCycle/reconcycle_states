#!/usr/bin/env python


from flexbe_core.proxy import ProxyPublisher
from flexbe_core.proxy import ProxyServiceCaller

import rospy
from flexbe_core import EventState, Logger
import time
from digital_interface_msgs.msg import DigitalState
from digital_interface_msgs.srv import PinStateWrite,PinStateWriteRequest


class ActivateRaspiDigitalOuput(EventState):

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
        super(ActivateRaspiDigitalOuput, self).__init__(outcomes = ['continue', 'failed'], input_keys = ['value'], output_keys = ['success'])

        
        self._pub=ProxyPublisher({service_name: DigitalState})
        self._srv=ProxyServiceCaller({service_name: PinStateWrite})
        
        #self._client = ProxyActionClient({self._topic: robot_module_msgs.msg.JointMinJerkAction}) # pass required clients as dict (topic: type)
     
        self._service_name = service_name
   

    def execute(self, userdata):
 

        return 'continue'
            
    def on_enter(self, userdata):
        
        state = PinStateWriteRequest()

        state.value = userdata.value
     
        

        Logger.loginfo("Set digital Output...")

   

        try:
            #Logger.loginfo("Goal sent: {}".format(str(userdata.goal_joint_pos)))
            self._srv.call(self._service_name,state)
     

        except Exception as e:
            print(e)
            # Since a state failure not necessarily causes a behavior failure, it is recommended to only print warnings, not errors.
			# Using a linebreak before appending the error log enables the operator to collapse details in the GUI.
            Logger.loginfo('Failed to set digital output:\n{}'.format(str(e)))
            self._error = True

    def on_exit(self, userdata):

        return 'continue'





if __name__ == '__main__':

    print("Testing standalone")

    class userdata():

        def __init__(self):

            self.value=False


    rospy.init_node('test_node')
    test_state= ActivateRaspiDigitalOuput('tool_changer_unlock')
    print('sleep')
    rospy.sleep(2)
    print('sleep')
    user_test=userdata()
    test_state.on_enter(user_test)
    test_state.execute(user_test)
    test_state.on_exit(user_test)
    #rospy.spin()