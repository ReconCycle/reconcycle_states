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
from myflexgit_flexbe_behaviors.wait_test_behavior_sm import waittestbehaviorSM
from myflexgit_flexbe_states.avtivate_raspi_output import ActivateRaspiDigitalOuput
from myflexgit_flexbe_states.read_from_mongodb import ReadFromMongo
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Mar 31 2021
@author: Rok Pahic
'''
class DebugingwaitinparalerSM(Behavior):
	'''
	/
	'''


	def __init__(self):
		super(DebugingwaitinparalerSM, self).__init__()
		self.name = 'Debuging wait in paraler'

		# parameters of this behavior
		self.add_parameter('text1', 'testiranje')
		self.add_parameter('wait_time_tu', 3)

		# references to used behaviors
		self.add_behavior(waittestbehaviorSM, 'Container/wait test behavior')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:30 y:365, x:46 y:224
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.read_name = 'panda1_drop_down3'
		_state_machine.userdata.TR = True

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:30 y:365, x:655 y:227
		_sm_container_0 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['read_name', 'TR'])

		with _sm_container_0:
			# x:112 y:115
			OperatableStateMachine.add('wait_2_2',
										WaitState(wait_time=self.wait_time_tu),
										transitions={'done': 'report_2'},
										autonomy={'done': Autonomy.Off})

			# x:361 y:284
			OperatableStateMachine.add('reading_2',
										ReadFromMongo(),
										transitions={'continue': 'testni blok_2', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'entry_name': 'read_name', 'joints_data': 'joints_data'})

			# x:116 y:189
			OperatableStateMachine.add('report',
										LogState(text='testiranje Loop12', severity=Logger.REPORT_ERROR),
										transitions={'done': 'wait'},
										autonomy={'done': Autonomy.Off})

			# x:583 y:437
			OperatableStateMachine.add('report3',
										LogKeyState(text='reporting12', severity=Logger.REPORT_WARN),
										transitions={'done': 'wait_3'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'joints_data'})

			# x:295 y:60
			OperatableStateMachine.add('report_2',
										LogState(text='Enter loop12', severity=Logger.REPORT_ERROR),
										transitions={'done': 'testni blok'},
										autonomy={'done': Autonomy.Off})

			# x:76 y:525
			OperatableStateMachine.add('report_3',
										LogState(text='exit Loop12', severity=Logger.REPORT_ERROR),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:639 y:54
			OperatableStateMachine.add('testni blok',
										ActivateRaspiDigitalOuput(service_name='/obr_activate'),
										transitions={'continue': 'reading', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'value': 'TR', 'success': 'success'})

			# x:722 y:367
			OperatableStateMachine.add('testni blok_2',
										ActivateRaspiDigitalOuput(service_name='/obr_activate'),
										transitions={'continue': 'report3', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'value': 'TR', 'success': 'success'})

			# x:105 y:266
			OperatableStateMachine.add('wait',
										WaitState(wait_time=self.wait_time_tu),
										transitions={'done': 'reading_2'},
										autonomy={'done': Autonomy.Off})

			# x:309 y:468
			OperatableStateMachine.add('wait_3',
										WaitState(wait_time=self.wait_time_tu),
										transitions={'done': 'report_3'},
										autonomy={'done': Autonomy.Off})

			# x:366 y:158
			OperatableStateMachine.add('reading',
										ReadFromMongo(),
										transitions={'continue': 'report', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'entry_name': 'read_name', 'joints_data': 'joints_data'})


		# x:30 y:365, x:937 y:417, x:230 y:365, x:330 y:365, x:430 y:365
		_sm_container_1 = ConcurrencyContainer(outcomes=['finished', 'failed'], input_keys=['read_name', 'TR'], conditions=[
										('finished', [('wait test behavior', 'finished'), ('Container', 'finished')]),
										('failed', [('wait test behavior', 'failed')]),
										('failed', [('Container', 'failed')])
										])

		with _sm_container_1:
			# x:530 y:101
			OperatableStateMachine.add('Container',
										_sm_container_0,
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'read_name': 'read_name', 'TR': 'TR'})

			# x:62 y:192
			OperatableStateMachine.add('wait test behavior',
										self.use_behavior(waittestbehaviorSM, 'Container/wait test behavior'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})



		with _state_machine:
			# x:241 y:80
			OperatableStateMachine.add('report',
										LogState(text='test start', severity=Logger.REPORT_ERROR),
										transitions={'done': 'Container'},
										autonomy={'done': Autonomy.Off})

			# x:241 y:157
			OperatableStateMachine.add('report_2',
										LogState(text='test end', severity=Logger.REPORT_ERROR),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:56 y:115
			OperatableStateMachine.add('Container',
										_sm_container_1,
										transitions={'finished': 'report_2', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'read_name': 'read_name', 'TR': 'TR'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
