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
import re

print(" Load in JHU atlas and labels ")
ex_path = os.path.expanduser( "~/.antspyt1w/" )
JHU_atlas = ants.image_read( ex_path + 'JHU-ICBM-FA-1mm.nii.gz' ) # Read in JHU atlas
JHU_labels = ants.image_read( ex_path + 'JHU-ICBM-labels-1mm.nii.gz' ) # Read in JHU labels

#### Load in data ####
print("Load in subject data ...")
ex_path_mm = os.path.expanduser( "~/.antspymm/" )
lrid = "/Users/stnava/data/PPMI/PPMI2/temp/PPMI/41343/20210722/DTI_LR/I1498254/dcm2niix/V0/PPMI-41343-20210722-DTI_LR-I1498254-dcm2niix-V0.nii.gz"
rlid = "/Users/stnava/data/PPMI/PPMI2/temp/PPMI/41343/20210722/DTI_RL/I1498252/dcm2niix/V0/PPMI-41343-20210722-DTI_RL-I1498252-dcm2niix-V0.nii.gz"
lrid = ""
rlid = ""
# Load in image L-R
img_LR_in = ants.image_read( lrid  ) # LR dwi image
img_LR_bval = re.sub( '.nii.gz', '.bval', lrid ) # bval
img_LR_bvec = re.sub( '.nii.gz', '.bvec', lrid )
# Load in image R-L
img_RL_in = ants.image_read( rlid  ) # RL dwi image
img_RL_bval = re.sub( '.nii.gz', '.bval', rlid ) # bval
img_RL_bvec = re.sub( '.nii.gz', '.bvec', rlid )

print("START!")
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
    motion_correct = True,
    dewarp_modality = 'FA',
    verbose = True)

if True:
    ants.image_write( myoutx['dtrecon_LR']['FA'], '/tmp/temp1fa1.nii.gz'  )
    ants.image_write( myoutx['dtrecon_RL']['FA'], '/tmp/temp2fa1.nii.gz'  )
    ants.image_write( myoutx['dtrecon_LR_dewarp']['FA'], '/tmp/temp1fa2.nii.gz'  )
    ants.image_write( myoutx['dtrecon_RL_dewarp']['FA'], '/tmp/temp2fa2.nii.gz'  )
    ants.image_write( myoutx['dtrecon_LR_dewarp']['RGB'], '/tmp/temp1rgb.nii.gz'  )
    ants.image_write( myoutx['dtrecon_RL_dewarp']['RGB'], '/tmp/temp2rgb.nii.gz'  )
    ants.image_write( myoutx['recon_fa'], '/tmp/temp1fa.nii.gz'  )
    ants.image_write( myoutx['recon_md'], '/tmp/temp1md.nii.gz'  )
