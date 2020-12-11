# reconcycle_states
FlexBe states for the ReconCycle project

# write_to_mongodb.py
Added write_to_mongodb. Input keys: JointState() data construction (entry_data), _id to write to (entry_name).
When tests are done change the following:

entry_data = JointState(position=[1,2,3,4,5,6,7], name=['a','b','c','d', 'e', 'f', 'g'])
to
entry_data = userdata.entry_data

# read_from_mongodb.py
Added read_from_mongodb. Input keys: _id to read from DB (entry_name). Output keys: JointState() data construction (joints_data).

# call_joint_trap_vel_action_server.py
Added call_joint_trap_vel_action_server. Input keys: JointState() data construction (joints_data). Output keys: JointState()
data construction (joint_values)

When tests with dummy interface are done change the following @ self._topic:
'panda_2/joint_trap_vel_action_server' to 'joint_trap_vel_action_server'



Current flow in FlexBe:
 --> Starting new behavior...
 Writting to mongoDB _id: matej!
 Reading _id: matej from mongoDB: [-]
     header: 
      seq: 0
      stamp: 
        secs: 0
        nsecs:         0
      frame_id: ''
    name: 
      - a
      - b
      - c
      - d
      - e
      - f
      - g
    position: [1, 2, 3, 4, 5, 6, 7]
    velocity: []
    effort: []
 Goal sent: header: [-]
      seq: 0
      stamp: 
        secs: 0
        nsecs:         0
      frame_id: ''
    name: 
      - a
      - b
      - c
      - d
      - e
      - f
      - g
    position: [1, 2, 3, 4, 5, 6, 7]
    velocity: []
    effort: []
 Action Server reply: [-]
     final_joints: 
      header: 
        seq: 0
        stamp: 
          secs: 0
          nsecs:         0
        frame_id: ''
      name: []
      position: []
      velocity: []
      effort: []
    fully_succeeded: True
 Exiting JointTrapVelAction state

