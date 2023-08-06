import os
os.environ["TF_NUM_INTEROP_THREADS"] = "8"
os.environ["TF_NUM_INTRAOP_THREADS"] = "8"
os.environ["ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS"] = "8"
from os.path import exists
from dipy.io.image import save_nifti, load_nifti
import antspymm
import antspyt1w
import antspynet
import ants
import pandas as pd
import tensorflow as tf
ex_path = os.path.expanduser( "~/.antspyt1w/" )
ex_path_mm = "/Users/stnava/data/HCP/DWI/140117/"
JHU_atlas = ants.image_read( ex_path + 'JHU-ICBM-FA-1mm.nii.gz') # Read in JHU atlas
JHU_labels = ants.image_read( ex_path + 'JHU-ICBM-labels-1mm.nii.gz') # Read in JHU labels
print("Load in HCP subject data for joint_dti_recon testing ...")
lrid = ex_path_mm + "140117_3T_DWI_dir95_LR"
rlid = ex_path_mm + "140117_3T_DWI_dir95_RL"
# Load in image L-R
img_LR_in = ants.image_read( lrid + '.nii.gz') # LR dwi image
img_LR_bval = lrid + '.bval' # bval
img_LR_bvec = lrid + '.bvec'
img_RL_in = ants.image_read( rlid + '.nii.gz') # LR dwi image
img_RL_bval = rlid + '.bval' # bval
img_RL_bvec = rlid + '.bvec'

a1b,a1w=antspymm.get_average_dwi_b0(img_LR_in)
a2b,a2w=antspymm.get_average_dwi_b0(img_RL_in)
btpB0, btpDW = antspymm.dti_template(
        b_image_list=[a1b,a2b],
        w_image_list=[a1w,a2w],
        iterations=7, verbose=True )

t1wh = ants.iMath( ants.image_read( ex_path_mm + "140117_T1w.nii.gz" ), "Normalize" )
t1bxt = antspyt1w.brain_extraction( t1wh )
t1w = t1wh * t1bxt
initrig = ants.registration( btpDW, t1w, 'BOLDRigid' )['fwdtransforms'][0]
tempreg = ants.registration( btpDW, t1w, 'SyNOnly',
                syn_metric='mattes', syn_sampling=32,
                reg_iterations=[50,50,20],
                multivariate_extras=[ [ "mattes", btpB0, t1w, 1, 32 ]],
                initial_transform=initrig
                )
dwimask = ants.apply_transforms( btpDW, t1bxt, tempreg['fwdtransforms'][1], interpolator='nearestNeighbor')
###########################
myoutx = antspymm.joint_dti_recon(
    img_LR_in,
    img_LR_bval,
    img_LR_bvec,
    jhu_atlas = JHU_atlas,
    jhu_labels = JHU_labels,
    srmodel = None,
    img_RL = img_RL_in,
    bval_RL = img_RL_bval,
    bvec_RL = img_RL_bvec,
    reference_B0=btpB0,
    reference_DWI=btpDW,
    brain_mask=dwimask,
    motion_correct = 'SyN',
    verbose = True)
if True:
    ants.image_write( myoutx['dtrecon_LR']['FA'], '/tmp/temp1fa1.nii.gz'  )
    ants.image_write( myoutx['dtrecon_LR']['motion_corrected'], '/tmp/temp1moco.nii.gz'  )
    ants.image_write( myoutx['dtrecon_RL']['FA'], '/tmp/temp2fa1.nii.gz'  )
    ants.image_write( myoutx['dtrecon_LR_dewarp']['FA'], '/tmp/temp1fa2.nii.gz'  )
    ants.image_write( myoutx['dtrecon_LR_dewarp']['RGB'], '/tmp/temp1rgb.nii.gz'  )
    ants.image_write( myoutx['recon_fa'], '/tmp/temp1fa.nii.gz'  )
    ants.image_write( myoutx['recon_md'], '/tmp/temp1md.nii.gz'  )


myoutxRig = antspymm.joint_dti_recon(
    img_LR_in,
    img_LR_bval,
    img_LR_bvec,
    jhu_atlas = JHU_atlas,
    jhu_labels = JHU_labels,
    srmodel = None,
    img_RL = img_RL_in,
    bval_RL = img_RL_bval,
    bvec_RL = img_RL_bvec,
    reference_B0=btpB0,
    reference_DWI=btpDW,
    brain_mask=dwimask,
    motion_correct = 'Rigid',
    verbose = True)
if True:
    ants.image_write( myoutx['dtrecon_LR']['FA'], '/tmp/temp1fa1.nii.gz'  )
    ants.image_write( myoutx['dtrecon_LR']['motion_corrected'], '/tmp/temp1moco.nii.gz'  )
    ants.image_write( myoutx['dtrecon_RL']['FA'], '/tmp/temp2fa1.nii.gz'  )
    ants.image_write( myoutx['dtrecon_LR_dewarp']['FA'], '/tmp/temp1fa2.nii.gz'  )
    ants.image_write( myoutx['dtrecon_LR_dewarp']['RGB'], '/tmp/temp1rgb.nii.gz'  )
    ants.image_write( myoutx['recon_fa'], '/tmp/temp1fa.nii.gz'  )
    ants.image_write( myoutx['recon_md'], '/tmp/temp1md.nii.gz'  )
