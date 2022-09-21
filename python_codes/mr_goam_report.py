from pathlib import Path
from mri_distortion_toolkit.utilities import get_all_files, plot_distortion_xyz_hist
from mri_distortion_toolkit.MarkerAnalysis import MarkerVolume, MatchedMarkerVolumes
import numpy as np

this_file_loc = Path(__file__).parent.resolve()
data_loc = this_file_loc.parent / '_segmentation_data'

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
matched_volume3 = MatchedMarkerVolumes(ground_truth_volume, distorted_volume3, n_refernce_markers=7)
# fields
from mri_distortion_toolkit.FieldCalculation import ConvertMatchedMarkersToBz
Fields = ConvertMatchedMarkersToBz(matched_volume3.MatchedCentroids, distorted_volume3.dicom_data)
# harmonics
from mri_distortion_toolkit import calculate_harmonics
gradient_strength = np.array(distorted_volume3.dicom_data['gradient_strength'])
normalisation_factor = [1 / gradient_strength[0], 1 / gradient_strength[1], 1 / gradient_strength[2],
                        1]  # this normalised gradient harmonics to 1mT/m
Gx, Gy, Gz, B0 = calculate_harmonics(Fields.MagneticFields, n_order=5, norm=normalisation_factor)
# report
from mri_distortion_toolkit.Reports import MRI_QA_Reporter

report_harmonics = MRI_QA_Reporter(gradient_harmonics=[Gx.harmonics,
                                                       Gy.harmonics,
                                                       Gz.harmonics],
                                     dicom_data=distorted_volume3.dicom_data)
report_harmonics.write_html_report()
