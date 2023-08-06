import sys, os
import unittest
os.environ["TF_NUM_INTEROP_THREADS"] = "8"
os.environ["TF_NUM_INTRAOP_THREADS"] = "8"
os.environ["ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS"] = "8"
import tempfile
import shutil
import tensorflow as tf
import antspymm
import antspyt1w
import antspynet
import ants



ex_path = os.path.expanduser( "~/.antspyt1w/" )
ex_path_mm = "/Users/stnava/data/HCP/DWI/140117/"
JHU_atlas = ants.image_read( ex_path + 'JHU-ICBM-FA-1mm.nii.gz') # Read in JHU atlas
JHU_labels = ants.image_read( ex_path + 'JHU-ICBM-labels-1mm.nii.gz') # Read in JHU labels
print("Load in HCP subject data for SR testing ...")
lrid = ex_path_mm + "140117_3T_DWI_dir95_LR"
rlid = ex_path_mm + "140117_3T_DWI_dir95_RL"
# Load in image L-R
img1 = ants.image_read( lrid + '.nii.gz') # LR dwi image
bval = lrid + '.bval' # bval
bvec = lrid + '.bvec'
img_RL_in = ants.image_read( rlid + '.nii.gz') # LR dwi image
img_RL_bval = rlid + '.bval' # bval
img_RL_bvec = rlid + '.bvec'
dd = antspymm.dipy_dti_recon( img1, bval, bvec, motion_correct='Rigid', verbose=True )
derka
## generate low res & its upsampling
# resample_image(image, resample_params, use_voxels=False, interp_type=1)
img1low = ants.resample_image( dd['motion_corrected'], [72,84,56,95], use_voxels=True, interp_type=0 )
img1up = ants.resample_image( img1low, img1.shape, use_voxels=True, interp_type=0 )
ddlin = antspymm.dipy_dti_recon( img1up, bval, bvec, mask=dd['dwi_mask'], motion_correct=False, verbose=True )
# img1nn = ants.resample_image( img1low, [128,128,80,33], use_voxels=True, interp_type=1 )
# ddnn = antspymm.dipy_dti_recon( img1nn, bval, bvec, mask=dd['dwi_mask'], motion_correct=False, verbose=True )
## do sr
mdlfn1 = '/Users/stnava/Downloads/ppmi_sr_example_pd_subject/siq_smallshort_train_2x2x2_1chan_featvggL6_best_mdl.h5'
mdlfn2 = '/Users/stnava/Downloads/ppmi_sr_example_pd_subject/siq_smallshort_train_2x2x2_1chan_featgraderL6_best_mdl.h5'
srmodel1 = tf.keras.models.load_model( mdlfn1, compile=False )
srmodel2 = tf.keras.models.load_model( mdlfn2, compile=False )
eps=1e-3
img1sr1=antspymm.super_res_mcimage(img1low, srmodel1, truncation=[eps, 1.0-eps],
    poly_order=2, target_range=[0, 1], isotropic=False, verbose=True)
img1sr2=antspymm.super_res_mcimage(img1low, srmodel2, truncation=[eps, 1.0-eps],
    poly_order=2, target_range=[0, 1], isotropic=False, verbose=True)
ddsr1 = antspymm.dipy_dti_recon( img1sr1, bval, bvec, mask=dd['dwi_mask'], motion_correct=False,  verbose=True )
ddsr2 = antspymm.dipy_dti_recon( img1sr2, bval, bvec, mask=dd['dwi_mask'], motion_correct=False,  verbose=True )
ants.image_write( dd['RGB'], '/tmp/temp.nii.gz' )
ants.image_write( ddlin['RGB'], '/tmp/templin.nii.gz' )
# ants.image_write( ddnn['RGB'], '/tmp/tempnn.nii.gz' )
ants.image_write( ddsr1['RGB'], '/tmp/tempsr1.nii.gz' )
ants.image_write( ddsr2['RGB'], '/tmp/tempsr2.nii.gz' )
antspynet.psnr( dd['FA'], ddlin['FA'] )
antspynet.psnr( dd['FA'], ddsr1['FA'] )
antspynet.psnr( dd['MD'], ddlin['MD'] )
antspynet.psnr( dd['MD'], ddsr1['MD'] )
wm='FA'
wm='MD'
anyzero=dd[wm]==0 or ddlin[wm]==0 or ddsr1[wm]==0 or ddsr2[wm]==0
dd[wm][anyzero]=0
ddlin[wm][anyzero]=0
ddsr1[wm][anyzero]=0
ddsr2[wm][anyzero]=0
wm='RGB'
antspynet.psnr( dd[wm], ddlin[wm] )
antspynet.psnr( dd[wm], ddsr1[wm] )
antspynet.psnr( dd[wm], ddsr2[wm] )
antspynet.ssim( dd[wm], ddlin[wm] )
antspynet.ssim( dd[wm], ddsr1[wm] )
antspynet.ssim( dd[wm], ddsr2[wm] )
derka
exit(0)
# img1 = ants.image_read( "processed/dwp0sr.nii.gz" )
# img2 = ants.image_read( "processed/dwp1sr.nii.gz" )
b0indices = antspymm.segment_timeseries_by_meanvalue( img1 )['highermeans']
b0indices2 = antspymm.segment_timeseries_by_meanvalue( img1 )['highermeans']
# FIXME: - test that these are the same values
# NOTE: could run SR at this point - will take a long time - example here:
# mdlfn = antspymm.get_data( "brainSR", target_extension=".h5")
# mdl = tf.keras.models.load_model( mdlfn )
# srimg = antspymm.super_res_mcimage( img, mdl, verbose=False )

dwp = antspymm.dewarp_imageset( [img1,img2], iterations=2, padding=6,
    target_idx = b0indices,
    syn_sampling = 20, syn_metric='mattes',
    type_of_transform = 'SyN',
    total_sigma = 0.0, random_seed=1,
    reg_iterations = [200,50,20] )

if islocal:
    print('dewarp done')
    ants.image_write( dwp['dewarped'][0], './dewarped0.nii.gz' )
    ants.image_write( dwp['dewarped'][1], './dewarped1.nii.gz' )

# FIXME: - add test
# testingClass.assertAlmostEqual(
#    float( dwp['dewarpedmean'].mean() ),
#    float( 108.2 ), 0, "template mean not close enough")

# now reconstruct DTI
bvec = antspymm.get_data( id1, target_extension=".bvec")
bval = antspymm.get_data( id1, target_extension=".bval")
dd = antspymm.dipy_dti_recon( dwp['dewarped'][0], bval, bvec, b0_idx=b0indices )
# ants.image_write( dd['RGB'], '/tmp/tempsr_rgb.nii.gz' )
bvec = antspymm.get_data( id2, target_extension=".bvec")
bval = antspymm.get_data( id2, target_extension=".bval")
ee = antspymm.dipy_dti_recon( dwp['dewarped'][1], bval, bvec, b0_idx=b0indices )
# ants.image_write( ee['RGB'], '/tmp/temp_rgb2.nii.gz' )
# FIXME: - add test

# sys.exit(os.EX_OK) # code 0, all ok
