#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.wait_state import WaitState
from myflexgit_flexbe_states.MoveSoftHand import MoveSoftHand
from myflexgit_flexbe_states.avtivate_raspi_output import ActivateRaspiDigitalOuput
from myflexgit_flexbe_states.call_joint_trap_vel_action_server import CallJointTrap
from myflexgit_flexbe_states.read_from_mongodb import ReadFromMongo
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Fri Mar 26 2021
@author: Rok Pahic
'''
class D5_2SM(Behavior):
	'''
	Video for D5_2, paraller atempt
	'''


	def __init__(self):
		super(D5_2SM, self).__init__()
		self.name = 'D5_2'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:741 y:94, x:723 y:338
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.TR = True
		_state_machine.userdata.panda1_init_position = 'panda_1_init'
		_state_machine.userdata.open_hand = [0.1]
		_state_machine.userdata.closed_hand_table = [0.6]
		_state_machine.userdata.closed_hand_clamp = [0.84]
		_state_machine.userdata.FA = False
		_state_machine.userdata.panda1_table_pick = 'panda_1_pick_up'
		_state_machine.userdata.panda1_clamp_pick = 'panda_1_from_clamp'
		_state_machine.userdata.panda1_clamp_release = 'panda_1_drop_down'
		_state_machine.userdata.panda1_plastic_release = 'panda_1_throw_plastic'
		_state_machine.userdata.panda1_waiting_point = 'panda_1_from_clamp'
		_state_machine.userdata.panda2_clamp_hold = 'panda_2_hold'
		_state_machine.userdata.panda2_clamp_break_trj = 'breaking_object_n1'
		_state_machine.userdata.panda2_clamp_retreat_trj = 'trj_umik_2'

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:30 y:365, x:797 y:145
		_sm_cell_shotdown_0 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['TR', 'FA'])

		with _sm_cell_shotdown_0:
			# x:212 y:121
			OperatableStateMachine.add('Deactivate CLAMP air block',
										ActivateRaspiDigitalOuput(service_name='obr_block2_ON'),
										transitions={'continue': 'finished', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Low, 'failed': Autonomy.Low},
										remapping={'value': 'TR', 'success': 'success'})


		# x:49 y:588, x:571 y:251
		_sm_cell_runing_1 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['TR', 'panda1_init_position', 'open_hand', 'FA', 'closed_hand_table', 'closed_hand_clamp', 'pos_table', 'clamp_release', 'clamp_pick', 'drop_plastic', 'panda1_holding_pos', 'panda2_clamp_hold', 'panda2_clamp_break_trj', 'panda2_clamp_retreat_trj'])

		with _sm_cell_runing_1:
			# x:102 y:36
			OperatableStateMachine.add('Read table pick position',
										ReadFromMongo(),
										transitions={'continue': 'Move to pick position', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'entry_name': 'pos_table', 'joints_data': 'joints_for_table'})

			# x:528 y:41
			OperatableStateMachine.add('Grab object',
										MoveSoftHand(motion_duration=3, motion_timestep=0.1),
										transitions={'continue': 'Read clamp drop', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Low, 'failed': Autonomy.Low},
										remapping={'goal_hand_pos': 'closed_hand_table', 'success': 'success'})

			# x:863 y:16
			OperatableStateMachine.add('Move to drop',
										CallJointTrap(max_vel=0.2, max_acl=0.2, namespace='panda_1'),
										transitions={'continue': 'Release object', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'joints_data': 'joints_data_release', 'joint_values': 'joint_values'})

			# x:847 y:369
			OperatableStateMachine.add('Move to hold point',
										CallJointTrap(max_vel=0.2, max_acl=0.2, namespace='panda_2'),
										transitions={'continue': 'failed', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Low, 'failed': Autonomy.Low},
										remapping={'joints_data': 'before_clamp', 'joint_values': 'joint_values'})

			# x:1126 y:236
			OperatableStateMachine.add('Move to hold position',
										CallJointTrap(max_vel=0.5, max_acl=0.5, namespace='panda_1'),
										transitions={'continue': 'Rotate CLAMP down', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Low, 'failed': Autonomy.Low},
										remapping={'joints_data': 'panda1_holding_values', 'joint_values': 'joint_values'})

			# x:287 y:29
			OperatableStateMachine.add('Move to pick position',
										CallJointTrap(max_vel=0.3, max_acl=0.3, namespace='panda_1'),
										transitions={'continue': 'Grab object', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Low, 'failed': Autonomy.Low},
										remapping={'joints_data': 'joints_for_table', 'joint_values': 'joint_values'})

			# x:726 y:40
			OperatableStateMachine.add('Read clamp drop',
										ReadFromMongo(),
										transitions={'continue': 'Move to drop', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'entry_name': 'clamp_release', 'joints_data': 'joints_data_release'})

			# x:1133 y:123
			OperatableStateMachine.add('Read hold position',
										ReadFromMongo(),
										transitions={'continue': 'Move to hold position', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'entry_name': 'panda1_holding_pos', 'joints_data': 'panda1_holding_values'})

			# x:994 y:498
			OperatableStateMachine.add('Read panda 2 working point',
										ReadFromMongo(),
										transitions={'continue': 'Move to hold point', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'entry_name': 'panda2_clamp_hold', 'joints_data': 'before_clamp'})

			# x:1001 y:65
			OperatableStateMachine.add('Release object',
										MoveSoftHand(motion_duration=3, motion_timestep=0.1),
										transitions={'continue': 'Close clamp', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Low, 'failed': Autonomy.Low},
										remapping={'goal_hand_pos': 'open_hand', 'success': 'success'})

			# x:644 y:571
			OperatableStateMachine.add('Rotate CLAMP down',
										ActivateRaspiDigitalOuput(service_name='/obr_rotate'),
										transitions={'continue': 'Wait to PCB fall', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Low, 'failed': Autonomy.Low},
										remapping={'value': 'TR', 'success': 'success'})

			# x:318 y:569
			OperatableStateMachine.add('Rotate CLAMP up',
										ActivateRaspiDigitalOuput(service_name='obr_rotate'),
										transitions={'continue': 'finished', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'value': 'FA', 'success': 'success'})

			# x:508 y:574
			OperatableStateMachine.add('Wait to PCB fall',
										WaitState(wait_time=3.0),
										transitions={'done': 'Rotate CLAMP up'},
										autonomy={'done': Autonomy.Low})

			# x:1162 y:40
			OperatableStateMachine.add('Close clamp',
										ActivateRaspiDigitalOuput(service_name='/obr_activate'),
										transitions={'continue': 'Read hold position', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Low, 'failed': Autonomy.Low},
										remapping={'value': 'TR', 'success': 'success'})


		# x:1175 y:68, x:27 y:668
		_sm_cell_init_2 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['TR', 'panda1_init_position', 'open_hand', 'FA'])

		with _sm_cell_init_2:
			# x:40 y:46
			OperatableStateMachine.add('Activate CLAMP air block ',
										ActivateRaspiDigitalOuput(service_name='/obr_block2_ON'),
										transitions={'continue': 'Read initial state', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'value': 'TR', 'success': 'success'})

			# x:594 y:56
			OperatableStateMachine.add('Move Panda 1 to initial',
										CallJointTrap(max_vel=0.3, max_acl=0.3, namespace='/panda_1'),
										transitions={'continue': 'Open hand', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Low, 'failed': Autonomy.Off},
										remapping={'joints_data': 'init_position', 'joint_values': 'joint_values'})

			# x:867 y:47
			OperatableStateMachine.add('Open hand',
										MoveSoftHand(motion_duration=2, motion_timestep=0.1),
										transitions={'continue': 'finished', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'goal_hand_pos': 'open_hand', 'success': 'success'})

			# x:377 y:55
			OperatableStateMachine.add('Read initial state',
										ReadFromMongo(),
										transitions={'continue': 'Move Panda 1 to initial', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'entry_name': 'panda1_init_position', 'joints_data': 'init_position'})



		with _state_machine:
			# x:112 y:39
			OperatableStateMachine.add('Cell init',
										_sm_cell_init_2,
										transitions={'finished': 'Cell runing', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'TR': 'TR', 'panda1_init_position': 'panda1_init_position', 'open_hand': 'open_hand', 'FA': 'FA'})

			# x:108 y:289
			OperatableStateMachine.add('Cell runing',
										_sm_cell_runing_1,
										transitions={'finished': 'Cell shotdown', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'TR': 'TR', 'panda1_init_position': 'panda1_init_position', 'open_hand': 'open_hand', 'FA': 'FA', 'closed_hand_table': 'closed_hand_table', 'closed_hand_clamp': 'closed_hand_clamp', 'pos_table': 'panda1_table_pick', 'clamp_release': 'panda1_clamp_release', 'clamp_pick': 'panda1_clamp_pick', 'drop_plastic': 'panda1_plastic_release', 'panda1_holding_pos': 'panda1_waiting_point', 'panda2_clamp_hold': 'panda2_clamp_hold', 'panda2_clamp_break_trj': 'panda2_clamp_break_trj', 'panda2_clamp_retreat_trj': 'panda2_clamp_retreat_trj'})

			# x:77 y:542
			OperatableStateMachine.add('Cell shotdown',
										_sm_cell_shotdown_0,
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'TR': 'TR', 'FA': 'FA'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
