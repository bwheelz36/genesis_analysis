from pathlib import Path
from mri_distortion_toolkit.MarkerAnalysis import MarkerVolume,MatchedMarkerVolumes
from time import perf_counter
from philips_phantom import philips_phantom
from mri_distortion_toolkit.utilities import plot_distortion_xyz_hist

this_file_loc = Path(__file__).parent.resolve()
data_loc = this_file_loc / '_segmentation_data'

# Distorted centroids corrected
philips_MR_corrected = MarkerVolume(data_loc / 'PhilipPhantom_MRI' / '2022-08__Studies\GOAM^ImageX_ZZZIMAGEX_MR_2022-08-31_172341_._T2.3D.Tra.2min_n401__00002' / 'slicer_centroids.mrk.json')
(x, y, z) = philips_phantom.get_alignment_coords(philips_MR_corrected)
philips_MR_corrected.MarkerCentroids = philips_MR_corrected.MarkerCentroids[philips_MR_corrected.MarkerCentroids['r'] < 190]
philips_MR_corrected.plot_3D_markers(title='MRI')

# Undistorted centroids
philips_centroids = philips_phantom.generate_centroids(x, y, z)
philips_gt = MarkerVolume(philips_centroids)

philips_gt.export_to_slicer(save_path=data_loc / 'PhilipPhantom_MRI' / 'Ground Truth')
philips_gt.plot_3D_markers(title='Ground truth')

# Match markers
corrected = MatchedMarkerVolumes(philips_gt, philips_MR_corrected)
corrected.plot_3D_markers()
plot_distortion_xyz_hist(corrected)

