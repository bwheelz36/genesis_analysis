from pathlib import Path
from mri_distortion_toolkit.MarkerAnalysis import MarkerVolume,MatchedMarkerVolumes
from mri_distortion_toolkit.utilities import plot_distortion_xyz_hist
from philips_phantom import philips_phantom

this_file_loc = Path(__file__).parent.resolve()
data_loc = this_file_loc.parent / '_segmentation_data'

# Distorted centroids corrected
philips_MR_corrected = MarkerVolume(data_loc / 'PhilipPhantom_MRI' / '2022-08__Studies\GOAM^ImageX_ZZZIMAGEX_MR_2022-08-31_172341_._T2.3D.Tra.2min_n401__00002' / 'slicer_centroids.mrk.json')
(x, y, z) = philips_phantom.get_alignment_coords(philips_MR_corrected)
# philips_MR_corrected.MarkerCentroids = philips_MR_corrected.MarkerCentroids[philips_MR_corrected.MarkerCentroids['r'] < 190]
# philips_MR_corrected.plot_3D_markers(title='MRI')

# Undistorted centroids
philips_centroids = philips_phantom.generate_centroids(x, y, z)
philips_gt = MarkerVolume(philips_centroids)

# philips_gt.export_to_slicer(save_path=data_loc / 'PhilipPhantom_MRI' / 'Ground Truth')
# philips_gt.plot_3D_markers(title='Ground truth')

# # Match markers corrected
corrected = MatchedMarkerVolumes(philips_gt, philips_MR_corrected)
corrected.plot_3D_markers()
plot_distortion_xyz_hist(corrected)

# Distorted centroids uncorrected
philips_MR_uncorrected = MarkerVolume(data_loc / 'PhilipPhantom_MRI' / '2022-08__Studies\GOAM^ImageX_ZZZIMAGEX_MR_2022-08-31_172341_._T2.3D.Tra.2min_n401__00000' / 'slicer_centroids.mrk.json')
philips_MR_uncorrected.MarkerCentroids = philips_MR_uncorrected.MarkerCentroids[philips_MR_uncorrected.MarkerCentroids['r'] < 190]
philips_MR_uncorrected.plot_3D_markers(title='MRI uncorrected')

# Match markers corrected
uncorrected = MatchedMarkerVolumes(philips_gt, philips_MR_uncorrected)
uncorrected.plot_3D_markers()
plot_distortion_xyz_hist(uncorrected)

print(f'Median distortion: {uncorrected.MatchedCentroids.match_distance.median(): 1.1f} mm, '
      f'Max distortion: {uncorrected.MatchedCentroids.match_distance.max(): 1.1f} mm')

from mri_distortion_toolkit.Reports import MRI_QA_Reporter
from mri_distortion_toolkit.Reports import Elekta_Distortion_tests

report = MRI_QA_Reporter(MatchedMarkerVolume=corrected.MatchedCentroids,
                         r_outer=190,
                         dicom_data=philips_MR_uncorrected.dicom_data,
                         tests_to_run=Elekta_Distortion_tests)
# report.write_html_report()

from mri_distortion_toolkit.FieldCalculation import ConvertMatchedMarkersToBz
from mri_distortion_toolkit import calculate_harmonics
import numpy as np

Bz = ConvertMatchedMarkersToBz(uncorrected.MatchedCentroids, philips_MR_uncorrected.dicom_data)
gradient_strength = np.array(philips_MR_uncorrected.dicom_data['gradient_strength'])
normalisation_factor = [1 / gradient_strength[0], 1 / gradient_strength[1], 1 / gradient_strength[2], 1]
# this normalised gradient harmonics to 1mT/m
G_x_Harmonics, G_y_Harmonics, G_z_Harmonics, B0_Harmonics = calculate_harmonics(Bz.MagneticFields,
                                                                                n_order=5,
                                                                                norm=normalisation_factor)

report_harmonics = MRI_QA_Reporter(gradient_harmonics=[G_x_Harmonics.harmonics,
                                                       G_y_Harmonics.harmonics,
                                                       G_z_Harmonics.harmonics],
                                     r_outer=190,
                                     dicom_data=philips_MR_uncorrected.dicom_data,
                                     tests_to_run=Elekta_Distortion_tests)
report_harmonics.write_html_report()
