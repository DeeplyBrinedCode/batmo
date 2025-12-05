from polarchart import *
import math
import matplotlib

def update_plot_from_list(points):
    """
    Update the polar plot with a predefined list of points.
    Parameters
    ----------
    points : list of tuples
    Each tuple represents a point as (angle_in_degrees, distance_in_cm).
    Behavior
    --------
    Converts angles from degrees to radians for polar plotting. Clears the previous plot. Plots all points on a polar graph.
    Sets the plot title and radial maximum based on the largest distance.
    """
    # Clear previous plot
    ax.clear()

    if points:
        # Convert angles to radians for polar plotting
        thetas = [math.radians(angle) for angle, dist in points]
        rs = [dist for angle, dist in points]

        # Plot points
        ax.plot(thetas, rs, marker='o', linestyle='-')

        # Set maximum radius to largest distance
        ax.set_rmax(100)

    ax.set_title("Polar Plot of Predefined Points")
    fig.canvas.draw()
    fig.canvas.flush_events()