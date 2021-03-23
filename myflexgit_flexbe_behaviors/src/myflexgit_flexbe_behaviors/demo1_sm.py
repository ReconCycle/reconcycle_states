#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from myflexgit_flexbe_states.MoveSoftHand import MoveSoftHand
from myflexgit_flexbe_states.avtivate_raspi_output import ActivateRaspiDigitalOuput
from myflexgit_flexbe_states.call_joint_trap_vel_action_server import CallJointTrap
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Jan 18 2021
@author: Rok Pahic
'''
class Demo1SM(Behavior):
	'''
	Testing Pick and drop in Reconcycle
	'''


	def __init__(self):
		super(Demo1SM, self).__init__()
		self.name = 'Demo1'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1161 y:653, x:55 y:600
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.PA_start_joint_pos = [-1.31,-0.08,-0.21,-1.618,-0.103,1.68,0.97]
		_state_machine.userdata.entry_name = 'test flexbe'
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
			# x:30 y:40
			OperatableStateMachine.add('Move to start',
										CallJointTrap(max_vel=0.5, max_acl=0.5, namespace=''),
										transitions={'continue': 'Open hand', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Low, 'failed': Autonomy.Low},
										remapping={'joints_data': 'PA_start_joint_pos', 'joint_values': 'joint_values'})

			# x:901 y:253
			OperatableStateMachine.add('Hold object',
										ActivateRaspiDigitalOuput(service_name="/obr_activate"),
										transitions={'continue': 'Rotate object', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Low, 'failed': Autonomy.Low},
										remapping={'value': 'True1', 'success': 'success'})

			# x:409 y:141
			OperatableStateMachine.add('Move to point1',
										CallJointTrap(max_vel=0.1, max_acl=0.1, namespace=''),
										transitions={'continue': 'Grab object', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Low, 'failed': Autonomy.Low},
										remapping={'joints_data': 'PA_pick_joint_pos', 'joint_values': 'joint_values'})

			# x:808 y:55
			OperatableStateMachine.add('Move to release location',
										CallJointTrap(max_vel=0.5, max_acl=0.5, namespace=''),
										transitions={'continue': 'Release hand for drop', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Low, 'failed': Autonomy.Low},
										remapping={'joints_data': 'PA_drop_joint_pos', 'joint_values': 'joint_values'})

			# x:1093 y:145
			OperatableStateMachine.add('Move to retreat location',
										CallJointTrap(max_vel=0.5, max_acl=0.5, namespace=''),
										transitions={'continue': 'Hold object', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Low, 'failed': Autonomy.Low},
										remapping={'joints_data': 'PA_start_joint_pos', 'joint_values': 'joint_values'})

			# x:240 y:51
			OperatableStateMachine.add('Open hand',
										MoveSoftHand(motion_duration=3, motion_timestep=0.1),
										transitions={'continue': 'Move to point1', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'goal_hand_pos': 'hand_release_positon', 'success': 'success'})

			# x:1098 y:45
			OperatableStateMachine.add('Release hand for drop',
										MoveSoftHand(motion_duration=3, motion_timestep=0.1),
										transitions={'continue': 'Move to retreat location', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Low, 'failed': Autonomy.Low},
										remapping={'goal_hand_pos': 'hand_release_positon', 'success': 'success'})

			# x:901 y:526
			OperatableStateMachine.add('Release object',
										ActivateRaspiDigitalOuput(service_name="/obr_activate"),
										transitions={'continue': 'finished', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Low, 'failed': Autonomy.Low},
										remapping={'value': 'False1', 'success': 'success'})

			# x:901 y:431
			OperatableStateMachine.add('Rotate back',
										ActivateRaspiDigitalOuput(service_name="/obr_rotate"),
										transitions={'continue': 'Release object', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Low, 'failed': Autonomy.Low},
										remapping={'value': 'False1', 'success': 'success'})

			# x:897 y:335
			OperatableStateMachine.add('Rotate object',
										ActivateRaspiDigitalOuput(service_name="/obr_rotate"),
										transitions={'continue': 'Rotate back', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Low, 'failed': Autonomy.Low},
										remapping={'value': 'True1', 'success': 'success'})

			# x:623 y:50
			OperatableStateMachine.add('Grab object',
										MoveSoftHand(motion_duration=5, motion_timestep=0.1),
										transitions={'continue': 'Move to release location', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Low, 'failed': Autonomy.Low},
										remapping={'goal_hand_pos': 'hand_grab_positon', 'success': 'success'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
