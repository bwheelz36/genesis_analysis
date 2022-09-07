from pathlib import Path
from mri_distortion_toolkit.utilities import get_all_files, plot_distortion_xyz_hist
from mri_distortion_toolkit.MarkerAnalysis import MarkerVolume, MatchedMarkerVolumes
import dicom2nifti

this_file_loc = Path(__file__).parent.resolve()
data_loc = this_file_loc / '_segmentation_data'

# ground truth centroids
ground_truth_volume = MarkerVolume(data_loc / 'GOAM_CT' / 'slicer_centroids.mrk.json')
# ground_truth_volume.plot_3D_markers(title='CT')

# distorted centroids
distorted_volume1 = MarkerVolume(data_loc / 'GOAM_MRI' / '2022-08__Studies/GOAM^ImageX_ZZZIMAGEX_MR_2022-08-31_172341_._T2.3D.Tra.2min_n301__00000' / 'slicer_centroids.mrk.json')
# distorted_volume.plot_3D_markers(title='MR1')

distorted_volume2 = MarkerVolume(data_loc / 'GOAM_MRI' / '2022-08__Studies/GOAM^ImageX_ZZZIMAGEX_MR_2022-08-31_172341_._T2.3D.Tra.2min_n301__00001' / 'slicer_centroids.mrk.json')
# distorted_volume.plot_3D_markers(title='MR1')

distorted_volume3 = MarkerVolume(data_loc / 'GOAM_MRI' / '2022-08__Studies/GOAM^ImageX_ZZZIMAGEX_MR_2022-08-31_172341_._T2.3D.Tra.2min_n301__00002' / 'slicer_centroids.mrk.json')
# distorted_volume.plot_3D_markers(title='MR1')

# matched volumes
matched_volume1 = MatchedMarkerVolumes(ground_truth_volume, distorted_volume1, n_refernce_markers=7)
# matched_volume1.plot_3D_markers()
plot_distortion_xyz_hist(matched_volume1)

matched_volume2 = MatchedMarkerVolumes(ground_truth_volume, distorted_volume2, n_refernce_markers=7)
matched_volume2.plot_3D_markers()
plot_distortion_xyz_hist(matched_volume2)

matched_volume3 = MatchedMarkerVolumes(ground_truth_volume, distorted_volume3, n_refernce_markers=7)
matched_volume3.plot_3D_markers()
plot_distortion_xyz_hist(matched_volume3)