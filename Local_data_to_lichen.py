import pandas as pd
from shapely.geometry import Polygon
import geopandas as gpd
import numpy as np
import os
from pathlib import Path
import paramiko

print('Starting processing...')

print('scanning for files')

# Walk through the directory and its subdirectories to find all files:
filepathlist = []
def os_walk(dir):
    for root, dirs, files in os.walk(dir):
        for file in files:
            filepathlist.append(os.path.join(root, file))   

# Upload file to lichen using SFTP:
def local_to_lichen_sat(sat_file, output_path):
    if not os.path.exists(sat_file):
        print(f"Satellite data file not found: {sat_file}")
        return
    
    # Establish SSH and SFTP connections
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='144.92.10.200', username='beronio', password='Griffin2026!')

    sftp = ssh.open_sftp()

    # Upload the file from local path to the server path
    filename = sat_file.split('/')[-1]
    updated_server_path = output_path + '/' + filename
    outputpath = Path(updated_server_path)

    if sftp.stat(updated_server_path).st_size > 0:
        print(f"Output file already exists and will be overwritten: {output_path}")
        print('Do you want to continue? (yes/no)')
        response = input().strip().lower()
        if response != 'yes':
            print('Processing cancelled.')
            return
        
    sftp.put(sat_file, updated_server_path)

    # Close connections safely
    sftp.close()
    ssh.close()
    print("File uploaded over SFTP successfully!")


if __name__ == "__main__":

    print('Please input the path to the data file (netCDF format):')
    satpath = input().strip()
    print('Please input the desired output path for the Lichen-compatible file (netCDF format):')
    output_path = input().strip()
    # print('Please input the path to the uncertainty data file (netCDF format):')
    # uncerpath = input().strip()

    print('Processing satellite data and converting to Lichen format...')

    local_to_lichen_sat(satpath, output_path)
    