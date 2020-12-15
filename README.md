# Reconcycle states

FlexBe states for the ReconCycle project

## Table of contents

* [Python files]()


### Python files  
#### write_to_mongodb.py
- Added write_to_mongodb. Input keys: JointState() data construction (entry_data), _id to write to (entry_name).
- When tests are done change the following:

- entry_data = JointState(position=[1,2,3,4,5,6,7], name=['a','b','c','d', 'e', 'f', 'g']) to
  entry_data = userdata.entry_data

#### read_from_mongodb.py
- Added read_from_mongodb. Input keys: _id to read from DB (entry_name). Output keys: JointState() data construction (joints_data).

#### call_joint_trap_vel_action_server.py
- Added call_joint_trap_vel_action_server. Input keys: JointState() data construction (joints_data). Output keys: JointState()
data construction (joint_values)

- When tests with dummy interface are done change the following @ self._topic:
'panda_2/joint_trap_vel_action_server' to 'joint_trap_vel_action_server'

#### Read_TF_Cart.py
- Added target1: lookupTransform():  input_keys =['target1'], output_keys = ['t1_data']

#### CallAction_TF_Cart.py
- Added cart_trap_vel_action_server: input_keys = ['t1_data'], output_keys = ['t1_out']


#### Read_TF_CartLin.py
- Added target2: lookupTransform(): input_keys =['target2'], output_keys = ['t2_data']

#### CallAction_TF_CartLin.py
- Added cart_lin_task_action_server: input_keys = ['t2_data'], output_keys = ['t2_out']