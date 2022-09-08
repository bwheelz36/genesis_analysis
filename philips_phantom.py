import numpy
import numpy as np
from mri_distortion_toolkit.MarkerAnalysis import MarkerVolume


class philips_phantom:

    @staticmethod
    def generate_centroids(center_x, center_y, center_z):
        """
        Generates centroids positions of the Philips phantom
        Assumes phantom is aligned along z (SI direction)

        Phantom: 7 panes of 276 markers. Panes spaced 55 mm apart. Marker pitch is 25 mm
        Each pane has 16 rows and maximum 21 columns

        Row 1: 5 markers
        Row 2: 9
        Row 3: 13
        Row 4: 15
        Row 5-6: 17
        Row 7-8: 19
        Row 9-13: 21
        Row 14-16:19

        """

        centroids = np.empty((0, 3), int)

        # Assuming that middle column, bottom row, central slice is (0,0,0)
        z_values = np.arange(-165, 165+1, 55)
        y_values = np.arange(0, -375 - 1, -25)
        x_n_markers = [19, 19, 19, 21, 21, 21, 21, 21, 19, 19, 17, 17, 15, 13, 9, 5]

        for z in z_values:
            for index, y in enumerate(y_values):
                x_values = np.arange(-((x_n_markers[index] - 1) / 2) * 25, ((x_n_markers[index] - 1) / 2) * 25 + 1, 25)
                for x in x_values:

                    xx = x + center_x
                    yy = y + center_y
                    zz = z + center_z

                    centroids = np.append(centroids, np.array([[xx, yy, zz]]), axis=0)

        return centroids

    @staticmethod
    def get_alignment_coords(_markervolume):

        middleX = (_markervolume.MarkerCentroids.x.max() + _markervolume.MarkerCentroids.x.min()) / 2
        maxY = _markervolume.MarkerCentroids.y.max()
        middleZ = (_markervolume.MarkerCentroids.z.max() + _markervolume.MarkerCentroids.z.min()) / 2

        return middleX, maxY, middleZ
