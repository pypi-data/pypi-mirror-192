import ants
import antspynet
import antspymm
import glob

def wmh_sim( x,  max_rot=10, nzsd=1 ):
    rRotGenerator = ants.contrib.RandomRotate3D( ( max_rot*(-1.0), max_rot ), reference=x )
    tx = rRotGenerator.transform()
    itx = ants.invert_ants_transform(tx)
    y = ants.apply_ants_transform_to_image( tx, x, x, interpolation='linear')
    y = ants.add_noise_to_image( y,'additivegaussian', [0,nzsd] )
    wmh=antspynet.sysu_media_wmh_segmentation(y)
    return ants.apply_ants_transform_to_image( itx, wmh, wmh, interpolation='linear')

ifns = glob.glob( "*FLAIR.nii" )
print( ifns )
refflair = ants.image_read( ifns[0] )
wmhprob = refflair * 0
for ifn in ifns:
    for sim in range( 10 ) :
        print( ifn + " " + str( sim ) )
        img = ants.image_read( ifn )
        simwmh = wmh_sim( img, nzsd=2 )
        wmhprob = wmhprob + simwmh
        wmhprobu = ants.iMath(wmhprob,"Normalize")
        ants.image_write( wmhprobu, 'flair_wmh_prior.nii.gz' )

ants.plot( refflair, wmhprobu, nslices=21, ncol=7, axis=2 )
