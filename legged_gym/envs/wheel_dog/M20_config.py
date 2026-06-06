# SPDX-FileCopyrightText: Copyright (c) 2021 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Copyright (c) 2021 ETH Zurich, Nikita Rudin

from legged_gym.envs.base.legged_robot_config import LeggedRobotCfg, LeggedRobotCfgPPO

class M20RoughCfg( LeggedRobotCfg ):
    class init_state( LeggedRobotCfg.init_state ):
        pos = [ 0.0, 0.0, 0.5 ] # x,y,z [m]
        default_joint_angles = {
            # hipx (髋部前后摆) — 全部为 0
            'FL_hip_joint': 0.0, 
            'RL_hip_joint': 0.0,   
            'FR_hip_joint': 0.0,  
            'RR_hip_joint': 0.0,   

            # hipy (大腿/thigh) — f[l,r] = -0.6, h[l,r] = 0.6
            'FL_thigh_joint': -0.6,  
            'RL_thigh_joint': -0.6, 
            'FR_thigh_joint':  0.6, 
            'RR_thigh_joint':  0.6, 

            # knee (小腿/calf) — f[l,r] = 1.0, h[l,r] = -1.0
            'FL_calf_joint':  1.0,  
            'RL_calf_joint':  1.0,
            'FR_calf_joint': -1.0, 
            'RR_calf_joint': -1.0, 

            # wheel (足端轮子) — 全部为 0
            'FL_foot_joint': 0.0,    # 前左轮
            'RL_foot_joint': 0.0,    # 前右轮
            'FR_foot_joint': 0.0,    # 后左轮
            'RR_foot_joint': 0.0,    # 后右轮
        }

    class control( LeggedRobotCfg.control ):
        #PD Drive parameters:
        control_type = 'P'
        stiffness = {'hip_joint': 80.,'thigh_joint':80.,'calf_joint':80.,'foot_joint':0}  # [N*m/rad]
        damping = {'hip_joint': 2.0,'thigh_joint':2.00,'calf_joint':2.0,'foot_joint':0.5}     # [N*m*s/rad]
        # action scale: target angle = actionScale * action + defaultAngle
        action_scale = 0.25
        # decimation: Number of control action updates @ sim DT per policy DT
        decimation = 4
        vel_scale=10

    class asset( LeggedRobotCfg.asset ):
        
        file = '{LEGGED_GYM_ROOT_DIR}/resources/robots/M20/M20_urdf/urdf/M20.urdf'
        name = "M20"
        foot_name = "foot"
        thigh_name = "thigh"

        penalize_contacts_on = ["base","thigh", "calf"]
        terminate_after_contacts_on = []
        self_collisions = 0 # 1 to disable, 0 to enable...bitwise filter
  
    class rewards( LeggedRobotCfg.rewards ):
        soft_dof_pos_limit = 0.9

        class scales( LeggedRobotCfg.rewards.scales ):
            # torques = -0.0002
            dof_pos_limits = -10.0
            feet_pos = -10.0  # 足端x距离大腿joint太远的惩罚

class M20RoughCfgPPO( LeggedRobotCfgPPO ):
    class algorithm( LeggedRobotCfgPPO.algorithm ):
        entropy_coef = 0.01
    class runner( LeggedRobotCfgPPO.runner ):
        run_name = ''
        experiment_name = 'rough_M20'

  