import numpy as np
from numpy.testing._private.utils import tempdir


def rot_y(theta_y, unit="radians"):

    if unit == "degrees":
        theta_y *= 2 * np.pi / 360

    s = np.sin(theta_y)
    c = np.cos(theta_y)
    return np.asarray([(c, 0, s), (0, 1, 0), (-s, 0, c)])


def rot_x(theta_x, unit="radians"):

    if unit == "degrees":
        theta_x *= 2 * np.pi / 360

    s = np.sin(theta_x)
    c = np.cos(theta_x)
    return np.asarray([(1, 0, 0), (0, c, -s), (0, s, c)])


def rot_z(theta_z, unit="radians"):

    if unit == "degrees":
        theta_z *= 2 * np.pi / 360

    s = np.sin(theta_z)
    c = np.cos(theta_z)
    return np.asarray([(c, -s, 0), (s, c, 0), (0, 0, 1)])


def tait_bryan_rotation_matrix(
    theta_z: float, theta_y: float, theta_x: float, unit="radians"
) -> np.ndarray:
    """
    @param theta_z: rotation about z-axis for first rotation in Tait-Bryan sequence
    @param theta_y: rotation about once-rotated y-axis for second rotation in Tait-Bryan sequence
    @param theta_x: rotation about twice-rotated x-axis for third rotation in Tait-Bryan sequence
    """

    if unit == "degrees":
        theta_x, theta_y, theta_z = (
            2 * x * np.pi / 360 for x in (theta_x, theta_y, theta_z)
        )

    elif unit == "radians":
        pass

    else:
        ValueError("Improper unit")

    rx = rot_x(theta_x, unit="radians")
    ry = rot_y(theta_y, unit="radians")
    rz = rot_z(theta_z, unit="radians")

    return np.matmul(rz, np.matmul(ry, rx))


def rotate_vector(R, v):
    """
    @param R: rotation matrix, from `rotation_matrix` function in this module
    @param v: vector to rotate, must be of shape (3,  n)
    """

    if v.shape[0] != 3:
        raise ValueError("v must be column vector(s)")

    vcount = v.shape[1]
    rotated = np.zeros((3, vcount))

    for i in range(vcount):
        rotated[:, i] = np.matmul(R, v).T

    return rotated


if __name__ == "__main__":
    v_imu = np.asarray([(-25.55), (-94.38), (142.0538)]).reshape((3, 1))
    R1 = tait_bryan_rotation_matrix(0, 61.6, 90, unit="degrees")
    R2 = tait_bryan_rotation_matrix(90, 0, 0, unit="degrees")

    R1_inv = np.linalg.inv(R1)
    R2_inv = np.linalg.inv(R2)

    print(v_ref)
