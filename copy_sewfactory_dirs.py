import os
import shutil
from glob import glob

FABRIC_COUNT = len(glob(os.path.join(
    r"D:\VTO2025\DATASETs\Ours1\CLO_AUTO_GEN",
    "CLO_ASSETs",
    "FABRICs",
    "*.zfab"
)))

sewfactory_garment_path_list = sorted(glob(os.path.join(
    r"D:\VTO2025\DATASETs\Ours1\CLO_AUTO_GEN",
    "sewfactory",
    "*"
)))[:FABRIC_COUNT]

for idx, raw_path in enumerate(sewfactory_garment_path_list) :
    
    target_dir = os.path.join(
        r"D:\VTO2025\DATASETs\Ours1\CLO_AUTO_GEN",
        "SAMPLE_DATA", "SEWFACTORY"
    )
    
    # Create target directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)
    
    # Get the directory name to copy
    dir_name = os.path.basename(raw_path)
    target_path = os.path.join(target_dir, dir_name)
    
    # Use copytree for copying directories
    shutil.copytree(
        raw_path,
        target_path,
        dirs_exist_ok=True  # This will overwrite if directory already exists
    )
    
    print(f"Copied {raw_path} to {target_path}")
    
    break 