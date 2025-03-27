import os, sys
import json
import time
from glob import glob
import random

from pathlib import Path
from dataclasses import dataclass

def get_sort_key(path_str):
    path = Path(path_str)
    # Find the 'garments_5000_X' part
    garment_dir = next(part for part in path.parts if part.startswith('garments_5000_'))
    # Extract the number after 'garments_5000_'
    garment_num = int(garment_dir.split('_')[-1])
    # Get the random ID from the path
    random_id = path.parent.name
    return (garment_num, random_id)

@dataclass
class PathConfig :
    root_path : str = None
    avatar_dir: str = "AVATARs"
    gcd_dir: str = "GarmentCodeData_v2"

    outfit_metadata_path: str = "outfit_path_list.json"
    combination_metadata_path: str = "top_bottom_path_list.json"
    
    sample_data_dir: str = r"sample_data\SAMPLE_DATA"
    
    outfit_path_list: list = None
    combination_path_list: list = None

    def __post_init__(self):
        self.avatar_path_list = sorted(glob(os.path.join(
            self.root_path, self.avatar_dir, "*.avt"
        )))
        self.gcd_path_list = sorted(
            glob(os.path.join(
                self.root_path, self.gcd_dir,
                "*", "*", "*config.json"
            )),
            key=get_sort_key
        )
        
        self.sample_data_dir = os.path.join(self.root_path, self.sample_data_dir)
        
        self.outfit_metadata_path = os.path.join(self.root_path, self.outfit_metadata_path)
        self.combination_metadata_path = os.path.join(self.root_path, self.combination_metadata_path)

        with open(self.outfit_metadata_path, "r") as f:
            self.outfit_metadata = json.load(f)
        self.outit_path_list = []
        for outfit in self.outfit_metadata:
            garment_split, _, garment_id = list(Path(outfit).parts)[-3:]
            self.outit_path_list.append(os.path.join(
                self.sample_data_dir, f"{garment_split}__{garment_id}__clo.json"
            ))
        

        with open(self.combination_metadata_path, "r") as f:
            self.combination_metadata_raw = json.load(f)
        self.combination_path_list = []
        for combination in self.combination_metadata_raw:
            top_base_path, bottom_base_path = combination.split(",")
            top_garment_split, _, top_garment_id = list(Path(top_base_path).parts)[-3:]
            bottom_garment_split, _, bottom_garment_id = list(Path(bottom_base_path).parts)[-3:]
            combined_path = os.path.join(
                self.sample_data_dir,
                f"{top_garment_split}__{top_garment_id}__{bottom_garment_id}__clo.json"
            )
                    
            self.combination_path_list.append(combined_path)

    @property
    def avatar_count(self) -> int:
        return len(self.avatar_path_list)

    @property
    def gcd_count(self) -> int:
        return len(self.gcd_path_list)
    
    
SYSTEM_CONFIG_DICT = {
    "HJP_WINDOWS_DESKTOP": {
        "CLO_DIR": "E:/HJP/KUAICV/VTO/DATA/CLO",
    }
}

system_name = "HJP_WINDOWS_DESKTOP"

path_config = PathConfig(root_path=SYSTEM_CONFIG_DICT[system_name]["CLO_DIR"])

print(path_config.avatar_path_list)
print(path_config.gcd_path_list)

avtfile_path = path_config.avatar_path_list[0]
avtfile_path = r"E:\HJP\KUAICV\VTO\DATA\CLO\AVATARs\173_55_miya_v1.avt"
avtfile_path = r"E:\HJP\KUAICV\VTO\DATA\CLO\AVATARs\173_60_bust_900.avt"


garment_config_json_path = path_config.gcd_path_list[0]
garment_config_json_path = r"E:\HJP\KUAICV\VTO\DATA\CLO\GarmentCodeData_v2\garments_5000_0\rand_HXRQ5GP3VV\rand_HXRQ5GP3VV_config_2.json"
garment_config_json_path = r"E:\HJP\KUAICV\VTO\DATA\CLO\OTHERs\MANUAL_SAMPLES\garments_5000_0__rand_SVUCY3YLRE__rand_ZTJFE9H3WI__clo.json"
garment_config_json_path = r"E:\HJP\KUAICV\VTO\DATA\CLO\sample_data\SAMPLE_DATA\garments_5000_27__rand_L6HTX1KO28__clo.json"


GARMENT_IDX = 50
garment_config_json_path = path_config.combination_path_list[GARMENT_IDX]

print(garment_config_json_path)