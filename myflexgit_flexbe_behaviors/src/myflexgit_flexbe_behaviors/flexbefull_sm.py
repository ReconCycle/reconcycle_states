#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from myflexgit_flexbe_states.CallAction_TF_Cart import CallT1
from myflexgit_flexbe_states.CallAction_TF_CartLin import CallT2
from myflexgit_flexbe_states.Call_joint_min_jerk_action_server import CallJointMinJerk
from myflexgit_flexbe_states.Read_TF_Cart import ReadT1
from myflexgit_flexbe_states.Read_TF_CartLin import ReadT2
from myflexgit_flexbe_states.call_joint_trap_vel_action_server import CallJointTrap
from myflexgit_flexbe_states.read_from_mongodb import ReadFromMongo
from myflexgit_flexbe_states.write_to_mongodb import WriteToMongo
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu Dec 17 2020
@author: Matej
'''
class FlexBEFULLSM(Behavior):
	'''
	Full behavior with states.
	'''


	def __init__(self):
		super(FlexBEFULLSM, self).__init__()
		self.name = 'FlexBEFULL'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		target1 = "target1"
		target2 = "target2"
		world = "world"
		goal_joint_pos = [0, 1, 0, 1, 0, 1, 1]
		motion_duration = 2
		motion_timestep = 0.1
		# x:723 y:656, x:130 y:365
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.entry_data = []
		_state_machine.userdata.entry_name = 'matej'
		_state_machine.userdata.joints_data = []
		_state_machine.userdata.joint_values = []
		_state_machine.userdata.t1_data = []
		_state_machine.userdata.t1_out = []
		_state_machine.userdata.t2_data = []
		_state_machine.userdata.t2_out = []

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:79 y:63
			OperatableStateMachine.add('WriteToMongoDB',
										WriteToMongo(),
										transitions={'continue': 'ReadFromMongoDB', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'entry_data': 'entry_data', 'entry_name': 'entry_name'})

			# x:837 y:216
			OperatableStateMachine.add('CallCartServer',
										CallT1(),
										transitions={'continue': 'ReadTFCartLin', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'t1_data': 't1_data', 't1_out': 't1_out'})

			# x:842 y:599
			OperatableStateMachine.add('CallJointMinJerk',
										CallJointMinJerk(goal_joint_pos=goal_joint_pos, motion_duration=motion_duration, motion_timestep=motion_timestep),
										transitions={'continue': 'finished', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'minjerk_out': 'minjerk_out'})

			# x:586 y:59
			OperatableStateMachine.add('CallJointTrapServer',
										CallJointTrap(),
										transitions={'continue': 'ReadTFCart', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'joints_data': 'joints_data', 'joint_values': 'joint_values'})

			# x:325 y:60
			OperatableStateMachine.add('ReadFromMongoDB',
										ReadFromMongo(),
										transitions={'continue': 'CallJointTrapServer', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'entry_name': 'entry_name', 'joints_data': 'joints_data'})

			# x:836 y:59
			OperatableStateMachine.add('ReadTFCart',
										ReadT1(target_frame=target1, source_frame=world),
										transitions={'continue': 'CallCartServer', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'t1_data': 't1_data'})

			# x:838 y:359
			OperatableStateMachine.add('ReadTFCartLin',
										ReadT2(target_frame=target2, source_frame=world),
										transitions={'continue': 'CallCartLinServer', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'t2_data': 't2_data'})

			# x:838 y:482
			OperatableStateMachine.add('CallCartLinServer',
										CallT2(),
										transitions={'continue': 'CallJointMinJerk', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'t2_data': 't2_data', 't2_out': 't2_out'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
