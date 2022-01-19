# WatChMaL DataTools
Tools for production and manipulation of data for WatChMaL 

cedar_script/ contains all the batch job submission scripts, to find out which
one to use, consult the README in that folder.

To generat the geometry npz file, it needs to be ran separately. It doesn't use
that much resources so can be performed on the login node. Do:
        python root_utils/full_geo_dump.py /path/to/relevant/root/file.root

After obtaining the one hdf5 file from all the data processing, you can
generate indices used for machine learning training with 
root_utils/Creat_indices_file.ipynb 