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
# from keyframes import hello
import keyframes as kf
import numpy as np
# from time import sleep
# import threading
from bezier import keyframes_to_points, points_to_graph


class AngleInterpolationAgent(PIDAgent):
    def __init__(self, simspark_ip='localhost',
                 simspark_port=3100,
                 teamname='DAInamite',
                 player_id=0,
                 sync_mode=True):
        super(AngleInterpolationAgent, self).__init__(simspark_ip, simspark_port, teamname, player_id, sync_mode)
        self.keyframes = ([], [], [])
        self.animation_values = {}

    def think(self, perception):
        target_joints = self.angle_interpolation(self.keyframes, perception)
        if 'LHipYawPitch' in target_joints.keys():
            target_joints['RHipYawPitch'] = target_joints['LHipYawPitch'] # copy missing joint in keyframes
        self.target_joints.update(target_joints)
        return super(AngleInterpolationAgent, self).think(perception)

    def angle_interpolation(self, keyframes, perception):
        target_joints = {}
        # YOUR CODE HERE

        # empty keyframes variable to detect if animation restarted
        if keyframes != ([], [], []):  # new animation
            all_points = keyframes_to_points(keyframes, self.joint_controller.dt)
            self.animation_values = {}
            for joint_name, points in all_points.items():
                # (np x, np y) -> list y
                self.animation_values[joint_name] = points_to_graph(points, self.joint_controller.dt)[1].tolist()
            self.keyframes = ([], [], [])

        delete = False
        for joint_name, joint_values in self.animation_values.items():
            target_joints[joint_name] = joint_values.pop(0)
            if len(joint_values) == 1:
                delete = True
                break
        if delete:
            self.animation_values = {}
            
        return target_joints

# def keyframe_change():
#     print("start")
#     agent.keyframes = hello()  # CHANGE DIFFERENT KEYFRAMES
#     sleep(3)
#     print("restart")
#     agent.keyframes = hello()

if __name__ == '__main__':
    agent = AngleInterpolationAgent()
    # threading.Thread(target=keyframe_change, daemon=True).start()
    agent.keyframes = kf.hello()
    agent.run()
