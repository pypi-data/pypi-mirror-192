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
# load in t1w
t1wh = ants.iMath( ants.image_read( ex_path_mm + "140117_T1w.nii.gz" ), "Normalize" )
t1w = t1wh * antspyt1w.brain_extraction( t1wh )
bxtdwi = antspymm.t1_based_dwi_brain_extraction( t1wh, t1w, img_LR_in,
    transform='Rigid', deform=True, verbose=True )
# ants.plot( bxtdwi['b0_avg'], bxtdwi['b0_mask' ], overlay_alpha=0.5 , axis=2 )
# ants.plot( bxtdwi['b0_avg'], bxtdwi['b0_mask' ], overlay_alpha=0.5 , axis=1 )
# ants.plot( bxtdwi['b0_avg'], bxtdwi['b0_mask' ], overlay_alpha=0.5 , axis=0 )
# derka
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
    motion_correct = 'SyN',
    dewarp_modality = 'FA',
    brain_mask = bxtdwi['b0_mask' ],
    t1w=t1w,
    denoise=True,
    verbose = True)

if True:
    ants.image_write( myoutx['dtrecon_LR']['FA'], '/tmp/temp1fa1.nii.gz'  )
    ants.image_write( myoutx['dtrecon_LR']['motion_corrected'], '/tmp/temp1moco.nii.gz'  )
    ants.image_write( myoutx['dtrecon_RL']['FA'], '/tmp/temp2fa1.nii.gz'  )
    ants.image_write( myoutx['dtrecon_LR_dewarp']['FA'], '/tmp/temp1fa2.nii.gz'  )
    ants.image_write( myoutx['dtrecon_RL_dewarp']['FA'], '/tmp/temp2fa2.nii.gz'  )
    ants.image_write( myoutx['dtrecon_LR']['RGB'], '/tmp/temp1rgb1.nii.gz'  )
    ants.image_write( myoutx['dtrecon_RL']['RGB'], '/tmp/temp2rgb2.nii.gz'  )
    ants.image_write( myoutx['dtrecon_LR_dewarp']['RGB'], '/tmp/temp1rgb.nii.gz'  )
    ants.image_write( myoutx['dtrecon_RL_dewarp']['RGB'], '/tmp/temp2rgb.nii.gz'  )
    ants.image_write( myoutx['recon_fa'], '/tmp/temp1fa.nii.gz'  )
    ants.image_write( myoutx['recon_md'], '/tmp/temp1md.nii.gz'  )
