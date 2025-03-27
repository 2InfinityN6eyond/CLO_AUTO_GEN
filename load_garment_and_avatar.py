import os, sys
import json
import time
from glob import glob
import random
import import_api
import utility_api
import fabric_api
import pattern_api
import export_api
import ApiTypes

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
    avatar_dir: str = "CLO_ASSETS/AVATARs"
    fabric_dir: str = "CLO_ASSETS/FABRICs"
    pose_dir: str = "CLO_ASSETS/POSEs"
    viewpoint_dir: str = "CLO_ASSETS/VIEWPOINTs"
    
    gcd_dir: str = "GarmentCodeData_v2"

    outfit_metadata_path: str = "outfit_path_list.json"
    combination_metadata_path: str = "top_bottom_path_list.json"
    
    sample_data_dir: str = r"sample_data\SAMPLE_DATA"
    
    outfit_path_list: list = None
    combination_path_list: list = None

    def __post_init__(self):
        self.avatar_path_list = sorted(glob(os.path.join(self.root_path, self.avatar_dir, "*.avt")))
        self.fabric_path_list = sorted(glob(os.path.join(self.root_path, self.fabric_dir, "*.zfab")))
        self.pose_path_list = sorted(glob(os.path.join(self.root_path, self.pose_dir, "*.pos")))
        self.viewpoint_path_list = sorted(glob(os.path.join(self.root_path, self.viewpoint_dir, "*.zcmr")))
        
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
        self.outfit_path_list = []
        for outfit in self.outfit_metadata:
            garment_split, _, garment_id = list(Path(outfit).parts)[-3:]
            
            self.outfit_path_list.append(os.path.join(
                self.sample_data_dir, garment_split, garment_id,
                f"{garment_id}__00__clo.json"
            ))

        with open(self.combination_metadata_path, "r") as f:
            self.combination_metadata_raw = json.load(f)
        self.combination_path_list = []
        for combination in self.combination_metadata_raw:
            top_base_path, bottom_base_path = combination.split(",")
            top_garment_split, _, top_garment_id = list(Path(top_base_path).parts)[-3:]
            bottom_garment_split, _, bottom_garment_id = list(Path(bottom_base_path).parts)[-3:]
            self.combination_path_list.append(os.path.join(
                self.sample_data_dir, top_garment_split,
                f"{top_garment_id}__00__{bottom_garment_id}__00",
                f"{top_garment_id}__00__{bottom_garment_id}__00__clo.json"
            ))
            
    @property
    def avatar_count(self) -> int:
        return len(self.avatar_path_list)

    @property
    def fabric_count(self) -> int:
        return len(self.fabric_path_list)
        
    @property
    def pose_count(self) -> int:
        return len(self.pose_path_list)
    
    @property
    def viewpoint_count(self) -> int:
        return len(self.viewpoint_path_list)

    @property
    def gcd_count(self) -> int:
        return len(self.gcd_path_list)
    


@dataclass
class GarmentScene :
    is_combination: bool = False
    garment_json_path: str = None
    avatar_path: str = None
    whole_fabric_path_list: str = None
    fabric_path_list: list = None
    panel_count_list: list = None
    pose_path:str = None
    viewpoint_path_list: list = None
    
    def __post_init__(self):
        # identify if scene is composed of single or multiple garments
        if len(os.path.basename(self.garment_json_path).split("__")) == 3:
            self.is_combination = False
        elif len(os.path.basename(self.garment_json_path).split("__")) == 5:
            self.is_combination = True
        else :
            raise ValueError(f"Invalid garment json path: {self.garment_json_path}")
        
        self.panel_count_list, self.prev_fabric_count = self.get_panel_fabric_count_list()
        self.fabric_path_list = list(map(
            lambda x : random.choice(self.whole_fabric_path_list),
            self.panel_count_list
        ))
        
        print("="*50)
        print(self.panel_count_list)
        print(self.prev_fabric_count)
        print(self.fabric_path_list)
        print("="*50)
        
        self.output_dir = os.path.dirname(self.garment_json_path)
        
    def get_panel_fabric_count_list(self) :
        with open(self.garment_json_path, "r") as f:
            json_data = json.load(f)
            
        panel_count_list = []
        cur_garment_id = None
        for pattern in json_data["PatternList"] :
            garment_id = pattern["ID"].split("_")[1]
            
            if garment_id == cur_garment_id :
                panel_count_list[-1] += 1
            else :
                cur_garment_id = garment_id
                panel_count_list.append(1)
            
        return panel_count_list, len(json_data["FabricList"])
             
    def import_scene(
        self, option = None,
        SIM_STEP = 200
    ) :
        '''
        import to clo
        '''
        if option is None :
            option = ApiTypes.ImportExportOption()
            option.bExportGarment = True
            option.bExportAvatar = False
            option.bSingleObject = True
            option.bThin = False
            option.bSaveInZip = False
            option.bMetaData = True
        
        utility_api.NewProject()
        
        import_api.ImportFile(self.avatar_path)
        pattern_api.ImportPatternJSON(self.garment_json_path)
        for fabric_path in self.fabric_path_list :
            fabric_api.AddFabric(fabric_path)
        
        fabric_idx = fabric_api.GetFabricCount(-2) - len(self.fabric_path_list)
        colorway_idx = fabric_idx
        panel_idx = 0
        for fabric_path, panel_count in zip(self.fabric_path_list, self.panel_count_list) :
            for _ in range(panel_count) :
                
                fabric_api.AssignFabricToPattern(fabric_idx, panel_idx, colorway_idx)
                pattern_api.SetArrangementShapeStyle(panel_idx, "Flat")
                panel_idx += 1
            fabric_idx += 1
    
        export_api.ExportZPac(      os.path.join(self.output_dir, "pre_drape.zpac"))
        export_api.ExportSnapshot3D(os.path.join(self.output_dir, "pre_drape.png"))
        # export_api.ExportOBJ(       os.path.join(self.output_dir, "pre_drape.obj"))
        import_api.ImportFile(      os.path.join(self.output_dir, "pre_drape.zpac"))
        
        
        utility_api.Simulate(SIM_STEP)
        
        import_api.ImportPose(self.pose_path)
        pose_name = os.path.basename(self.pose_path).split(".")[0]
        export_api.ExportOBJ(os.path.join(self.output_dir, f"{pose_name}.obj"), option)
        
        for viewpoint in self.viewpoint_path_list :
            view_name = os.path.basename(viewpoint).split(".")[0]
            import_api.ImportFile(viewpoint)
            export_api.ExportRenderingImage(os.path.join(self.output_dir, f"{view_name}.png"))
        
        
        
        
        
    

    
SYSTEM_CONFIG_DICT = {
    "HJP_WINDOWS_DESKTOP": {
        "CLO_DIR": "E:/HJP/KUAICV/VTO/DATA/CLO",
    }
}

system_name = "HJP_WINDOWS_DESKTOP"

path_config = PathConfig(root_path=SYSTEM_CONFIG_DICT[system_name]["CLO_DIR"])

# final_garment_path_list = sorted(
#     path_config.outfit_path_list + path_config.combination_path_list
# )

# GARMENT_IDX = 9
# garment_config_json_path = final_garment_path_list[GARMENT_IDX]


for garment_config_json_path in sorted(
    path_config.combination_path_list
) :

    garment_scene = GarmentScene(
        garment_json_path=garment_config_json_path,
        avatar_path=path_config.avatar_path_list[0],
        whole_fabric_path_list=path_config.fabric_path_list,
        pose_path=path_config.pose_path_list[0],
        viewpoint_path_list=path_config.viewpoint_path_list
    )

    garment_scene.import_scene()