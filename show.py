import viser
import numpy as np
import argparse
from pathlib import Path
import time
from plyfile import PlyData

INIT_POINT_SIZE = 0.003

def main():

    # ----------------
    # READ IN PLY FILE
    # ----------------

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "ply_path",
        help=("Path to the ply point cloud file"),
        type=Path
    )
    args = parser.parse_args()
    ply_path = args.ply_path
    pcd = read_ply(ply_path)

    # ----------------
    # RUN THE VISER SERVER
    # ----------------

    server = viser.ViserServer()

    cloud_handle = server.scene.add_point_cloud(
        "/cloud",
        points=pcd,
        point_size=INIT_POINT_SIZE,
        colors=(80, 80, 255)
    )

    sonar_point_size_slider = server.gui.add_slider(
        "Point size",
        min=0.0005,
        max=0.01,
        step=0.0005,
        initial_value=INIT_POINT_SIZE,
    )

    @sonar_point_size_slider.on_update
    def _(_):
        cloud_handle.point_size = sonar_point_size_slider.value

    @server.on_client_connect
    def _(_):
        fit_initial_camera(server, pcd)

    while True:
        time.sleep(1)


def read_ply(path):
    ply = PlyData.read(path)
    vertices = ply["vertex"].data

    points = np.column_stack((
        vertices["x"],
        vertices["y"],
        vertices["z"],
    )).astype(np.float32)

    return points


def fit_initial_camera(server, point_cloud, margin=1.3):
    """
    Find pose of initial camera to have the given point cloud fully in view
    Set that initial view on the passed server object

    point_cloud:
        point cloud that is aligned. np.array of (N, 3)
        Needs to be in world coordinates.
    """

    pmin = point_cloud.min(axis=0)
    pmax = point_cloud.max(axis=0)

    center = 0.5 * (pmin + pmax)
    radius = 0.5 * np.linalg.norm(pmax - pmin)

    # Choose a reasonable viewing direction from the scene.
    view_dir = np.array([1.0, -1.0, 0.7])
    view_dir /= np.linalg.norm(view_dir)

    # Viser's initial_camera.fov is the vertical FOV.
    fov_y = server.initial_camera.fov

    distance = margin * radius / np.tan(fov_y / 2.0)

    camera_position = center + distance * view_dir

    server.initial_camera.position = camera_position
    server.initial_camera.look_at = center
    server.initial_camera.up = (0.0, 0.0, 1.0)


if __name__ == "__main__":
    main()