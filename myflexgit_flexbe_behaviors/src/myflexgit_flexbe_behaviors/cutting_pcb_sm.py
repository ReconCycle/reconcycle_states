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
class CuttingPCBSM(Behavior):
	'''
	Panda robot pickup the PCB, put it in the cutter, pickup the battery
	'''


	def __init__(self):
		super(CuttingPCBSM, self).__init__()
		self.name = 'Cutting PCB'

		# parameters of this behavior
		self.add_parameter('robot_name_space', ''panda_2'')
		self.add_parameter('max_vel', 0.2)
		self.add_parameter('max_acl', 0.2)
		self.add_parameter('cutting_time', 6)
		self.add_parameter('cutter_service', ''/cutter_activate')

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# O 34 154 
		# 1. move to safe position before pick up|n2. move to pcb and start vacuum|n3. move to safe position before cutter|n4. move pcb in clam and release vacuum|n5. move to safe position before cutter|n6. cutt|n7. pickup battery with vacumm|n8. move over the trash and drop battery



	def create(self):
		# x:108 y:609, x:267 y:395
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.TR = True
		_state_machine.userdata.panda1_init_position = 'panda_1_init'
		_state_machine.userdata.FA = False
		_state_machine.userdata.panda1_table_pick = 'panda_1_pick_up'
		_state_machine.userdata.panda1_clamp_pick = 'panda_1_from_clamp'
		_state_machine.userdata.panda1_clamp_release = 'panda_1_drop_down1'
		_state_machine.userdata.panda1_plastic_release = 'panda_1_throw_plastic'
		_state_machine.userdata.panda1_waiting_point = 'holding_point_panda_1'
		_state_machine.userdata.panda2_clamp_hold = 'panda_2_hold'
		_state_machine.userdata.panda2_clamp_break_trj = 'breaking_object_n1'
		_state_machine.userdata.panda2_clamp_retreat_trj = 'trj_umik_2'
		_state_machine.userdata.closed_hand_clamp = [0.84]
		_state_machine.userdata.closed_hand_table = [0.6]
		_state_machine.userdata.open_hand = [0.1]

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:842 y:39, x:130 y:365
		_sm_container_0 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['position_name'])

		with _sm_container_0:
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



		with _state_machine:
			# x:272 y:42
			OperatableStateMachine.add('Container',
										_sm_container_0,
										transitions={'finished': 'Activate cutter', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'position_name': 'panda1_table_pick'})

			# x:712 y:43
			OperatableStateMachine.add('Cutting timer',
										WaitState(wait_time=self.cutting_time),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Low})

			# x:497 y:48
			OperatableStateMachine.add('Activate cutter',
										ActivateRaspiDigitalOuput(service_name=self.cutter_service),
										transitions={'continue': 'Cutting timer', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Low, 'failed': Autonomy.Low},
										remapping={'value': 'TR', 'success': 'success'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
