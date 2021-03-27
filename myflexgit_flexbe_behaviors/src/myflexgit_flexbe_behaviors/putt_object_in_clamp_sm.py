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
from myflexgit_flexbe_behaviors.test_dmp_execution_sm import TestDMPexecutionSM
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
class PuttobjectinclampSM(Behavior):
	'''
	Pick up heat alocator from table and put in clamp
	'''


	def __init__(self):
		super(PuttobjectinclampSM, self).__init__()
		self.name = 'Putt object in clamp'

		# parameters of this behavior
		self.add_parameter('clamp_service_name', ''obr_activate'')
		self.add_parameter('max_acl', 0.3)
		self.add_parameter('namespace', ''panda_1'')
		self.add_parameter('max_vel', 0.3)

		# references to used behaviors
		self.add_behavior(TestDMPexecutionSM, 'Cell runing/TestDMPexecution')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1121 y:485, x:723 y:338
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['object_table_location_name', 'clamp_release_location_name', 'clamp_waiting_location_name', 'closed_hand_table'])
		_state_machine.userdata.TR = True
		_state_machine.userdata.panda1_init_position = 'panda_1_init'
		_state_machine.userdata.open_hand = [0.1]
		_state_machine.userdata.closed_hand_table = [0.6]
		_state_machine.userdata.closed_hand_clamp = [0.84]
		_state_machine.userdata.FA = False
		_state_machine.userdata.object_table_location_name = 'panda_1_pick_up'
		_state_machine.userdata.panda1_clamp_pick = 'panda_1_from_clamp'
		_state_machine.userdata.clamp_release_location_name = 'panda_1_drop_down1'
		_state_machine.userdata.panda1_plastic_release = 'panda_1_throw_plastic'
		_state_machine.userdata.clamp_waiting_location_name = 'holding_point_panda_1'
		_state_machine.userdata.panda2_clamp_hold = 'panda_2_hold'
		_state_machine.userdata.panda2_clamp_break_trj = 'breaking_object_n1'
		_state_machine.userdata.panda2_clamp_retreat_trj = 'trj_umik_2'

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:30 y:365, x:130 y:365
		_sm_put_object_in_clamp_0 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['position_name'])

		with _sm_put_object_in_clamp_0:
			# x:182 y:50
			OperatableStateMachine.add('Read robot position',
										ReadFromMongo(),
										transitions={'continue': 'Move to robot position', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'entry_name': 'position_name', 'joints_data': 'joints_positions'})

			# x:500 y:117
			OperatableStateMachine.add('Move to robot position',
										CallJointTrap(max_vel=self.max_vel, max_acl=self.max_acl, namespace=self.namespace),
										transitions={'continue': 'finished', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Low, 'failed': Autonomy.Low},
										remapping={'joints_data': 'joints_positions', 'joint_values': 'joint_values'})


		# x:30 y:365, x:130 y:365
		_sm_pick_object_1 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['position_name'])

		with _sm_pick_object_1:
			# x:182 y:50
			OperatableStateMachine.add('Read robot position',
										ReadFromMongo(),
										transitions={'continue': 'Move to robot position', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'entry_name': 'position_name', 'joints_data': 'joints_positions'})

			# x:500 y:117
			OperatableStateMachine.add('Move to robot position',
										CallJointTrap(max_vel=self.max_vel, max_acl=self.max_acl, namespace=self.namespace),
										transitions={'continue': 'finished', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Low, 'failed': Autonomy.Low},
										remapping={'joints_data': 'joints_positions', 'joint_values': 'joint_values'})


		# x:30 y:365, x:130 y:365
		_sm_move_to_safe_spot_2 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['position_name'])

		with _sm_move_to_safe_spot_2:
			# x:182 y:50
			OperatableStateMachine.add('Read robot position',
										ReadFromMongo(),
										transitions={'continue': 'Move to robot position', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'entry_name': 'position_name', 'joints_data': 'joints_positions'})

			# x:500 y:117
			OperatableStateMachine.add('Move to robot position',
										CallJointTrap(max_vel=self.max_vel, max_acl=self.max_acl, namespace=self.namespace),
										transitions={'continue': 'finished', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Low, 'failed': Autonomy.Low},
										remapping={'joints_data': 'joints_positions', 'joint_values': 'joint_values'})


		# x:49 y:588, x:571 y:251
		_sm_cell_runing_3 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['TR', 'panda1_init_position', 'open_hand', 'FA', 'closed_hand_table', 'closed_hand_clamp', 'pos_table', 'clamp_release', 'clamp_pick', 'drop_plastic', 'panda1_holding_pos', 'panda2_clamp_hold', 'panda2_clamp_break_trj', 'panda2_clamp_retreat_trj'])

		with _sm_cell_runing_3:
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
										autonomy={'continue': Autonomy.Low, 'failed': Autonomy.Off},
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
										transitions={'continue': 'TestDMPexecution', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Low, 'failed': Autonomy.Low},
										remapping={'joints_data': 'panda1_holding_values', 'joint_values': 'joint_values'})

			# x:287 y:29
			OperatableStateMachine.add('Move to pick position',
										CallJointTrap(max_vel=0.3, max_acl=0.3, namespace='panda_1'),
										transitions={'continue': 'Grab object', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Low, 'failed': Autonomy.Low},
										remapping={'joints_data': 'joints_for_table', 'joint_values': 'joint_values'})

			# x:250 y:578
			OperatableStateMachine.add('Open clamp',
										ActivateRaspiDigitalOuput(service_name='/obr_activate'),
										transitions={'continue': 'finished', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'value': 'FA', 'success': 'success'})

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

			# x:1083 y:473
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

			# x:928 y:565
			OperatableStateMachine.add('Rotate CLAMP down',
										ActivateRaspiDigitalOuput(service_name='/obr_rotate'),
										transitions={'continue': 'Wait to PCB fall', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Low, 'failed': Autonomy.Low},
										remapping={'value': 'TR', 'success': 'success'})

			# x:477 y:566
			OperatableStateMachine.add('Rotate CLAMP up',
										ActivateRaspiDigitalOuput(service_name='obr_rotate'),
										transitions={'continue': 'Open clamp', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'value': 'FA', 'success': 'success'})

			# x:1091 y:370
			OperatableStateMachine.add('TestDMPexecution',
										self.use_behavior(TestDMPexecutionSM, 'Cell runing/TestDMPexecution'),
										transitions={'finished': 'Rotate CLAMP down', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:675 y:580
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



		with _state_machine:
			# x:114 y:44
			OperatableStateMachine.add('Release object_2',
										MoveSoftHand(motion_duration=3, motion_timestep=0.1),
										transitions={'continue': 'Pick object', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Low, 'failed': Autonomy.Low},
										remapping={'goal_hand_pos': 'open_hand', 'success': 'success'})

			# x:1162 y:40
			OperatableStateMachine.add('Close clamp',
										ActivateRaspiDigitalOuput(service_name=self.clamp_service_name),
										transitions={'continue': 'Move to safe spot', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Low, 'failed': Autonomy.Low},
										remapping={'value': 'TR', 'success': 'success'})

			# x:580 y:23
			OperatableStateMachine.add('Grab object',
										MoveSoftHand(motion_duration=3, motion_timestep=0.1),
										transitions={'continue': 'Put object in clamp', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Low, 'failed': Autonomy.Low},
										remapping={'goal_hand_pos': 'closed_hand_table', 'success': 'success'})

			# x:1145 y:202
			OperatableStateMachine.add('Move to safe spot',
										_sm_move_to_safe_spot_2,
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'position_name': 'clamp_waiting_location_name'})

			# x:340 y:28
			OperatableStateMachine.add('Pick object',
										_sm_pick_object_1,
										transitions={'finished': 'Grab object', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'position_name': 'object_table_location_name'})

			# x:748 y:21
			OperatableStateMachine.add('Put object in clamp',
										_sm_put_object_in_clamp_0,
										transitions={'finished': 'Release object', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'position_name': 'clamp_release_location_name'})

			# x:931 y:28
			OperatableStateMachine.add('Release object',
										MoveSoftHand(motion_duration=3, motion_timestep=0.1),
										transitions={'continue': 'Close clamp', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Low, 'failed': Autonomy.Low},
										remapping={'goal_hand_pos': 'open_hand', 'success': 'success'})

			# x:108 y:289
			OperatableStateMachine.add('Cell runing',
										_sm_cell_runing_3,
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'TR': 'TR', 'panda1_init_position': 'panda1_init_position', 'open_hand': 'open_hand', 'FA': 'FA', 'closed_hand_table': 'closed_hand_table', 'closed_hand_clamp': 'closed_hand_clamp', 'pos_table': 'panda1_table_pick', 'clamp_release': 'panda1_clamp_release', 'clamp_pick': 'panda1_clamp_pick', 'drop_plastic': 'panda1_plastic_release', 'panda1_holding_pos': 'panda1_waiting_point', 'panda2_clamp_hold': 'panda2_clamp_hold', 'panda2_clamp_break_trj': 'panda2_clamp_break_trj', 'panda2_clamp_retreat_trj': 'panda2_clamp_retreat_trj'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
