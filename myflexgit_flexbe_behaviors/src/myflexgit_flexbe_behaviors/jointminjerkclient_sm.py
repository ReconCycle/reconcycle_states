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
Created on Mon Jan 04 2021
@author: Matej
'''
class JointMinJerkClientSM(Behavior):
	'''
	Calling joint_min_jerk action server.
	'''


	def __init__(self):
		super(JointMinJerkClientSM, self).__init__()
		self.name = 'JointMinJerkClient'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		goal_joint_pos = [-0.04, -0.20, 0.20, -2.00, 0.018, 1.83, 1]
		motion_duration = 2
		motion_timestep = 0.1
		# x:30 y:365, x:130 y:365
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:122 y:89
			OperatableStateMachine.add('CallJointMinJerk',
										CallJointMinJerk(goal_joint_pos=goal_joint_pos, motion_duration=motion_duration, motion_timestep=motion_timestep),
										transitions={'continue': 'finished', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'minjerk_out': 'minjerk_out'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
