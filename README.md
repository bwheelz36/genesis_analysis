# genesis_analysis
temporary repo to store anaylsis of genesis data

- _segmentation data holds the json files for previous segmentations - all MRs done but no CTs
- I was struggling to read the CT data into slicer, so the `_dicom_to_nii.py` script converts them to nifti which can be read in
- it might also be easier to just construct a model based ground truth based on the phantom construction, although alignment will still be a challenge... I will also add in the info about this phantom I have
