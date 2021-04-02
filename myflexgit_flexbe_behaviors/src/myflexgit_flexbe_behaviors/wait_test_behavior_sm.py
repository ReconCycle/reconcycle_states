#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.log_key_state import LogKeyState
from flexbe_states.log_state import LogState
from flexbe_states.wait_state import WaitState
from myflexgit_flexbe_states.read_from_mongodb import ReadFromMongo
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Mar 31 2021
@author: Rok Pahic
'''
class waittestbehaviorSM(Behavior):
	'''
	/
	'''


	def __init__(self):
		super(waittestbehaviorSM, self).__init__()
		self.name = 'wait test behavior'

		# parameters of this behavior
		self.add_parameter('self.text1', 'testiranje')
		self.add_parameter('wait_time', 3)

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:30 y:365, x:716 y:179
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.read_name = 'panda1_drop_down3'

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:112 y:53
			OperatableStateMachine.add('wait_2',
										WaitState(wait_time=self.wait_time),
										transitions={'done': 'report_2'},
										autonomy={'done': Autonomy.Off})

			# x:361 y:284
			OperatableStateMachine.add('reading_2',
										ReadFromMongo(),
										transitions={'continue': 'report3', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'entry_name': 'read_name', 'joints_data': 'joints_data'})

			# x:116 y:189
			OperatableStateMachine.add('report',
										LogState(text='testiranje Loop1', severity=Logger.REPORT_ERROR),
										transitions={'done': 'wait'},
										autonomy={'done': Autonomy.Off})

			# x:583 y:437
			OperatableStateMachine.add('report3',
										LogKeyState(text='reporting', severity=Logger.REPORT_WARN),
										transitions={'done': 'wait_3'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'joints_data'})

			# x:295 y:60
			OperatableStateMachine.add('report_2',
										LogState(text='Enter loop1', severity=Logger.REPORT_ERROR),
										transitions={'done': 'reading'},
										autonomy={'done': Autonomy.Off})

			# x:76 y:525
			OperatableStateMachine.add('report_3',
										LogState(text='exit Loop1', severity=Logger.REPORT_ERROR),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:105 y:266
			OperatableStateMachine.add('wait',
										WaitState(wait_time=self.wait_time),
										transitions={'done': 'reading_2'},
										autonomy={'done': Autonomy.Off})

			# x:309 y:468
			OperatableStateMachine.add('wait_3',
										WaitState(wait_time=self.wait_time),
										transitions={'done': 'report_3'},
										autonomy={'done': Autonomy.Off})

			# x:366 y:158
			OperatableStateMachine.add('reading',
										ReadFromMongo(),
										transitions={'continue': 'report', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'entry_name': 'read_name', 'joints_data': 'joints_data'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
