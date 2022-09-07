from pathlib import Path
from mri_distortion_toolkit.MarkerAnalysis import MarkerVolume
from time import perf_counter

CT_data_loc = Path(r'C:\Users\pliu4890\OneDrive - The University of Sydney (Staff)\Documents\MRI-Linac\Experiments\20220901 Genesis Goam\CT\GOAM')
time_start = perf_counter()
CT_volume = MarkerVolume(CT_data_loc, ImExtension='dcm', n_markers_expected=531, gaussian_image_filter_sd=0, verbose=True)
print(f'time: {perf_counter() - time_start}')
CT_volume.plot_3D_markers()
CT_volume.export_to_slicer()

mri_1_data_loc = Path(r'C:\Users\Brendan\cloudstor\Shared\MRI-Linac Experimental Data\GOAM-01092022_Genesis\GOAM\GOAM_MRI\2022-08__Studies\GOAM^ImageX_ZZZIMAGEX_MR_2022-08-31_172341_._T2.3D.Tra.2min_n301__00000')
mri_2_data_loc = Path(r'C:\Users\Brendan\cloudstor\Shared\MRI-Linac Experimental Data\GOAM-01092022_Genesis\GOAM\GOAM_MRI\2022-08__Studies\GOAM^ImageX_ZZZIMAGEX_MR_2022-08-31_172341_._T2.3D.Tra.2min_n301__00001')
mri_3_data_loc = Path(r'C:\Users\Brendan\cloudstor\Shared\MRI-Linac Experimental Data\GOAM-01092022_Genesis\GOAM\GOAM_MRI\2022-08__Studies\GOAM^ImageX_ZZZIMAGEX_MR_2022-08-31_172341_._T2.3D.Tra.2min_n301__00002')

time_start = perf_counter()
mri_1_vol = MarkerVolume(mri_1_data_loc, r_max=170, n_markers_expected=531)
print(f'time: {perf_counter() - time_start}')
mri_1_vol.export_to_slicer()
mri_1_vol.save_dicom_data()

mri_2_vol = MarkerVolume(mri_2_data_loc, n_markers_expected=531)
mri_2_vol.export_to_slicer()
mri_2_vol.save_dicom_data()

mri_3_vol = MarkerVolume(mri_3_data_loc, n_markers_expected=531)
mri_3_vol.export_to_slicer()
mri_3_vol.save_dicom_data()