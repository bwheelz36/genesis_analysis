from mri_distortion_toolkit.MarkerAnalysis import MarkerVolume, MatchedMarkerVolumes
from mri_distortion_toolkit.utilities import plot_distortion_xyz_hist
import numpy as np

# create marker volumes:
mr_volume_with_DC = MarkerVolume(r'_segmentation_data\GOAM_MRI\2022-08__Studies\GOAM^ImageX_ZZZIMAGEX_MR_2022-08-31_172341_._T2.3D.Tra.2min_n301__00002\slicer_centroids.mrk.json')
mr_volume_no_DC = MarkerVolume(r'_segmentation_data\GOAM_MRI\2022-08__Studies\GOAM^ImageX_ZZZIMAGEX_MR_2022-08-31_172341_._T2.3D.Tra.2min_n301__00001\slicer_centroids.mrk.json')
ct_volume = MarkerVolume(r'_segmentation_data\GOAM_CT\slicer_centroids.mrk.json')

# match markers:
no_DC_match = MatchedMarkerVolumes(ct_volume, mr_volume_no_DC, n_refernce_markers=7)
with_DC_match = MatchedMarkerVolumes(ct_volume, mr_volume_with_DC, n_refernce_markers=7)

from mri_distortion_toolkit.FieldCalculation import ConvertMatchedMarkersToBz
from mri_distortion_toolkit import calculate_harmonics
from pathlib import Path

Bz_field = ConvertMatchedMarkersToBz(no_DC_match.MatchedCentroids, mr_volume_no_DC.dicom_data)
gradient_strength = np.array(mr_volume_no_DC.dicom_data['gradient_strength'])
normalisation_factor = [1 / gradient_strength[0], 1 / gradient_strength[1], 1 / gradient_strength[2],
                        1]  # this normalised gradient harmonics to 1mT/m
G_x_Harmonics, G_y_Harmonics, G_z_Harmonics, B0_Harmonics = calculate_harmonics(Bz_field.MagneticFields,
                                                                                n_order=5,
                                                                                norm=normalisation_factor)

from mri_distortion_toolkit.DistortionCorrection import ImageDomainDistortionCorrector, KspaceDistortionCorrector
distorted_data_loc = Path(r'C:\Users\Brendan\Downloads\GOAM-01092022_Genesis\GOAM\GOAM_MRI\2022-08__Studies\GOAM^ImageX_ZZZIMAGEX_MR_2022-08-31_172341_._T2.3D.Tra.2min_n301__00001')
GDC = ImageDomainDistortionCorrector(ImageDirectory=distorted_data_loc.resolve(),
                                gradient_harmonics=[G_x_Harmonics.harmonics,
                                                    G_y_Harmonics.harmonics,
                                                    G_z_Harmonics.harmonics],
                                dicom_data=mr_volume_no_DC.dicom_data,
                                correct_through_plane=True,
                                pad=0)

GDC.correct_all_images()
GDC.save_all_images()  # saves as png so you can quickly inspect results
GDC.save_all_images_as_dicom()  # saves as dicom which can be read into analysis packages.