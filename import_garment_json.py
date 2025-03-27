import os
import json
import import_api
import utility_api
import fabric_api
import pattern_api
import export_api
import ApiTypes
import time
import os
import glob
import random

from dataclasses import dataclass

ieo_option = ApiTypes.ImportExportOption()
ieo_option.bExportGarment = True
ieo_option.bExportAvatar = False
ieo_option.bSingleObject = False # single or Multiple
#ieo_option.weldType = WELD_TYPE
ieo_option.bThin = False
ieo_option.bSaveInZip = False


@dataclass
class PathInfo:
    avtfile: str = "174_65_miya_noac.avt"
    custom_point: str = None
    pose_path: str = None
    DATA_DIR: str = None
    FABRIC: str = None
    Garment_info: str = "CLO_FORMAT_SAMPLE.json"

path_dict = {
    "HJP_WINDOWS_DESKTOP": {
        "avtfile_path": “/Users/seph/Documents/clo/Assets/Avatar/Avatar/Male_V2/2025_0205_1806jinho.avt”,
        "custom_point_path": “/Users/seph/Desktop/고려대_인턴_연구실/View_Point",
        "pose_path": “/Users/seph/Desktop/고려대_인턴_연구실/Pose",
        "DATA_DIR": “/Users/seph/Desktop/고려대_인턴_연구실/NO_ARC_CLO_JSON",
        "FABRIC_PATH": “/Users/seph/Desktop/고려대_인턴_연구실/Fabric",
        "Garment_info_path": “/Users/seph/Desktop/고려대_인턴_연구실/garment_code_data_meta_df.json"
    },
    "JOSEF_WINDOWS_DESKTOP": {
        "avtfile_path": “/Users/seph/Documents/clo/Assets/Avatar/Avatar/Male_V2/2025_0205_1806jinho.avt”,
        "custom_point_path": “/Users/seph/Desktop/고려대_인턴_연구실/View_Point",
        "pose_path": “/Users/seph/Desktop/고려대_인턴_연구실/Pose",
        "DATA_DIR": “/Users/seph/Desktop/고려대_인턴_연구실/NO_ARC_CLO_JSON",
        "FABRIC_PATH": “/Users/seph/Desktop/고려대_인턴_연구실/Fabric",
        "Garment_info_path": “/Users/seph/Desktop/고려대_인턴_연구실/garment_code_data_meta_df.json"
    }
}


PC_IDENTIFIER = "HJP_WINDOWS_DESKTOP"


# 아바타 load
#avtfile_path = “/Users/seph/Documents/clo/Assets/Avatar/Avatar/Male_V2/2025_0205_1806jinho.avt”
#avtfile_path = “/Users/seph/Documents/clo/Assets/Avatar/Avatar/Female_V2/Mia_avt_revise.avt”
avtfile_path = “/Users/seph/Downloads/174_65_noac_miya_20250302_1947.avt”
custom_point_path = “/Users/seph/Desktop/고려대_인턴_연구실/View_Point”
pose_path = “/Users/seph/Desktop/고려대_인턴_연구실/Pose”
DATA_DIR = “/Users/seph/Desktop/고려대_인턴_연구실/NO_ARC_CLO_JSON”
FABRIC_PATH = “/Users/seph/Desktop/고려대_인턴_연구실/Fabric”
Garment_info_path = “/Users/seph/Desktop/고려대_인턴_연구실/garment_code_data_meta_df.json”


export_json_1 = “/Users/seph/Downloads/bad_garment/rand_598QGS7XYH_rand_598QGS7XYH/Clo_Garment_rand_598QGS7XYH_rand_598QGS7XYH.json”
export_json_2 = “/Users/seph/Downloads/bad_garment/rand_AG6HLSKJCH_rand_AG6HLSKJCH/Clo_Garment_rand_AG6HLSKJCH_rand_AG6HLSKJCH.json”
export_json_3 = “/Users/seph/Downloads/bad_garment/rand_HNQQDUZLR3_rand_HNQQDUZLR3/Clo_Garment_rand_HNQQDUZLR3_rand_HNQQDUZLR3.json”
export_json_4 = “/Users/seph/Downloads/rand_QTXYOGGN3U_rand_QTXYOGGN3U/Clo_Garment_rand_QTXYOGGN3U_rand_QTXYOGGN3U.json”
export_json_5 =“‘/Users/seph/Downloads/top_bottom_info 복사본/rand_AYGDGFWAFZ_rand_GXU0CG660C/Clo_Garment_rand_AYGDGFWAFZ_rand_GXU0CG660C.json’”
#pattern_api.ExportPatternJSON(export_json_5)
# good ex simulate
pattern_api.ImportPatternJSON(export_json_5)
#zpac_path = “/Users/seph/Downloads/prac111.zpac”
#import_api.ImportFile(zpac_path)
import json
#a = utility_api.GetCustomViewInformation()
#save_camera_position = “/Users/seph/Downloads/part_panel/d/camera_positions.json”
#with open(save_camera_position, “w”) as f:
#    f.write(a)
for i in range(0, 28, 1):
    pattern_api.SetArrangementShapeStyle(i, “Flat”)
