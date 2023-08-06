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
testingClass = unittest.TestCase( )
islocal = False
dtiid = "/Users/stnava/Downloads/PPMI500/source/data/PPMI/103467/20210929/DTI_LR/I1519041/PPMI-103467-20210929-DTI_LR-I1519041"
img1 = ants.image_read( dtiid + ".nii.gz" )
dd = antspymm.dipy_dti_recon( img1, dtiid+".bval", dtiid+".bvec",
    motion_correct='SyN', verbose=True )
