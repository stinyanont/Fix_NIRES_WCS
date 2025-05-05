import os, glob, copy, argparse

import numpy as np

from astropy.io import fits
from astropy.wcs import WCS

#We will divide by zero. Shoot me.
np.seterr(divide='ignore')

def fix_NIRES_WCS(header):
    """
    Fix NIRES SVC WCS header. The WCS header provided with NIRES SVC data
    does NOT take the PA into account and has a wrong reference pixel.
    
    We fix this by rotating the CD matrix by 180 - PA degrees.

    We also found that the CRPIX provided does not change with the pointing origin.
    We fix this by seting CRPIX corresponding to the selected pointing origin.
    
    TO DO: find a way to translate the PO provided to the pixel coordinates
    Right now, just use the measured position in our data

    Input: original header
    Output: FITS header with the CD matrix fixed
    """
    PA = header['ROTDEST'] #PA of vertical axis of the image
    #load up the original CD
    original_CD = np.array([[header['CD1_1'], header['CD1_2']],
                            [header['CD2_1'], header['CD2_2']]])
    theta = np.radians(180 - PA)
    rotation_matrix = np.array( [[np.cos(theta), -np.sin(theta)],\
                                 [np.sin(theta),  np.cos(theta)]])
    #rotate the CD matrix
    new_CD = np.matmul(rotation_matrix, original_CD)

    header['CD1_1'] = new_CD[0,0]
    header['CD1_2'] = new_CD[0,1]
    header['CD2_1'] = new_CD[1,0]
    header['CD2_2'] = new_CD[1,1]

    #Also reset CRPIX
    ####Right now just use measured value from data. 
    ####Figure out how to get this from the pointing origin specified in mm
    print(header['PONAME'])
    if 'IMAG' in header['PONAME']:
        print('IMAG PO')
        header['CRPIX1'] = 482.4
        header['CRPIX2'] = 454.5
    elif 'NIRES' in header['PONAME']:
        print("NIRES PO")
        header['CRPIX1'] = 84.28
        header['CRPIX2'] = 450.16

    return header

def fixWCS(path, subfix = 'fixedWCS'):
    """
    Fix WCS of all NIRES SVC image files in the path
    The code does not check for you if these are NIRES
    SVC files, so only run on NIRES data, otherwise everything 
    gets "fixed"
    """
    files = glob.glob(path+'/v*.fits*')
    for file in files:
        out_name = file.split('.fits')[0]+'.%s.fits'%subfix
    #     print(out_name)
        hdu = fits.open(file)
        new_header = fix_NIRES_WCS(hdu[0].header)
        hdu[0].header = new_header 
        # hdul = fits.HDUList([hdu])
        hdu.writeto(out_name, overwrite=True)

def fixWCSfile(file, subfix = 'fixedWCS'):
	"""
	Same as the above, but for specified files. 
	"""
    out_name = file.split('.fits')[0]+'.%s.fits'%subfix
#     print(out_name)
    hdu = fits.open(file)
    new_header = fix_NIRES_WCS(hdu[0].header)
    hdu[0].header = new_header 
    # hdul = fits.HDUList([hdu])
    hdu.writeto(out_name, overwrite=True) 

if __name__ == '__main__': 
    #Arguments parser
    parser = argparse.ArgumentParser(
                        prog='Fix_NIRES_WCS',
                        description='Fix NIRES Slit Viewing Camera WCS.',
                        epilog='python Fix_NIRES_WCS.py filenames')
    parser.add_argument('filenames')
    parser.add_argument('--suffix', default = 'fixedWCS')

    args = parser.parse_args()

    files = glob.glob(args.filenames)
    for file in files:
        fixWCSfile(file, subfix = args.subfix)