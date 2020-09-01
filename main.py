import pathfinder as pf
import math

def generate_path(points_plus_angles):
    path_points = [pf.Waypoint(path_point["x"], path_point["y"], math.radians(path_point["angle"])) for path_point in points_plus_angles]

    path = pf.generate(path_points, pf.FIT_HERMITE_CUBIC, pf.SAMPLES_HIGH,
                   dt=0.05, max_velocity=1.7, max_acceleration=2, max_jerk=60)

    modifier = pf.modifiers.TankModifier(path).modify(0.5)

    return modifier

points = (
    {"x": 20, "y": 30, "angle": 30},
    {"x": 25, "y": 39, "angle": 30},
    {"x": 22, "y": 39, "angle": 30}
)
print(generate_path)


