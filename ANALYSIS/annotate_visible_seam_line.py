# CLO Viewpoints

import numpy as np
from dataclasses import dataclass

@dataclass
class CloCamera :
    name: str = None
    cam2world: np.ndarray = None
    fov: float = None
    width: int = None
    height: int = None
    
camera_info = {
    "Custom_View_0": CloCamera(
        name = "Custom_View_1",
        cam2world = np.array([
            [1, 0, 0, -9.2e-05],
            [0, 1, 0, -896.122],
            [0, 0, 1, -7998.56],
            [0, 0, 0, 1]
        ]),
        fov = 15,
        width = 480,
        height = 640
    ),  
    "Custom_View_1": CloCamera(
        name = "Custom_View_1",
        cam2world = np.array([
            [1, 0, 0, -9.2e-05],
            [0, 1, 0, -896.122],
            [0, 0, 1, -7998.56],
            [0, 0, 0, 1]
        ]),
        fov = 15,
        width = 480,
        height = 640
    ),  
    "Custom_View_2": CloCamera(
        name = "Custom_View_2",
        cam2world = np.array([
            [0.707107, 0, 0.707107, 1.01581],
            [0, 1, 0, -896.122],
            [-0.707107, 0, 0.707107, -7998.98],
            [0, 0, 0, 1]
        ]),
        fov = 15,
        width = 480,
        height = 640
    ),
    "Custom_View_3": CloCamera(
        name = "Custom_View_3",
        cam2world = np.array([
            [0.707107, 0, -0.707107, -1.01581],
            [0, 1, 0, -896.122],
            [0.707107, 0, 0.707107, -7998.98],
            [0, 0, 0, 1]
        ]),
        fov = 15,
        width = 480,
        height = 640
    ),
    "Custom_View_4": CloCamera(
        name = "Custom_View_4",
        cam2world = np.array([
            [0, 0, 1, 1.44049],
            [0, 1, 0, -896.122],
            [-1, 0, 0, -8000],
            [0, 0, 0, 1]
        ]),
        fov = 15,
        width = 480,
        height = 640
    ),
    "Custom_View_5": CloCamera(
        name = "Custom_View_5",
        cam2world = np.array([
            [0, 0, -1, -1.44093],
            [0, 1, 0, -896.122],
            [1, 0, 0, -8000],
            [0, 0, 0, 1]
        ]),
        fov = 15,
        width = 480,
        height = 640
    ),
    "Custom_View_6": CloCamera(
        name = "Custom_View_6",
        cam2world = np.array([
            [-1, 0, 0, -0.000608],
            [0, 1, 0, -896.122],
            [0, 0, -1, -8001.44],
            [0, 0, 0, 1]
        ]),
        fov = 15,
        width = 480,
        height = 640
    ),
    "Custom_View_7": CloCamera(
        name = "Custom_View_7",
        cam2world = np.array([
            [-0.677822, 0, -0.735226, -1.0604],
            [-0.051424, 0.997551, 0.047409, -893.857],
            [0.733425, 0.069943, -0.676162, -8063.65],
            [0, 0, 0, 1]
        ]),
        fov = 15,
        width = 480,
        height = 640
    ),
    "Custom_View_8": CloCamera(
        name = "Custom_View_8",
        cam2world = np.array([
            [-0.773786, 0, 0.633447, 0.911345],
            [0.035455, 0.998432, 0.043309, -894.654],
            [-0.632454, 0.055971, -0.772573, -8051.27],
            [0, 0, 0, 1]
        ]),
        fov = 15,
        width = 480,
        height = 640
    ),
    "Custom_View_9": CloCamera(
        name = "Custom_View_9",
        cam2world = np.array([
            [0.847255, 0, 0.531186, 0.765239],
            [0.223366, 0.907291, -0.356274, -813.553],
            [-0.48194, 0.420503, 0.768707, -8375.71],
            [0, 0, 0, 1]
        ]),
        fov = 15,
        width = 480,
        height = 640
    ),
    "Custom_View_10": CloCamera(
        name = "Custom_View_10",
        cam2world = np.array([
            [0.716937, 0, -0.697138, -1.0054],
            [-0.275326, 0.918708, -0.283145, -823.685],
            [0.640466, 0.394938, 0.658656, -8352.96],
            [0, 0, 0, 1]
        ]),
        fov = 15,
        width = 480,
        height = 640
    )   
}
for camera in camera_info.values() :
    camera.cam2world = np.linalg.inv(camera.cam2world)
    
    
    
    
    
import os, sys
import json
import cv2
from glob import glob
from pathlib import Path
import trimesh
import xml.etree.ElementTree as ET

from analysis_utils import visualize_meshes_plotly

@dataclass
class SeamDressScene :
    garment_dir: str = None
    garment_version: str = None
    
    spec_path_list: list = None
    stitch_dict_list: list = None
    
    # pose_list: list = None
    view_name_list: list = None
    
    mesh_path_list: list = None
    meta_path_list: list = None
    mesh_list: list = None
    
    rendered_path_list: list = None

    def __post_init__(self, garment_version = "01"):
        self.garment_id_list = str(Path(self.garment_dir).name).split("__")[::2]
        # self.spec_path_list = list(map(
        #     lambda gid : str(Path(self.garment_dir) / f"{gid}__{garment_version}__specification.json"),
        #     self.garment_id_list,
        # ))
        
        self.spec_path_list = []
        for garment_id in self.garment_id_list :
            spec_path = str(Path(self.garment_dir) / f"{garment_id}__{garment_version}__specification.json")
            if os.path.exists(spec_path) :
                self.spec_path_list.append(spec_path)
            else :
                spec_path = str(Path(self.garment_dir) / f"{garment_id}_specification.json")
                self.spec_path_list.append(spec_path)
        
        self.stitch_dict_list = []
        for spec_path in self.spec_path_list:
            with open(spec_path, "r") as f:
                spec = json.load(f)
            stitch_dict = {}
            for idx, stitch in enumerate(spec["pattern"]["stitches"]):
                stitch_dict[idx] = stitch
            self.stitch_dict_list.append(stitch_dict)
            
        self.stitch_dict_dict = {}
        for garment_id, spec_path in zip(self.garment_id_list, self.spec_path_list) :
            with open(spec_path, "r") as f :
                spec = json.load(f)
            stitch_dict = {}
            for idx, stitch in enumerate(spec["pattern"]["stitches"]) :
                stitch_dict[idx] = stitch
            self.stitch_dict_dict[garment_id] = stitch_dict
        
        self.garment_count = len(self.spec_path_list)
        # self.rendered_path_list = list(filter(
        #     lambda x : "__" in Path(x).stem,
        #     glob(str(Path(self.garment_dir) / "Custom*.png"))
        # ))
        self.rendered_path_list = sorted(glob(os.path.join(
            self.garment_dir, "Custom*.png"
        )))
        self.view_name_list = list(map(
            lambda x: Path(x).stem[:-2],
            self.rendered_path_list
        ))
        self.rendered_img_dict = dict(zip(
            self.view_name_list,
            list(map(
                lambda x : cv2.imread(x),
                self.rendered_path_list
            ))
        ))
        
        self.mesh_path_list = sorted(glob(str(Path(self.garment_dir)/"*.obj")))
        # self.pose_list = list(map(lambda x: Path(x).stem, self.mesh_path_list))
        self.meta_path_list = list(map(
            lambda x : str(Path(self.garment_dir) / f"{x}_meta_data.xml"),
            self.view_name_list
        ))
        
        assert list(map(
            lambda x : Path(x).stem[:-2], self.rendered_path_list
        )) == list(map(
            lambda x : Path(x).stem, self.mesh_path_list
        )) and list(map(
            lambda x : Path(x).stem, self.mesh_path_list
        )) == list(map(
            lambda x : Path(x).stem[:-10], self.meta_path_list
        ))
        
    def read_mesh(self):
        
        self.body_mesh_dict = {}
        self.garment_mesh_dict_dict = {}
        for mesh_path in self.mesh_path_list :
            view_name = str(Path(mesh_path).stem)
                            
            mesh_scene = trimesh.load(mesh_path)
            mesh_list = []
            for geometry in mesh_scene.geometry.values() :
                if isinstance(geometry, trimesh.Trimesh):
                    mesh_list.append(geometry)
            self.body_mesh_dict[view_name] = trimesh.util.concatenate(mesh_list[:-self.garment_count])
            self.garment_mesh_dict_dict[view_name] = dict(zip(
                self.garment_id_list,
                # mesh_list[-1:-self.garment_count-1:-1]
                mesh_list[-self.garment_count:]
            ))
        
        # self.read_stitch_vert()
        
    def read_stitch_vert(self, same_vert_thresh=1e-1) :
        """
        Set below member variables.
        - self.stitch_vert_mask_dict_list
            - list for each garment, dict containing stitch vertex mask for each stitch
        - self.stitch_vert_idx_arr_list
        - self.stitch_vert_idx_arr_dict_list
        """
        
        self.stch_vert_idx_arr_list_dict_dict = {}
        self.stch_vert_mask_list_dict_dict = {}
        self.seam_line_vert_idx_arr_list_dict_dict = {}
        
        for view_name, meta_path in zip(self.view_name_list, self.meta_path_list) :
            assert view_name == Path(meta_path).stem[:-10], f"inconsistent view name and meta path"
        
            # CLO saved metatdata does not distinguish stitches between garments
            raw_stitch_vert_idx_list_list = []
            
            tree = ET.parse(meta_path)
            root = tree.getroot()
            seam_line_pair_list = root.find("SeamLinePairList")
            for pair in seam_line_pair_list.findall("SeamLinePair") :
                seam_lines = pair.findall("SeamLine")
                if len(seam_lines) >= 2 :
                    first_indexes_str = seam_lines[0].get("MeshPointIndexes")
                    second_indexes_str = seam_lines[1].get("MeshPointIndexes")
                    first_list = list(map(lambda x: int(x)-1, first_indexes_str.split("/")))
                    second_list = list(map(lambda x: int(x)-1, second_indexes_str.split("/")))
                    raw_stitch_vert_idx_list_list.append(first_list + second_list)
                else :
                    print("SeamLinePair has less than 2 SeamLine")
            
            stch_vert_idx_arr_list_dict = {}
            if len(self.garment_id_list) == 1 : # single garment
                garment_id = self.garment_id_list[0]
                stch_vert_idx_arr_list_dict[garment_id] = []
                for idx in self.stitch_dict_dict[garment_id].keys() :
                    stch_vert_idx_arr_list_dict[garment_id].append(
                        np.array(raw_stitch_vert_idx_list_list[idx])
                    )
            elif len(self.garment_id_list) == 2 : # combination of two garments
                bottom_id = self.garment_id_list[1]
                top_id = self.garment_id_list[0]
                
                stch_vert_idx_arr_list_dict[bottom_id] = []
                stch_vert_idx_arr_list_dict[top_id] = []
                
                for idx in self.stitch_dict_dict[bottom_id].keys() :
                    stch_vert_idx_arr_list_dict[bottom_id].append(
                        np.array(raw_stitch_vert_idx_list_list[idx])
                    )
                
                idx_accum = idx + 1
                vert_offset = len(self.garment_mesh_dict_dict[view_name][bottom_id].vertices)
                
                for idx in self.stitch_dict_dict[top_id].keys() :
                    stch_vert_idx_arr_list_dict[top_id].append(
                        np.array(raw_stitch_vert_idx_list_list[idx + idx_accum]) - vert_offset
                    )
            
            stch_vert_mask_list_dict = {}
            for garment_id, stch_vert_idx_arr_list in stch_vert_idx_arr_list_dict.items() :
                garment_mesh = self.garment_mesh_dict_dict[view_name][garment_id]
                vert_count = garment_mesh.vertices.shape[0]
                
                stch_vert_mask_list_dict[garment_id] = []
                for (stch_idx, stch_vert_idx_arr) in enumerate(stch_vert_idx_arr_list) :
                    mask = np.zeros(vert_count, dtype=bool)
                    mask[stch_vert_idx_arr] = True
                    stch_vert_mask_list_dict[garment_id].append(mask)
                
            # dict per garment, dict per stitch, array of seam line vertex idx, ordered so that it follows seam line linearly
            # vertex idx is already sorted linearly. just need to remove overlapping vertices
            # In the case of stitch between two garments, every seam vertex is duplicated,
            seam_line_vert_idx_arr_list_dict = {}
            for garment_id, stch_vert_idx_arr_list in stch_vert_idx_arr_list_dict.items() :
                seam_line_vert_idx_arr_list_dict[garment_id] = []
                
                garment_mesh = self.garment_mesh_dict_dict[view_name][garment_id]
                vert_count = garment_mesh.vertices.shape[0]
                
                for stch_idx, stch_vert_idx_arr in enumerate(stch_vert_idx_arr_list) :
                    seam_line_vert_idx_list = [stch_vert_idx_arr[0]]
                    for vert_idx in stch_vert_idx_arr[1:] :
                        
                        dist_arr = garment_mesh.vertices[seam_line_vert_idx_list] - garment_mesh.vertices[[vert_idx]]
                        dist_arr = np.linalg.norm(dist_arr, axis=1)
                        if np.min(dist_arr) < same_vert_thresh :
                            continue
                        seam_line_vert_idx_list.append(vert_idx)
                        # for i in seam_line_vert_idx_list :
                        #     if (garment_mesh.vertices[vert_idx] == garment_mesh.vertices[i]).all() :
                        #         break
                        # else :
                        #     seam_line_vert_idx_list.append(vert_idx)

                    seam_line_vert_idx_arr_list_dict[garment_id].append(np.array(seam_line_vert_idx_list))

            self.stch_vert_idx_arr_list_dict_dict[view_name] = stch_vert_idx_arr_list_dict
            self.stch_vert_mask_list_dict_dict[view_name] = stch_vert_mask_list_dict
            self.seam_line_vert_idx_arr_list_dict_dict[view_name] = seam_line_vert_idx_arr_list_dict
            
            
            


import pickle
import pyrender
import matplotlib.pyplot as plt
from tqdm import tqdm
# ================================
            
garment_dir_list = sorted(glob(os.path.join(
    "..", "SAMPLE_DATA", "GCD__GOOD", "*"
))) + sorted(glob(os.path.join(
    "..", "SAMPLE_DATA", "SEWFACTORY__GOOD", "*"
)))


MIN_CONSEC_VERT_TO_BE_SEGMENT = 3
MIN_CONSEC_VERT_TO_DISCONNECT = 2


for garment_dir in tqdm(garment_dir_list) :    
    
    try :
        scene = SeamDressScene(Path(garment_dir))
        
        assert len(scene.view_name_list) > 9, f"garment dir {garment_dir} has less than 10 views"
        
        already_processed = True
        for view_name in scene.view_name_list :
            if not os.path.exists(
                str(Path(garment_dir) / f"{view_name}.pkl")
            ) :
                already_processed = False
                break
        if already_processed :
            print(f"already processed {garment_dir}")
            continue
        
        scene.read_mesh()
        scene.read_stitch_vert(same_vert_thresh=1e-1)


    except Exception as e :
        print(e)
        continue
    

    # for rendered_img_path in scene.rendered_path_list :
    for view_name, rendered_img_path in zip(scene.view_name_list, scene.rendered_path_list) :        
        assert view_name == Path(rendered_img_path).stem[:-2], f"{view_name} != {Path(rendered_img_path).stem[:-2]}"
        
        cam_name, pose_name = view_name.split("__")
        cam_info = camera_info[cam_name]

        body_mesh = scene.body_mesh_dict[view_name]
        garment_mesh_dict = scene.garment_mesh_dict_dict[view_name]
        garment_mesh_list = list(garment_mesh_dict.values())
            
        material = pyrender.MetallicRoughnessMaterial(
            baseColorFactor=(0.0, 0.0, 0.0, 1.0),  # RGB color, Alpha
            metallicFactor=0.658,  # Range: [0.0, 1.0]
            roughnessFactor=0.5  # Range: [0.0, 1.0]
        )
        
        pyrender_body_mesh = pyrender.Mesh.from_trimesh(
            body_mesh, material=material
        )
        
        pyrender_garment_mesh_list = [pyrender.Mesh.from_trimesh(
            garment_mesh, material=material
        ) for garment_mesh in garment_mesh_list]
        
        
        pyrender_cam = pyrender.PerspectiveCamera(
            yfov = np.deg2rad(cam_info.fov),
        )
        
        pyrender_scene = pyrender.Scene(bg_color=(1.0, 1.0, 1.0, 1.0))
        
        pyrender_scene.add(pyrender_body_mesh)
        
        for pyrender_garment_mesh in pyrender_garment_mesh_list :
            pyrender_scene.add(pyrender_garment_mesh)
        pyrender_scene.add(pyrender_cam, pose=cam_info.cam2world)
        
        camera_node = list(filter(
            lambda x : x.camera is not None,
            pyrender_scene.get_nodes()
        ))[-1]
        
        
        intensity = 80.
        light_positions = [
            np.array([1.60614, 1.5341, 1.23701]),
            np.array([1.31844, 1.92831, -2.52238]),
            np.array([-2.80522, 1.2594, 2.34624]),
            np.array([0.160261, 1.81789, 3.52215]),
            np.array([-2.65752, 1.41194, -1.26328])
        ]
        light_colors = [
            [1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0]
        ]

        for i in range(5):
            light = pyrender.PointLight(color=light_colors[i], intensity=intensity)
            light_pose = np.eye(4)
            light_pose[:3, 3] = light_positions[i]
            pyrender_scene.add(light, pose=light_pose)

        try :    
            r = pyrender.OffscreenRenderer(
                viewport_width=cam_info.width, viewport_height=cam_info.height
            )
            flags = pyrender.RenderFlags.SKIP_CULL_FACES
            color, depth = r.render(pyrender_scene, flags=flags)
            r.delete()
        except Exception as e :
            print(e)
            continue
        
        # remove image backgground and save image
        bg_img = plt.imread(rendered_img_path)
        mask = depth.copy()
        mask[mask != 0] = 1
        bg_img[:, :, -1] = mask
        plt.imsave(
            os.path.join(scene.garment_dir, f"{view_name}.png"),
            bg_img
        )
        
        width, height = cam_info.width, cam_info.height
        view_matrix = np.linalg.inv(pyrender_scene.get_pose(camera_node))
        proj_matrix = camera_node.camera.get_projection_matrix(width, height)
        
        visibility_mask_list = []
        pixel_coords_list = []
        for garment_mesh in garment_mesh_list :
            vertices_homog = np.hstack([
                garment_mesh.vertices,
                np.ones((garment_mesh.vertices.shape[0], 1))
            ])

            view_proj = proj_matrix @ view_matrix
            projected = vertices_homog @ view_proj.T

            z_coords = projected[:, 2].copy()
            projected = projected[:, :3] / projected[:, 3:4]

            pixel_coords = np.zeros((projected.shape[0], 2))
            pixel_coords[:, 0] = (projected[:, 0] + 1.0) * width / 2.0
            pixel_coords[:, 1] = height - (projected[:, 1] + 1.0) * height / 2.0

            px = np.clip(pixel_coords[:, 0].astype(int), 0, width - 1)
            py = np.clip(pixel_coords[:, 1].astype(int), 0, height - 1)

            THRESHOLD = -0.5
            THRESHOLD = -70.
            # THRESHOLD = -80.
            visibility_mask = (
                z_coords > 0
            ) &  (
                pixel_coords[:, 0] >= 0
            ) & (
                pixel_coords[:, 0] < width
            ) & (
                pixel_coords[:, 1] >= 0
            ) & (
                pixel_coords[:, 1] < height
            ) & (
                z_coords + THRESHOLD <= depth[py, px]
            )
            
            visibility_mask_list.append(visibility_mask)
            pixel_coords_list.append(pixel_coords)
            
            
        visible_seam_line_dict_dict = {}
        
        for idx, garment_id in enumerate(scene.stitch_dict_dict.keys()) :
            visible_seam_line_dict_dict[garment_id] = {}
            
            garment_mesh = garment_mesh_dict[garment_id]
            vert_count = garment_mesh.vertices.shape[0]
            
            stitch_dict = scene.stitch_dict_dict[garment_id]
            # seam_line_vert_idx_arr_dict = scene.seam_line_vert_idx_arr_dict_dict[garment_id]
            seam_line_vert_idx_arr_list = scene.seam_line_vert_idx_arr_list_dict_dict[view_name][garment_id]
            
            visibility_mask = visibility_mask_list[idx]
            pixel_coords = pixel_coords_list[idx]
            
            
            # for stch_idx, seam_line_vert_idx_arr in seam_line_vert_idx_arr_dict.items() :
            for stch_idx, seam_line_vert_idx_arr in enumerate(seam_line_vert_idx_arr_list) :
                # seam_line_vert_idx_arr = np.array(seam_line_vert_idx_arr)
                
                seam_line_vis_mask = []
                for seam_vert_idx in seam_line_vert_idx_arr :
                    seam_line_vis_mask.append(visibility_mask[seam_vert_idx])
                seam_line_vis_mask = np.array(seam_line_vis_mask)
                    
                # If length of disconnection between visible seam vertices
                # is less then MIN_CONSEC_VERT_TO_DISCONNECT,
                # consider the disconnection is connected
                # (which change invisible seam vertices to visible)
                idx = 0
                while idx < len(seam_line_vis_mask) :
                    if idx >= len(seam_line_vis_mask) -2 :
                        break

                    while not (seam_line_vis_mask[idx] == True and seam_line_vis_mask[idx + 1] == False) :
                        if idx >= len(seam_line_vis_mask) - 2 :
                            break
                        idx += 1
                    if idx >= len(seam_line_vis_mask) - 2 :
                        break
                    window_end_idx = min(idx + MIN_CONSEC_VERT_TO_DISCONNECT + 1, len(seam_line_vis_mask) - 1)
                    for rid in range(window_end_idx, idx, -1) :
                        if seam_line_vis_mask[rid] == True :
                            seam_line_vis_mask[idx:rid] = True
                            break
                    idx = rid
                

                # If length of connection between visible seam vertices
                # is less then MIN_CONSEC_VERT_TO_BE_SEGMENT,
                # consider the connection is not a segment
                # (which change visible seam vertices to invisible)
                idx = 0
                while idx < len(seam_line_vis_mask) :
                    if seam_line_vis_mask[idx] != True :
                        idx += 1
                        continue
                    idx2 = idx + 1
                    while idx2 < len(seam_line_vis_mask) and seam_line_vis_mask[idx2] == True :
                        idx2 += 1
                    if idx2 - idx < MIN_CONSEC_VERT_TO_BE_SEGMENT :
                        seam_line_vis_mask[idx:idx2] = False
                    idx = idx2
                    
                line_segment_idx_arr_list = []
                line_segment_pos_arr_list = []
                if True in seam_line_vis_mask :
                    idx = seam_line_vis_mask.tolist().index(True)
                    while idx < len(seam_line_vis_mask) :
                        line_segment_idx_list = []
                        line_segment_pos_list = []
                        while idx < len(seam_line_vis_mask) and seam_line_vis_mask[idx] == True :
                            line_segment_idx_list.append(
                                seam_line_vert_idx_arr[idx]
                            )
                            line_segment_pos_list.append(
                                pixel_coords[seam_line_vert_idx_arr[idx]]
                            )
                            idx += 1
                        if len(line_segment_idx_list) > 0 :
                            line_segment_idx_arr_list.append(np.array(line_segment_idx_list))
                            line_segment_pos_arr_list.append(np.array(line_segment_pos_list))
                        idx += 1

                if len(line_segment_pos_arr_list) > 0 :
                    segment_edge_len_arr_list = []
                    segment_t_arr_list = []
                    segment_u_arr_list = []
                    segment_v_arr_list = []
                    for segment_pos_arr in line_segment_pos_arr_list :
                        i_vec = segment_pos_arr[-1] - segment_pos_arr[0]
                        j_vec = np.array([i_vec[1], -i_vec[0]])
                        
                        i_vec_normalized = i_vec / np.linalg.norm(i_vec)
                        j_vec_normalized = j_vec / np.linalg.norm(j_vec)
                        
                        edge_len_arr = np.concatenate((
                            [0],
                            np.linalg.norm(segment_pos_arr[1:] - segment_pos_arr[:-1], axis=1)
                        ))
                        segment_edge_len_arr_list.append(edge_len_arr)
                        t_arr = np.cumsum(edge_len_arr) / np.sum(edge_len_arr)
                        
                        vect_arr = segment_pos_arr - segment_pos_arr[0]
                        u_arr = np.sum(vect_arr * i_vec_normalized, axis=1) / np.linalg.norm(i_vec)
                        v_arr = np.sum(vect_arr * j_vec_normalized, axis=1) / np.linalg.norm(j_vec)
                        
                        segment_t_arr_list.append(t_arr)
                        segment_u_arr_list.append(u_arr)
                        segment_v_arr_list.append(v_arr)
                    
                        
                        if len(t_arr) != len(segment_pos_arr) :
                            print(segment_pos_arr.shape, t_arr.shape, u_arr.shape, v_arr.shape)
                            print("error")
                        
                        
                        if len(t_arr) != len(u_arr) or len(t_arr) != len(v_arr) :
                            print(edge_len_arr.shape, t_arr.shape, u_arr.shape, v_arr.shape)
                            print("error")
                        
                        error_num = np.sum(
                            vect_arr - (u_arr.reshape(-1, 1) * i_vec.reshape(1, -1) + v_arr.reshape(-1, 1) * j_vec.reshape(1, -1))
                        )
                        if error_num > 1e-6 :
                            print(vect_arr.shape, u_arr.shape, v_arr.shape)
                            print(error_num)
                            print("error")

                    visible_seam_line_dict_dict[garment_id][stch_idx] = {
                        "segment_idx_arr_list" : line_segment_idx_arr_list,
                        "segment_pos_arr_list" : line_segment_pos_arr_list,
                        "segment_edge_len_arr_list" : segment_edge_len_arr_list,
                        "segment_t_arr_list" : segment_t_arr_list,
                        "segment_u_arr_list" : segment_u_arr_list,
                        "segment_v_arr_list" : segment_v_arr_list
                    }


        print(str(Path(scene.garment_dir) / f"{view_name}.pkl"), "wb")
        with open(
            str(Path(scene.garment_dir) / f"{view_name}.pkl"), "wb"
        ) as f :
            pickle.dump(
                visible_seam_line_dict_dict, f
            )
