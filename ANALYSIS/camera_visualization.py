import numpy as np
import plotly.graph_objects as go

def visualize_camera_info(
    fig,
    cam2world,
    fov,
    aspect,
    near = 10,
    far = 500,
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
    cam_forward = -cam2world[:3, 2]  # -Z axis is forward
    cam_right = cam2world[:3, 0]    # X axis is right
    cam_up = cam2world[:3, 1]       # Y axis is up
    
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
            line=dict(color='blue', width=2),
            name='Camera Frustum'
        ))
    
    # Add camera position marker
    fig.add_trace(go.Scatter3d(
        x=[cam_pos[0]],
        y=[cam_pos[1]],
        z=[cam_pos[2]],
        mode='markers',
        marker=dict(size=8, color='red'),
        name='Camera Position'
    ))
    
    # Add camera orientation vectors
    vector_length = 50.0  # Adjust based on your scene scale
    for vec, color, name in [(cam_forward, 'green', 'Forward'), 
                           (cam_right, 'red', 'Right'), 
                           (cam_up, 'blue', 'Up')]:
        fig.add_trace(go.Scatter3d(
            x=[cam_pos[0], cam_pos[0] + vector_length * vec[0]],
            y=[cam_pos[1], cam_pos[1] + vector_length * vec[1]],
            z=[cam_pos[2], cam_pos[2] + vector_length * vec[2]],
            mode='lines',
            line=dict(color=color, width=3),
            name=f'Camera {name}'
        ))
    
    return fig 