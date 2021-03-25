#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from myflexgit_flexbe_states.ExecuteJointDMPfromMongoDB import ExeJointDMP
from myflexgit_flexbe_states.avtivate_raspi_output import ActivateRaspiDigitalOuput
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Jan 18 2021
@author: Rok Pahic
'''
class TestDMPexecutionSM(Behavior):
	'''
	Testing DMP execution on robot 2
	'''


	def __init__(self):
		super(TestDMPexecutionSM, self).__init__()
		self.name = 'TestDMPexecution'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:287 y:595, x:55 y:600
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.PA_start_joint_pos = [-1.31,-0.08,-0.21,-1.618,-0.103,1.68,0.97]
		_state_machine.userdata.trj_name = 'breaking_object_test'
		_state_machine.userdata.PA_pick_joint_pos = [0.14161578650850998, -1.5168914103295907, -2.1584001102049624, -1.8599657923756354, -1.8240628920282174, 3.4166442354520155, 0.7055232277431606]
		_state_machine.userdata.hand_grab_positon = [0.6]
		_state_machine.userdata.hand_release_positon = [0.1]
		_state_machine.userdata.PA_drop_joint_pos = [1.1941379129761143, -1.3262326462394314, -1.6472267352773604, -2.5728268495777202, -1.9003523117568755, 3.024962522929494, 1.016712569170942]
		_state_machine.userdata.True1 = True
		_state_machine.userdata.False1 = False

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:30 y:125
			OperatableStateMachine.add('Clamp',
										ActivateRaspiDigitalOuput(service_name='/obr_activate'),
										transitions={'continue': 'Execute test DMP', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Low, 'failed': Autonomy.Low},
										remapping={'value': 'True1', 'success': 'success'})

			# x:267 y:92
			OperatableStateMachine.add('Execute test DMP',
										ExeJointDMP(time_scale=1, motion_timestep=0.01, robot_namespace='panda_2', max_vel=0.3, max_acl=0.3),
										transitions={'continue': 'finished', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Low, 'failed': Autonomy.Low},
										remapping={'entry_name': 'trj_name', 'success': 'success'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
