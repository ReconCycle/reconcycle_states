# Reconcycle states

This repository includes python FlexBe states for the ReconCycle project

# Table of contents

- [ReconCycle states](#reconcycle-states)
- [Table of contents](#table-of-contents)
- [Introduction](#introduction)
- [Python files](#python-files)
	- [ROS 1](#ros-1)
- [Behaviors](#behaviors)
- [Examples](#examples)


# Introduction
[FlexBE](http://wiki.ros.org/flexbe/) helps us to create complex robot behaviors without the need for manually coding them.
States define what should be done by a behavior. They are grouped as statemachines, defining the control flow when the behavior is executed. 
Therefore, each state declares a set of outcomes which represent possible results of execution

This repository includes FlexBe states [python files](#python-files)


# Python files
Python files represent FlexBe states which are joined together into one behavior.

## ROS 1  
- [write_to_mongodb](/myflexgit_flexbe_states/src/myflexgit_flexbe_states/write_to_mongodb.py)
	- input keys: JointState() data construction (entry_data).
	- _id to write to in mongodb (entry_name).
 
- [read_from_mongodb](/myflexgit_flexbe_states/src/myflexgit_flexbe_states/read_from_mongodb.py)
	- input keys: _id to read from in mongodb (entry_name).
	- output keys: JointState() data construction (joints_data).

- [call_joint_trap_vel_action_server](/myflexgit_flexbe_states/src/myflexgit_flexbe_states/call_joint_trap_vel_action_server.py)
	- Input keys: JointState() data construction (joints_data).
	- Output keys: JointState() data construction (joint_values)

- [Read_TF_Cart](/myflexgit_flexbe_states/src/myflexgit_flexbe_states/Read_TF_Cart.py)
	- Added target1: lookupTransform()
	- output_keys = ['t1_data']
	- input parameters: 
		- target_frame -> string
    	- source_frame -> string

- [CallAction_TF_Cart](/myflexgit_flexbe_states/src/myflexgit_flexbe_states/CallAction_TF_Cart.py)
	- Added call to cart_trap_vel_action_server
	- input_keys = ['t1_data']
	- output_keys = ['t1_out']

- [Read_TF_CartLin](/myflexgit_flexbe_states/src/myflexgit_flexbe_states/Read_TF_CartLin.py)
	- Added target2: lookupTransform()
	- output_keys = ['t2_data']
	- input parameters:
		- target_frame -> string
    	- source_frame -> string

- [CallAction_TF_CartLin](/myflexgit_flexbe_states/src/myflexgit_flexbe_states/CallAction_TF_CartLin.py)
	- Added call to cart_lin_task_action_server
	- input_keys = ['t2_data']
	- output_keys = ['t2_out']

- [Call_joint_min_jerk_action_server](/myflexgit_flexbe_states/src/myflexgit_flexbe_states/Call_joint_min_jerk_action_server.py)
	- Added call to joint_min_jerk_action_server
	- output_keys = ['minjerk_out']
	- input parameters:
		- goal_joint_pos -> list data of 7 joints. Example: [0, 1, 0, 1, 0, 0, 1]
		- motion_duration -> float 
		- motion_timestep -> float
	

# Behaviors
Behaviors are modeled as hierarchical state machines where states correspond to active actions and transitions describe the reaction to outcomes.

A [behavior file](/myflexgit_flexbe_behaviors/src/myflexgit_flexbe_behaviors/flexbefull_sm.py) is constructed from [python files](#python-files). The file is run by FlexBe behavior engine.

More information about FlexBe behavior engine is avaliable [here](https://github.com/team-vigir/flexbe_behavior_engine/blob/master/README.md).


# Examples
In order for examples to work, a pre-build panda_dockers has to be build and run:  
https://github.com/abr-ijs/panda_dockers

Example commands for a joint_min_jerk_action_client:
	- inside folder ros1_flexbe:
		- docker build --no-cache -t reconcycle/states:states .
		- docker run -it --name rcstate --network panda-simulator-gzweb_ros -e ROS_MASTER_URI=http://rosmaster:11311 reconcycle/states:states roslaunch myflexgit_flexbe_behaviors JointMinJerk.launch
		
An example of states inside behavior model. ![here](https://github.com/ReconCycle/reconcycle_states/blob/main/myflexgit_flexbe_states/src/myflexgit_flexbe_states/FlexBe%20Statemachine.png).