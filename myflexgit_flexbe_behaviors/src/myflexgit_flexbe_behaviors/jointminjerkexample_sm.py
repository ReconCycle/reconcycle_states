#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from myflexgit_flexbe_states.Call_joint_min_jerk_action_server import CallJointMinJerk
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Jan 20 2021
@author: Matej
'''
class JointMinJerkExampleSM(Behavior):
	'''
	And example of Call_joint_min_jerk_action_server.py client.
	'''


	def __init__(self):
		super(JointMinJerkExampleSM, self).__init__()
		self.name = 'JointMinJerkExample'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		motion_duration = 2
		motion_timestep = 0.01
		# x:30 y:365, x:130 y:365
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.goal_joint_pos = [-0.04, -0.20, 0.20, -2.00, 0.018, 1.83, 1]

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:69 y:107
			OperatableStateMachine.add('MoveJointMinJerkStateExample',
										CallJointMinJerk(motion_duration=motion_duration, motion_timestep=motion_timestep),
										transitions={'continue': 'finished', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'goal_joint_pos': 'goal_joint_pos', 'minjerk_out': 'minjerk_out'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
