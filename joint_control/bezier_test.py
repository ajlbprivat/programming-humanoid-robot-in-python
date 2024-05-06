import numpy as np
import matplotlib.pyplot as plt
from keyframes import hello

def bezier_curve(P0, P1, P2, P3, num_points=100):
    # Parameter values (i) for the curve
    t = np.linspace(0, 1, num_points)

    # Bezier curve formula
    B_x = (1 - t)**3 * P0[0] + 3 * (1 - t)**2 * t * P1[0] + 3 * (1 - t) * t**2 * P2[0] + t**3 * P3[0]
    B_y = (1 - t)**3 * P0[1] + 3 * (1 - t)**2 * t * P1[1] + 3 * (1 - t) * t**2 * P2[1] + t**3 * P3[1]

    return B_x, B_y

def plot_bezier(points):
    plt.figure()
    
    for i in range(0, len(points) - 3, 3):
        P0 = points[i + 1]
        P1 = points[i + 2]
        P2 = points[i + 3]
        P3 = points[i + 4]

        # Calculate Bezier curve points for this section
        curve_x, curve_y = bezier_curve(P0, P1, P2, P3)
        
        # Plot the Bezier curve
        plt.plot(curve_x, curve_y, label=f'Section {i//3+1}')

    # Plot the control points
    for i, point in enumerate(points):
        plt.scatter(point[0], point[1], c='r')

    plt.title('Bezier Curve')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_bezier_keyframes(keyframes):
    for i in range(len(keyframes[0])):
        joint_name = keyframes[0][i]
        joint_times = keyframes[1][i]
        joint_keys = keyframes[2][i]
        joint_points = []
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
            joint_points.append((handle_a_x, handle_a_y))
            joint_points.append((main_x, main_y))
            joint_points.append((handle_b_x, handle_b_y))

        # print(joint_points)
        plot_bezier(joint_points)

# # Example points (P1, H1a, H1b, P2, H2a, H2b, P3, H3a, H3b)
# points = [(0.5, 1), (1, 1), (1.5, 1),   # H1a, P1, H1b
#           (2.5, 3), (3, 3), (3.5, 3),   # H2a, P2, H2b
#           (4.5, 2), (5, 2), (5.5, 2)]   # H3a, P3, H3b

# plot_bezier(points)

keyframes = hello()
plot_bezier_keyframes(keyframes)
