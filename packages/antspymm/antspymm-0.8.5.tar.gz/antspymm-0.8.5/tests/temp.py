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

print("THIS TEST USES DATA FROM DIFFERENT SUBJECTS'T1 and DWI - as such, not a great example of performance but demonstrates utility nonetheless")
ex_path = os.path.expanduser( "~/.antspyt1w/" )
ex_path_mm = os.path.expanduser( "~/.antspymm/" )
jhu_atlas = ants.image_read( ex_path + 'JHU-ICBM-FA-1mm.nii.gz') # Read in JHU atlas
jhu_labels = ants.image_read( ex_path + 'JHU-ICBM-labels-1mm.nii.gz') # Read in JHU labels

#### Load in data ####
print("Load in subject data ...")
t1id = ex_path_mm + "t1.nii.gz"
lrid = ex_path_mm + "I1499279_Anon_20210819142214_5"
ex_path = "/Users/stnava/data/PPMI/DTI/data/sub3101/"
t1id = ex_path + "PPMI-3101-20120817-T1w-S178931.nii.gz"
lrid = ex_path + "PPMI-3101-20120817-DTI_gated-I353354"
# Load in image L-R
dwi = ants.image_read( lrid + '.nii.gz') # LR dwi image
img_LR_bval = lrid + '.bval' # bval
img_LR_bvec = lrid + '.bvec'
t1w = ants.image_read( t1id )
t1w = t1w * ants.threshold_image( antspynet.brain_extraction( t1w, 't1') , 0.5, 1)
derka
dtibxt_data = antspymm.t1_based_dwi_brain_extraction( t1w, dwi, transform='Rigid' )
bval_LR = img_LR_bval
bvec_LR = img_LR_bvec
########################################
recon_LR_nomo = antspymm.dipy_dti_recon(
    dwi, bval_LR, bvec_LR,
    motion_correct=False,
    mask = dtibxt_data['b0_mask'],
    mask_dilation=0 )
########################################
recon_LR = antspymm.dipy_dti_recon(
    dwi, bval_LR, bvec_LR,
    motion_correct=True,
    mask = dtibxt_data['b0_mask'],
    mask_dilation=0 )
derka
OR_LRFA = recon_LR['FA']
ts_LR_avg = recon_LR['avgb0']



OR_LRFA = recon_LR['FA']
ts_LR_avg = recon_LR['avgb0']

derka

b0bxt = antspynet.brain_extraction( recon_LR['avgb0'], 'bold' )
b0bxt = ants.threshold_image( b0bxt, 0.5, 1.0 )
t1wrig = ants.registration( recon_LR['avgb0'] * b0bxt, t1w, 'Rigid' )['warpedmovout']

mymod='average_dwi'
zz=antspynet.brain_extraction( recon_LR[mymod], 'flair' ).threshold_image(0.5,1)
t1wrig = ants.registration( recon_LR[mymod] * zz, t1w, 'Rigid' )['warpedmovout']

# t1wrig = ants.registration( ts_LR_avg, t1w, 'Rigid' )['warpedmovout']
print("syn")
synreg = ants.registration(
            t1wrig,
            recon_LR['FA'] * zz,
            'SyNOnly',
            total_sigma=0.0,
            syn_metric='CC', syn_sampling=2, reg_iterations=[100,100,20],
            gradient_step=0.1 )
ants.image_mutual_information( t1wrig, synreg['warpedmovout'])
ants.image_write( synreg['warpedmovout'], '/tmp/tempw.nii.gz' )

dwp_OR ={
            'deformable_registrations':[synreg],
            'dewarpedmean':synreg['warpedmovout']
            }

# apply the dewarping tx to the original dwi and reconstruct again
def concat_dewarp(
            refimg,
            originalDWI,
            dwpTx,
            motion_parameters,
            motion_correct=True ):
        dwpimage = []
        for myidx in range(originalDWI.shape[3]):
            b0 = ants.slice_image( originalDWI, axis=3, idx=myidx)
            concatx = dwpTx.copy()
            if motion_correct:
                concatx.append( motion_parameters[myidx][0] )
            warpedb0 = ants.apply_transforms( refimg, b0, concatx )
            dwpimage.append( warpedb0 )
        return ants.list_to_ndimage( originalDWI, dwpimage )

img_LRdwp = concat_dewarp( t1wrig, img_LR,
            dwp_OR['deformable_registrations'][0]['fwdtransforms'],
            recon_LR['motion_parameters'],
            motion_correct=True
            )
recon_LR2 = antspymm.dipy_dti_recon( img_LRdwp, bval_LR, bvec_LR,
    motion_correct=False, mask_dilation=0  )
ants.image_mutual_information( t1wrig, recon_LR2['FA'])
ants.image_mutual_information( t1wrig, synreg['warpedmovout'])
ants.image_write( t1wrig, '/tmp/temp.nii.gz' )
ants.image_write( recon_LR2['FA'], '/tmp/tempfa.nii.gz' )

derka
# testing code
myidx=1
motion_parameters = recon_LR['motion_parameters']
b0 = ants.slice_image( img_LR, axis=3, idx=myidx)
concatx = synreg['fwdtransforms'].copy()
concatx.append( motion_parameters[myidx][0] )
warpedb0 = ants.apply_transforms( t1wrig, b0, concatx )
concatxb = synreg['fwdtransforms'].copy()
concatxb = motion_parameters[myidx] + concatxb
warpedb0b = ants.apply_transforms( t1wrig, b0, concatxb )

# img_LRdwp = ants.apply_transforms( t1w, img_LR, synreg['fwdtransforms'],
#   imagetype = 3 )
