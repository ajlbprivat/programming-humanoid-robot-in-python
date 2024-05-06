'''In this exercise you need to implement an angle interploation function which makes NAO executes keyframe motion

* Tasks:
    1. complete the code in `AngleInterpolationAgent.angle_interpolation`,
       you are free to use splines interploation or Bezier interploation,
       but the keyframes provided are for Bezier curves, you can simply ignore some data for splines interploation,
       please refer data format below for details.
    2. try different keyframes from `keyframes` folder

* Keyframe data format:
    keyframe := (names, times, keys)
    names := [str, ...]  # list of joint names
    times := [[float, float, ...], [float, float, ...], ...]
    # times is a matrix of floats: Each line corresponding to a joint, and column element to a key.
    keys := [[float, [int, float, float], [int, float, float]], ...]
    # keys is a list of angles in radians or an array of arrays each containing [float angle, Handle1, Handle2],
    # where Handle is [int InterpolationType, float dTime, float dAngle] describing the handle offsets relative
    # to the angle and time of the point. The first Bezier param describes the handle that controls the curve
    # preceding the point, the second describes the curve following the point.
'''


from pid import PIDAgent
from keyframes import hello
import numpy as np


class AngleInterpolationAgent(PIDAgent):
    def __init__(self, simspark_ip='localhost',
                 simspark_port=3100,
                 teamname='DAInamite',
                 player_id=0,
                 sync_mode=True):
        super(AngleInterpolationAgent, self).__init__(simspark_ip, simspark_port, teamname, player_id, sync_mode)
        self.keyframes = ([], [], [])

    def think(self, perception):
        target_joints = self.angle_interpolation(self.keyframes, perception)
        if 'LHipYawPitch' in target_joints.keys():
            target_joints['RHipYawPitch'] = target_joints['LHipYawPitch'] # copy missing joint in keyframes
        self.target_joints.update(target_joints)
        return super(AngleInterpolationAgent, self).think(perception)

    def angle_interpolation(self, keyframes, perception):
        target_joints = {}
        # YOUR CODE HERE
        
        # Iterate over each joint
        for joint_idx, joint_name in enumerate(keyframes[0]):
            # Extract keyframes for the current joint
            joint_keyframes = keyframes[2][joint_idx]

            # Initialize lists to store times and angles
            times = []
            angles = []

            # Iterate over keyframes
            for keyframe in joint_keyframes:
                # Extract angle and handles
                angle = keyframe[0]
                handles = keyframe[1:]

                # Append time and angle to lists
                times.append(keyframe[1][1])  # Assuming time is the second element in handles
                angles.append(angle)

            # Interpolate angles using Bezier interpolation
            interpolated_angles = self.bezier_interpolation(times, angles, perception.time)

            # Populate target joints dictionary
            target_joints[joint_name] = interpolated_angles

        return target_joints

    def bezier_interpolation(self, times, angles, time):
        # Perform Bezier interpolation
        # For simplicity, let's assume linear interpolation between keyframes
        # You can replace this with actual Bezier interpolation implementation
        
        # Convert lists to numpy arrays for easier manipulation
        times = np.array(times)
        angles = np.array(angles)
        
        # Perform linear interpolation
        interpolated_angles = np.interp(time, times, angles)
        
        return interpolated_angles

if __name__ == '__main__':
    agent = AngleInterpolationAgent()
    agent.keyframes = hello()  # CHANGE DIFFERENT KEYFRAMES
    agent.run()
