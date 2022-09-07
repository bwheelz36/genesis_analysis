from pathlib import Path
from mri_distortion_toolkit.utilities import get_all_files
import dicom2nifti



data_loc = Path(r'C:\Users\Brendan\cloudstor\Shared\MRI-Linac Experimental Data\GOAM-01092022_Genesis\GOAM\PhilipPhantom_CT\2022-08__Studies\Philips^Distortion_ZZZTEST_CT_2022-08-31_165114_RT^01.Pelvis.Customized.(Adult)_Pelvis..2.0..HD.FoV_n230__00000')
all_files = get_all_files(data_loc, file_extension='DCM')

dicom2nifti.dicom_series_to_nifti(data_loc, data_loc / 'gah', reorient_nifti=True)