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
ex_path_mm = "/Users/stnava/Downloads/PPMI_100006_20201216/"
JHU_atlas = ants.image_read( ex_path + 'JHU-ICBM-FA-1mm.nii.gz') # Read in JHU atlas
JHU_labels = ants.image_read( ex_path + 'JHU-ICBM-labels-1mm.nii.gz') # Read in JHU labels

#### Load in data ####
print("Load in subject data ...")
lrid = ex_path_mm + "PPMI-100006-20201216-DTI_30dir_LR-I1526388"
rlid = ex_path_mm + "PPMI-100006-20201216-DTI_30dir_RL-I1526387"
# Load in image L-R
img_LR_in = ants.image_read( lrid + '.nii.gz') # LR dwi image
img_LR_bval = lrid + '.bval' # bval
img_LR_bvec = lrid + '.bvec'
img_RL_in = ants.image_read( rlid + '.nii.gz') # LR dwi image
img_RL_bval = rlid + '.bval' # bval
img_RL_bvec = rlid + '.bvec'
print("begin")

myoutx = antspymm.joint_dti_recon(
        img_LR_in,
        img_LR_bval,
        img_LR_bvec,
        jhu_atlas=JHU_atlas,
        jhu_labels=JHU_labels,
        img_RL = img_RL_in,
        bval_RL = img_RL_bval,
        bvec_RL = img_RL_bvec,
        srmodel=None,
        motion_correct=True,
        verbose = True)

doit=True
if doit:
    ants.image_write( myoutx['dtrecon_LR']['RGB'], '/tmp/temp1.nii.gz'  )
    ants.image_write( myoutx['dtrecon_LR_dewarp']['RGB'], '/tmp/temp2.nii.gz'  )
    ants.image_write( myoutx['recon_fa'], '/tmp/temp1fa.nii.gz'  )
    ants.image_write( myoutx['recon_md'], '/tmp/temp1md.nii.gz'  )
    ants.image_write( myoutx['t1w_rigid'], '/tmp/tempt1w.nii.gz'  )
