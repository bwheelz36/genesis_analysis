from mri_distortion_toolkit.utilities import get_all_files
import dicom2nifti
from pathlib import Path

dicom_location = Path(r'C:\Users\Brendan\cloudstor\Shared\MRI-Linac Experimental Data\GOAM-01092022_Genesis\GOAM\GOAM_CT\2022-08__Studies\ImageX^GOAM_ZZZIMAGEX_CT_2022-08-31_170444_RT^01.Pelvis.Customized.(Adult)_Pelvis..2.0..B31f_n178__00000')

dicom2nifti.dicom_series_to_nifti(dicom_location, dicom_location / 'gah', reorient_nifti=True)