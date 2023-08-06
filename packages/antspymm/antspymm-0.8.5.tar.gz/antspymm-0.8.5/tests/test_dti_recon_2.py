import ants
import antspymm
lrid = "/Users/stnava/data/PPMI/PPMI2/temp/PPMI/41343/20210722/DTI_LR/I1498254/dcm2niix/V0/PPMI-41343-20210722-DTI_LR-I1498254-dcm2niix-V0.nii.gz"
img_LR_in = ants.image_read( lrid  ) # LR dwi image
img_LR_bval = re.sub( '.nii.gz', '.bval', lrid ) # bval
img_LR_bvec = re.sub( '.nii.gz', '.bvec', lrid )
dd = antspymm.dipy_dti_recon( img_LR_in, img_LR_bval, img_LR_bvec, motion_correct=False, mask_dilation=0 )
ee = antspymm.dipy_dti_recon( img_LR_in, img_LR_bval, img_LR_bvec, motion_correct=True, mask_dilation=0 )
