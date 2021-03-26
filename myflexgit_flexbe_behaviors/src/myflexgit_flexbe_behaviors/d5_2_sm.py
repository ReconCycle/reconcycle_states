#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
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

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:30 y:365, x:797 y:145
		_sm_cell_shotdown_0 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['TR'])

		with _sm_cell_shotdown_0:
			# x:212 y:121
			OperatableStateMachine.add('Deactivate CLAMP air block',
										ActivateRaspiDigitalOuput(service_name='obr_block2_ON'),
										transitions={'continue': 'finished', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Low, 'failed': Autonomy.Low},
										remapping={'value': 'TR', 'success': 'success'})


		# x:904 y:39, x:73 y:654
		_sm_cell_runing_1 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['TR', 'panda1_init_position'])

		with _sm_cell_runing_1:
			# x:97 y:96
			OperatableStateMachine.add('Rotate CLAMP down',
										ActivateRaspiDigitalOuput(service_name='/obr_activate'),
										transitions={'continue': 'finished', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Low, 'failed': Autonomy.Low},
										remapping={'value': 'TR', 'success': 'success'})


		# x:890 y:31, x:167 y:451
		_sm_cell_init_2 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['TR', 'panda1_init_position'])

		with _sm_cell_init_2:
			# x:22 y:82
			OperatableStateMachine.add('Activate CLAMP air block ',
										ActivateRaspiDigitalOuput(service_name='/obr_block2_ON'),
										transitions={'continue': 'Read initial state', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Low, 'failed': Autonomy.Low},
										remapping={'value': 'TR', 'success': 'success'})

			# x:464 y:141
			OperatableStateMachine.add('Move Panda 1 to initial',
										CallJointTrap(max_vel=0.3, max_acl=0.3, namespace='/panda_1'),
										transitions={'continue': 'finished', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'joints_data': 'init_position', 'joint_values': 'joint_values'})

			# x:256 y:70
			OperatableStateMachine.add('Read initial state',
										ReadFromMongo(),
										transitions={'continue': 'Move Panda 1 to initial', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Low, 'failed': Autonomy.Off},
										remapping={'entry_name': 'panda1_init_position', 'joints_data': 'init_position'})



		with _state_machine:
			# x:76 y:60
			OperatableStateMachine.add('Cell init',
										_sm_cell_init_2,
										transitions={'finished': 'Cell runing', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'TR': 'TR', 'panda1_init_position': 'panda1_init_position'})

			# x:268 y:50
			OperatableStateMachine.add('Cell runing',
										_sm_cell_runing_1,
										transitions={'finished': 'Cell shotdown', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'TR': 'TR', 'panda1_init_position': 'panda1_init_position'})

			# x:477 y:58
			OperatableStateMachine.add('Cell shotdown',
										_sm_cell_shotdown_0,
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'TR': 'TR'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
