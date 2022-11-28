import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np

def hyperfocal(focal_length, aperture_number, circle_oc_confusion_limit):
    return focal_length**2/(aperture_number * circle_oc_confusion_limit) + focal_length

def fov(focal_length, sensor_width):
    return 2*np.arctan(sensor_width / (2 * focal_length))

if __name__=='__main__':

    coc = .019 * u.millimeter #  https://en.wikipedia.org/wiki/Circle_of_confusion#Determining_a_circle_of_confusion_diameter_from_the_object_field
    f = np.arange(24,70) * u.millimeter
    N = np.asarray([2.8, 3.2, 3.5, 4, 4.5, 5.6, 6.3, 7.1, 8, 9, 10, 11, 13, 14, 16, 18, 20, 22])

    ff, NN, = np.meshgrid(f, N)

    H = hyperfocal(ff, NN, coc)

    width_apsc = 23.6 * u.mm
    print(fov(f, width_apsc).to(u.deg))