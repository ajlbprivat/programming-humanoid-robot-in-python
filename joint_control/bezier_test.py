import matplotlib.pyplot as plt
from keyframes import hello
from bezier import keyframes_to_points, points_to_graph

def plot_graph(x, y, points):
    plt.figure()
    plt.plot(x, y)

    # Plot the control points
    for i, point in enumerate(points):
        plt.scatter(point[0], point[1], c='r')

    plt.title('Bezier Curve')
    plt.xlabel('X')
    plt.ylabel('Y')
    # plt.legend()
    plt.grid(True)
    plt.show()

interval = 0.3
keyframes = hello()
all_points = keyframes_to_points(keyframes, interval)
points = all_points['RShoulderPitch']
x, y = points_to_graph(points, interval)
plot_graph(x, y, points)
