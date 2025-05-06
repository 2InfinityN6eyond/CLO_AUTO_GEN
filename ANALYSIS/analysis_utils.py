import trimesh
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
import json
import svgpathtools as svgpath


def set_constants():
    import socket
    import os
    from glob import glob
    import torch

    hostname = socket.gethostname()
    if hostname == "hjpui-MacBookPro.local":
        DATASET_ROOT = "/media/hjp/05aba9a7-0e74-4e54-9bc9-5f11b9c4c757/GarmentCodeData/"
        
    elif hostname == "epyc64":
        DATASET_ROOT = "/home/hjp/VTO2025/GarmentCodeData"
        
    elif hostname == "server" :
        DATASET_ROOT = "/media/hjp/05aba9a7-0e74-4e54-9bc9-5f11b9c4c757/GarmentCodeData/"

    return DATASET_ROOT



     
def v_id_map(vertices): 
    v_map = [None] * len(vertices) 
    v_map[0] = 0 
    for i in range(1, len(vertices)): 
        if all(vertices[i - 1] == vertices[i]): 
            v_map[i] = v_map[i-1]   
        else: 
            v_map[i] = v_map[i-1] + 1 
    return v_map



def parse_clo_json(data) :
    panel_svg_path_dict = {}
    for panel_data in data["PatternList"] :
        panel_name = "_".join(panel_data["Name"].split("_")[2:])
        
        svg_path = []
        for line in panel_data["ShapeInfo"]["LineList"] :
            point_list = []
            for point in line["PointList"] :
                point_list.append(point["Position"]['x'] + point["Position"]['y'] * 1j)
            
            if len(point_list) == 2 :
                svg_path.append(svgpath.Line(point_list[0], point_list[1]))
            elif len(point_list) == 4 :
                svg_path.append(svgpath.CubicBezier(point_list[0], point_list[1], point_list[2], point_list[3]))
            else :
                raise ValueError("No Straight Line nor Cubic Bezier Curve")
            
        panel_svg_path_dict[panel_name] = svgpath.Path(*svg_path),
        
        print(svg_path)
        
        
        
    return panel_svg_path_dict

with open("../modified_2.json", "r") as f :
    data = json.load(f)
    
parsed = parse_clo_json(data)

# parsed

# basic visualization fucntions

def plot_panel_info(
    ax, panel_name, panel_svg_path_dict, stitch_dict,
    N_SAMPLES: int = 100,
):
    path = panel_svg_path_dict[panel_name][0]
    
    # boundary_points = np.array([path.point(t) for t in np.linspace(0, 1, N_SAMPLES)])
    # boundary_points = np.array([boundary_points.real, boundary_points.imag]).T
        
    # ax.plot(boundary_points[:, 0], boundary_points[:, 1], 'b-')
    ax.set_title(panel_name)
    ax.axis('equal')
    ax.grid(True)

    colors = plt.cm.rainbow(np.linspace(0, 1, len(path)))

    for edge_idx, segment in enumerate(path):
        segment_points = np.array([
            [segment.point(t).real, segment.point(t).imag]
            for t in np.linspace(0, 1, N_SAMPLES)
        ])
        
        ax.plot(
            segment_points[:, 0],
            segment_points[:, 1] * -1,
            '-', color=colors[edge_idx]
        )
        
        segment_center = segment.point(0.5)
        segment_center = np.array([segment_center.real, segment_center.imag])
    
        has_stitch = False
    
        for stitch_idx, stitch_edges in stitch_dict.items():
            for edge_info in stitch_edges:
                if not isinstance(edge_info, dict):
                    # print(edge_info)
                    continue
                if edge_info['edge'] == edge_idx and edge_info['panel'] == panel_name:
                    has_stitch = True
                    ax.text(
                        segment_center[0],
                        -segment_center[1],
                        f"{stitch_idx}\n{edge_info['edge']}",
                        ha='center', va='center'
                    )

        if not has_stitch:
            ax.text(
                segment_center[0],
                -segment_center[1],
                f"no stitch,\n{edge_idx}",
                ha='center', va='center'
            )
            
            

def visualize_meshes_plotly(
    mesh_list,
    color_list=None,
    vertices_list = None,
    vertices_color_list = None,
    vertex_marker_size = 2,
    show_edges = True,
    edge_width = 2,
    show = True,
):
    # Pre-convert to list and load meshes once
    mesh_list = [mesh_list] if not isinstance(mesh_list, list) else mesh_list
    final_mesh_list = [trimesh.load(m) if isinstance(m, str) else m for m in mesh_list]
    
    color_list = color_list or ['lightgray'] * len(final_mesh_list)
    
    # Create all mesh traces at once
    mesh_traces = []
    edge_traces = []
    for mesh, color in zip(final_mesh_list, color_list):
        face_colors = mesh.visual.face_colors[:, :3] if hasattr(mesh.visual, 'face_colors') else None
        mesh_traces.append(go.Mesh3d(
            x=mesh.vertices[:, 0],
            y=mesh.vertices[:, 1],
            z=mesh.vertices[:, 2],
            i=mesh.faces[:, 0],
            j=mesh.faces[:, 1],
            k=mesh.faces[:, 2],
            opacity=0.5,
            facecolor=face_colors,
            color=None if face_colors is not None else color
        ))
        
        if show_edges:
            edge_x = []
            edge_y = []
            edge_z = []
            vertices = mesh.vertices
            for edge in mesh.edges:
                edge_x.extend([vertices[edge[0], 0], vertices[edge[1], 0], None])
                edge_y.extend([vertices[edge[0], 1], vertices[edge[1], 1], None])
                edge_z.extend([vertices[edge[0], 2], vertices[edge[1], 2], None])
        
            edge_traces.append(go.Scatter3d(
                x=edge_x, y=edge_y, z=edge_z,
                mode='lines',
                line=dict(
                    color = color if color is not None else 'red',
                    width=edge_width
                ),
                name='Edges'
            ))
    
    fig = go.Figure(data = mesh_traces + edge_traces)
    
    if vertices_list is not None and vertices_color_list is not None:
        for vertex, color in zip(vertices_list, vertices_color_list):
            fig.add_trace(go.Scatter3d(
                x=vertex[:, 0],
                y=vertex[:, 1],
                z=vertex[:, 2],
                mode='markers',
                marker=dict(size=vertex_marker_size, color=color, opacity=1),
                name='Vertices'
            ))
    fig.update_layout(
        scene=dict(aspectmode='data'),
        width=800,
        height=800,
        showlegend=False
    )
    
    if show:
        fig.show()
    return fig
    
    
def visualize_camera_info(
    fig,
    cam2world,
    fov,
    aspect,
    name = None,
    near = 10,
    far = 500,
    marker_size = 8,
    cam_axis_length = 50,
) :
    """
    Add camera visualization to a Plotly figure.
    
    Args:
        fig: Plotly figure object
        cam2world: 4x4 camera-to-world transformation matrix
        fov: Field of view in radians
        aspect: Aspect ratio (width/height)
        near: Near plane distance
        far: Far plane distance
    """
    
    # Extract camera position and orientation from cam2world matrix
    cam_pos = cam2world[:3, 3]
    cam_right = cam2world[:3, 0]    # X axis is right
    cam_up = cam2world[:3, 1]       # Y axis is up
    cam_forward = -cam2world[:3, 2]  # -Z axis is forward
    
    # Calculate frustum size based on FOV
    near_height = 2 * near * np.tan(fov/2)
    near_width = near_height * aspect
    far_height = 2 * far * np.tan(fov/2)
    far_width = far_height * aspect
    
    # Calculate corner points
    near_top_right = cam_pos + near * cam_forward + (near_height/2) * cam_up + (near_width/2) * cam_right
    near_top_left = cam_pos + near * cam_forward + (near_height/2) * cam_up - (near_width/2) * cam_right
    near_bottom_right = cam_pos + near * cam_forward - (near_height/2) * cam_up + (near_width/2) * cam_right
    near_bottom_left = cam_pos + near * cam_forward - (near_height/2) * cam_up - (near_width/2) * cam_right
    
    far_top_right = cam_pos + far * cam_forward + (far_height/2) * cam_up + (far_width/2) * cam_right
    far_top_left = cam_pos + far * cam_forward + (far_height/2) * cam_up - (far_width/2) * cam_right
    far_bottom_right = cam_pos + far * cam_forward - (far_height/2) * cam_up + (far_width/2) * cam_right
    far_bottom_left = cam_pos + far * cam_forward - (far_height/2) * cam_up - (far_width/2) * cam_right
    
    # Create frustum lines
    frustum_lines = [
        # Near plane
        [near_top_right, near_top_left],
        [near_top_left, near_bottom_left],
        [near_bottom_left, near_bottom_right],
        [near_bottom_right, near_top_right],
        # Far plane
        [far_top_right, far_top_left],
        [far_top_left, far_bottom_left],
        [far_bottom_left, far_bottom_right],
        [far_bottom_right, far_top_right],
        # Connecting lines
        [near_top_right, far_top_right],
        [near_top_left, far_top_left],
        [near_bottom_left, far_bottom_left],
        [near_bottom_right, far_bottom_right],
    ]
    
    # Add frustum lines to the figure
    for line in frustum_lines:
        fig.add_trace(go.Scatter3d(
            x=[line[0][0], line[1][0]],
            y=[line[0][1], line[1][1]],
            z=[line[0][2], line[1][2]],
            mode='lines',
            line=dict(color='black', width=2),
            name='Camera Frustum'
        ))
    
    # Add camera position marker
    fig.add_trace(go.Scatter3d(
        x=[cam_pos[0]],
        y=[cam_pos[1]],
        z=[cam_pos[2]],
        mode='markers',
        marker=dict(size=marker_size, color='red'),
        name='Camera Position'
    ))
    
    # Add camera orientation vectors
    # vector_length = 50.0  # Adjust based on your scene scale
    vector_length = cam_axis_length  # Adjust based on your scene scale
    for vec, color, name in [
        (cam_right, 'red', 'Right(X)'), 
        (cam_up, 'green', 'Up(Y)'),
        (cam_forward, 'blue', 'Forward(-Z)'), 
    ]:
        fig.add_trace(go.Scatter3d(
            x=[cam_pos[0], cam_pos[0] + vector_length * vec[0]],
            y=[cam_pos[1], cam_pos[1] + vector_length * vec[1]],
            z=[cam_pos[2], cam_pos[2] + vector_length * vec[2]],
            mode='lines',
            line=dict(color=color, width=3),
            name=f'Camera {name}'
        ))
    
    return fig
    