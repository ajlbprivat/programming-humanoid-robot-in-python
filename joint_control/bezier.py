import numpy as np

def points_to_graph(points, interval):
    # range of full graph
    t_full = np.arange(0, points[-2][0] + interval, interval)
    t_final = np.array([])
    y_final = np.array([])
    
    for i in range(0, len(points) - 3, 3):
        P0 = points[i + 1]
        P1 = points[i + 2]
        P2 = points[i + 3]
        P3 = points[i + 4]

        # cut out part for this curve
        t_part = t_full[(t_full >= P0[0]) & (t_full < P3[0])]
        # for formula: from 0 to 1
        t = (t_part - P0[0]) / (P3[0] - P0[0])
        # Bezier curve formula
        y_part = (1 - t)**3 * P0[1] + 3 * (1 - t)**2 * t * P1[1] + 3 * (1 - t) * t**2 * P2[1] + t**3 * P3[1]
        # add sections together
        t_final = np.append(t_final, t_part)
        y_final = np.append(y_final, y_part)

    return t_final, y_final

def keyframes_to_points(keyframes, interval):
    # find last keyframe
    max_joint_time = 0.0
    for i in range(len(keyframes[0])):
        new_joint_time = keyframes[1][i][-1]
        if new_joint_time > max_joint_time:
            max_joint_time = new_joint_time
    # make sure last point is included
    max_joint_time += interval

    all_points = {}

    # go through joints
    for i in range(len(keyframes[0])):
        joint_name = keyframes[0][i]
        joint_times = keyframes[1][i]
        joint_keys = keyframes[2][i]
        joint_points = []
        # go through keyframes
        for j in range(len(joint_times)):
            main_x = joint_times[j]
            whole_point = joint_keys[j]
            main_y = whole_point[0]
            handle_a = whole_point[1]
            handle_b = whole_point[2]
            handle_a_x = main_x + handle_a[1]
            handle_a_y = main_y + handle_a[2]
            handle_b_x = main_x + handle_b[1]
            handle_b_y = main_y + handle_b[2]
            # add three points per keyframe: handle - point - handle
            joint_points.append((handle_a_x, handle_a_y))
            joint_points.append((main_x, main_y))
            joint_points.append((handle_b_x, handle_b_y))

        # create first and last point of animation (2 handle + 1 point at same position)
        for j in range(3):
            joint_points.insert(0, (0, joint_points[1][1]))
        for j in range(3):
            joint_points.append((max_joint_time, joint_points[-2][1]))

        all_points[joint_name] = joint_points

    return all_points