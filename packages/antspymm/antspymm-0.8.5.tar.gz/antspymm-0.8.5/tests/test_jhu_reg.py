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

print(" Load in JHU atlas and labels ")
ex_path = os.path.expanduser( "~/.antspyt1w/" )
ex_path_mm = os.path.expanduser( "~/.antspymm/" )
JHU_atlas = ants.image_read( ex_path + 'JHU-ICBM-FA-1mm.nii.gz' ) # Read in JHU atlas
JHU_labels = ants.image_read( ex_path + 'JHU-ICBM-labels-1mm.nii.gz' ) # Read in JHU labels

#### Load in data ####
print("Load in subject data ...")
lrid = ex_path_mm + "I1499279_Anon_20210819142214_5"
rlid = ex_path_mm + "I1499337_Anon_20210819142214_6"
# Load in image L-R
img_LR_in = ants.image_read( lrid + '.nii.gz') # LR dwi image
img_LR_bval = lrid + '.bval' # bval
img_LR_bvec = lrid + '.bvec'
# Load in image R-L
img_RL_in = ants.image_read( rlid + '.nii.gz' ) # RL dwi image
img_RL_bval = lrid + '.bval' # bval
img_RL_bvec = lrid + '.bvec'

print("ee")
eem = antspymm.dipy_dti_recon( img_RL_in, img_RL_bval, img_RL_bvec, autocrop=False, motion_correct=True  )
ants.image_write( eem['motion_corrected'], '/tmp/moco1.nii.gz' )
print("dd")
ddm = antspymm.dipy_dti_recon( img_LR_in, img_LR_bval, img_LR_bvec, autocrop=False, motion_correct=True )
ants.image_write( ddm['motion_corrected'], '/tmp/moco2.nii.gz' )

avgdd = ants.get_average_of_timeseries( ddm['motion_corrected'] )
avgee = ants.get_average_of_timeseries( eem['motion_corrected'] )
bb = antspynet.brain_extraction( avgdd, 't2' ).threshold_image(0.5,1)
bbb = ants.iMath(bb,"MD",4)
cc = antspynet.brain_extraction( avgee, 't2' ).threshold_image(0.5,1)
ccc = ants.iMath( cc, "MD",4)
JHU_atlas_aff1 = ants.registration( avgdd*bb, JHU_atlas, 'Affine' )['warpedmovout']


dwp_OR = antspymm.dewarp_imageset(
            [ avgdd, avgee ],
            initial_template=ants.crop_image( avgdd, bbb ),
            iterations = 5,
            syn_metric='CC',
            syn_sampling=2,
            reg_iterations=[100,100,20,0] )

def concat_dewarp( refimg, originalDWI, dwpTx, motion_parameters, motion_correct=True ):
    dwpimage = []
    for myidx in range(originalDWI.shape[3]):
        b0 = ants.slice_image( originalDWI, axis=3, idx=myidx)
        if not motion_correct:
            concatx = dwpTx
        if motion_correct:
            concatx = motion_parameters[myidx].copy()
            for j in range(len(dwpTx)):
                concatx.append( dwpTx[j]  )
        warpedb0 = ants.apply_transforms( refimg, b0, concatx )
        dwpimage.append( warpedb0 )
    return ants.list_to_ndimage( originalDWI, dwpimage )

img_LRdwp = concat_dewarp(
    dwp_OR['dewarpedmean'],
    img_LR_in,
    dwp_OR['deformable_registrations'][0]['fwdtransforms'],
    ddm['motion_parameters'] )
img_RLdwp = concat_dewarp(
    dwp_OR['dewarpedmean'],
    img_RL_in,
    dwp_OR['deformable_registrations'][1]['fwdtransforms'],
    eem['motion_parameters'] )
ants.image_write( img_LRdwp, '/tmp/temp1.nii.gz' )
ants.image_write( img_RLdwp, '/tmp/temp2.nii.gz' )
