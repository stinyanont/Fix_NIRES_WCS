# Fix NIRES Slit-Viewing Camera WCS

Keck/NIRES has a slit-viewing camera with a usable field of view. However, the WCS provided by the instrument software has two issues. First, the reference pixel CRPIX is set at an arbitrary pixel, not taking the actual pointing origin (PO) into account. Second, the CD matrix used to compute the RA/Dec of a given pixel does not take the PA of the observation into account. 

This script fixed these issue and provide a correct WCS header keywords by (1) reading the 'PONAME' keyword and setting 'CRPIX1' and 'CRPIX2' to the pixels corresponding to the PO used, and (2) rotate the CD matrix by 180-PA. The resulting WCS should provide correct coordinates up to some small offset due to Keck's pointing error. 

Currently, the XY pixel corresponding to the 'IMAG PO' and 'NIRES PO' are documented at (84.28, 450.16) and (482.4, 454.5), respectively. These numbers come from a rough measurement from the data. New numbers will be calculated based on the PO positions documented here: https://www2.keck.hawaii.edu/inst/nires/pointing_origins.html

## Usage

The script can be run on files in the directory by running `python Fix_NIRES_WCS.py filename_string`. It will glob the filename_string and run the script an all files. By default, it adds a suffix `_fixedWCS` in front of `.fits` in the output. A custom suffix can be provided as an option: `--suffix something_else`.

The script can also be imported, with the `fix_NIRES_WCS` function taking a NIRES WCS FITS header and returning a new header with corrected WCS keywords. 
