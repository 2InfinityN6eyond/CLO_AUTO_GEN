import numpy as np
import trimesh
import pyrender
from pathlib import Path
import matplotlib.pyplot as plt


def accurate_vertex_visibility_detection(
    mesh, 
    camera_info, 
    depth_map, 
    width, 
    height,
    ray_samples=5,  # Number of rays per vertex for robustness
    depth_tolerance=1.0,  # Tolerance for depth comparison
    use_face_visibility=True  # Use face-based visibility as additional check
):
    """
    More accurate vertex visibility detection using multiple ray casting and depth testing.
    
    Args:
        mesh: Trimesh object
        camera_info: Camera parameters with cam2world, fov, near, far attributes
        depth_map: Depth map from rendering
        width, height: Image dimensions
        ray_samples: Number of rays to cast per vertex
        depth_tolerance: Tolerance for depth comparison
        use_face_visibility: Whether to use face visibility as additional check
    
    Returns:
        visibility_mask: Boolean array indicating visible vertices
        pixel_coords: Pixel coordinates for each vertex
    """
    
    # Get camera matrices
    view_matrix = camera_info.cam2world
    proj_matrix = np.array([
        [1/np.tan(np.deg2rad(camera_info.fov)/2), 0, 0, 0],
        [0, 1/np.tan(np.deg2rad(camera_info.fov)/2), 0, 0],
        [0, 0, -(1000 + 0.1)/(1000 - 0.1), -2*1000*0.1/(1000 - 0.1)],
        [0, 0, -1, 0]
    ])
    
    # Transform vertices to camera space
    vertices_homog = np.hstack([mesh.vertices, np.ones((mesh.vertices.shape[0], 1))])
    view_proj = proj_matrix @ np.linalg.inv(view_matrix)
    projected = vertices_homog @ view_proj.T
    
    # Perspective division
    z_coords = projected[:, 2].copy()
    projected = projected[:, :3] / projected[:, 3:4]
    
    # Convert to pixel coordi-nates
    pixel_coords = np.zeros((projected.shape[0], 2))
    pixel_coords[:, 0] = (projected[:, 0] + 1.0) * width / 2.0
    pixel_coords[:, 1] = height - (projected[:, 1] + 1.0) * height / 2.0
    
    # Initialize visibility mask
    visibility_mask = np.zeros(len(mesh.vertices), dtype=bool)
    
    # Basic frustum culling
    in_frustum = (
        (z_coords > 0) &
        (pixel_coords[:, 0] >= 0) & (pixel_coords[:, 0] < width) &
        (pixel_coords[:, 1] >= 0) & (pixel_coords[:, 1] < height)
    )
    
    # For vertices in frustum, perform detailed visibility testing
    for i in np.where(in_frustum)[0]:
        vertex = mesh.vertices[i]
        pixel_x, pixel_y = pixel_coords[i]
        vertex_depth = z_coords[i]
        
        # Sample multiple rays around the vertex for robustness
        visible_rays = 0
        total_rays = 0
        
        # Create small offsets around the vertex
        np.random.seed(42)  # For reproducibility
        offsets = np.random.uniform(-0.01, 0.01, (ray_samples, 3))
        
        for offset in offsets:
            test_vertex = vertex + offset
            test_vertex_homog = np.append(test_vertex, 1)
            test_projected = test_vertex_homog @ view_proj.T
            
            if test_projected[3] <= 0:  # Behind camera
                continue
                
            test_projected = test_projected[:3] / test_projected[3]
            test_pixel_x = int((test_projected[0] + 1.0) * width / 2.0)
            test_pixel_y = int(height - (test_projected[1] + 1.0) * height / 2.0)
            
            if (0 <= test_pixel_x < width and 0 <= test_pixel_y < height):
                total_rays += 1
                depth_at_pixel = depth_map[test_pixel_y, test_pixel_x]
                
                # Check if vertex is visible (depth is close to depth map)
                if abs(test_projected[2] - depth_at_pixel) < depth_tolerance:
                    visible_rays += 1
        
        # Vertex is visible if majority of rays are visible
        if total_rays > 0 and visible_rays / total_rays > 0.5:
            visibility_mask[i] = True
    
    # Additional face-based visibility check
    if use_face_visibility and hasattr(mesh, 'faces') and len(mesh.faces) > 0:
        face_visibility = np.zeros(len(mesh.faces), dtype=bool)
        
        for face_idx, face in enumerate(mesh.faces):
            face_vertices = mesh.vertices[face]
            face_center = np.mean(face_vertices, axis=0)
            
            # Check if face center is visible
            face_center_homog = np.append(face_center, 1)
            face_projected = face_center_homog @ view_proj.T
            
            if face_projected[3] > 0:
                face_projected = face_projected[:3] / face_projected[3]
                face_pixel_x = int((face_projected[0] + 1.0) * width / 2.0)
                face_pixel_y = int(height - (face_projected[1] + 1.0) * height / 2.0)
                
                if (0 <= face_pixel_x < width and 0 <= face_pixel_y < height):
                    depth_at_face = depth_map[face_pixel_y, face_pixel_x]
                    if abs(face_projected[2] - depth_at_face) < depth_tolerance:
                        face_visibility[face_idx] = True
        
        # Mark vertices as visible if they belong to visible faces
        for face_idx, face in enumerate(mesh.faces):
            if face_visibility[face_idx]:
                visibility_mask[face] = True
    
    return visibility_mask, pixel_coords


def ray_cast_visibility_detection(
    mesh, 
    camera_info, 
    depth_map, 
    width, 
    height,
    ray_density=1.0  # Rays per pixel
):
    """
    Ray casting based visibility detection for high accuracy.
    
    Args:
        mesh: Trimesh object
        camera_info: Camera parameters
        depth_map: Depth map from rendering
        width, height: Image dimensions
        ray_density: Number of rays per pixel
    
    Returns:
        visibility_mask: Boolean array indicating visible vertices
        pixel_coords: Pixel coordinates for each vertex
    """
    
    # Create ray origins (camera position)
    camera_pos = camera_info.cam2world[:3, 3]
    
    # Transform vertices to camera space
    view_matrix = camera_info.cam2world
    proj_matrix = np.array([
        [1/np.tan(np.deg2rad(camera_info.fov)/2), 0, 0, 0],
        [0, 1/np.tan(np.deg2rad(camera_info.fov)/2), 0, 0],
        [0, 0, -(1000 + 0.1)/(1000 - 0.1), -2*1000*0.1/(1000 - 0.1)],
        [0, 0, -1, 0]
    ])
    
    vertices_homog = np.hstack([mesh.vertices, np.ones((mesh.vertices.shape[0], 1))])
    view_proj = proj_matrix @ np.linalg.inv(view_matrix)
    projected = vertices_homog @ view_proj.T
    
    z_coords = projected[:, 2].copy()
    projected = projected[:, :3] / projected[:, 3:4]
    
    pixel_coords = np.zeros((projected.shape[0], 2))
    pixel_coords[:, 0] = (projected[:, 0] + 1.0) * width / 2.0
    pixel_coords[:, 1] = height - (projected[:, 1] + 1.0) * height / 2.0
    
    visibility_mask = np.zeros(len(mesh.vertices), dtype=bool)
    
    # Basic frustum culling
    in_frustum = (
        (z_coords > 0) &
        (pixel_coords[:, 0] >= 0) & (pixel_coords[:, 0] < width) &
        (pixel_coords[:, 1] >= 0) & (pixel_coords[:, 1] < height)
    )
    
    # For each vertex in frustum, perform ray casting
    for i in np.where(in_frustum)[0]:
        vertex = mesh.vertices[i]
        pixel_x, pixel_y = pixel_coords[i]
        
        # Cast ray from camera to vertex
        ray_direction = vertex - camera_pos
        ray_direction = ray_direction / np.linalg.norm(ray_direction)
        
        # Check if ray intersects with depth map
        ray_length = np.linalg.norm(vertex - camera_pos)
        
        # Sample depth along ray
        sample_points = np.linspace(0, ray_length, int(ray_length * ray_density))
        visible = True
        
        for t in sample_points:
            sample_point = camera_pos + t * ray_direction
            
            # Project sample point to image plane
            sample_homog = np.append(sample_point, 1)
            sample_projected = sample_homog @ view_proj.T
            
            if sample_projected[3] > 0:
                sample_projected = sample_projected[:3] / sample_projected[3]
                sample_pixel_x = int((sample_projected[0] + 1.0) * width / 2.0)
                sample_pixel_y = int(height - (sample_projected[1] + 1.0) * height / 2.0)
                
                if (0 <= sample_pixel_x < width and 0 <= sample_pixel_y < height):
                    depth_at_sample = depth_map[sample_pixel_y, sample_pixel_x]
                    
                    # If we hit something before reaching the vertex, it's occluded
                    if abs(sample_projected[2] - depth_at_sample) < 1.0 and t < ray_length * 0.95:
                        visible = False
                        break
        
        if visible:
            visibility_mask[i] = True
    
    return visibility_mask, pixel_coords


def multi_pass_visibility_detection(
    mesh_list, 
    camera_info, 
    depth_map, 
    width, 
    height,
    passes=3
):
    """
    Multi-pass visibility detection for better accuracy.
    
    Args:
        mesh_list: List of meshes
        camera_info: Camera parameters
        depth_map: Depth map from rendering
        width, height: Image dimensions
        passes: Number of visibility detection passes
    
    Returns:
        visibility_mask_list: List of visibility masks for each mesh
        pixel_coords_list: List of pixel coordinates for each mesh
    """
    visibility_mask_list = []
    pixel_coords_list = []
    
    for mesh in mesh_list:
        # First pass: Basic visibility detection
        vis_mask, pix_coords = accurate_vertex_visibility_detection(
            mesh, camera_info, depth_map, width, height
        )
        
        # Additional passes: Refine visibility using neighboring information
        for pass_num in range(passes - 1):
            # Create a refined mesh with only visible vertices
            visible_vertices = mesh.vertices[vis_mask]
            
            if len(visible_vertices) > 0:
                # Create a temporary mesh for refinement
                temp_mesh = trimesh.Trimesh(vertices=visible_vertices)
                
                # Re-run visibility detection on visible subset with tighter parameters
                refined_mask, refined_coords = accurate_vertex_visibility_detection(
                    temp_mesh, camera_info, depth_map, width, height,
                    ray_samples=3, depth_tolerance=0.5
                )
                
                # Update original visibility mask
                vis_mask[vis_mask] = refined_mask
        
        visibility_mask_list.append(vis_mask)
        pixel_coords_list.append(pix_coords)
    
    return visibility_mask_list, pixel_coords_list


def visualize_visibility_results(
    mesh_list, 
    visibility_mask_list, 
    pixel_coords_list, 
    rendered_image,
    save_path=None
):
    """
    Visualize visibility detection results.
    
    Args:
        mesh_list: List of meshes
        visibility_mask_list: List of visibility masks
        pixel_coords_list: List of pixel coordinates
        rendered_image: Original rendered image
        save_path: Path to save visualization
    """
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Original image
    axes[0, 0].imshow(rendered_image)
    axes[0, 0].set_title('Original Rendered Image')
    axes[0, 0].axis('off')
    
    # All visible vertices
    axes[0, 1].imshow(rendered_image)
    for i, (vis_mask, pix_coords) in enumerate(zip(visibility_mask_list, pixel_coords_list)):
        visible_pixels = pix_coords[vis_mask]
        if len(visible_pixels) > 0:
            axes[0, 1].scatter(visible_pixels[:, 0], visible_pixels[:, 1], 
                             s=1, alpha=0.7, label=f'Mesh {i+1}')
    axes[0, 1].set_title('All Visible Vertices')
    axes[0, 1].legend()
    axes[0, 1].axis('off')
    
    # Visibility mask overlay
    mask_overlay = np.zeros_like(rendered_image)
    for i, (vis_mask, pix_coords) in enumerate(zip(visibility_mask_list, pixel_coords_list)):
        visible_pixels = pix_coords[vis_mask].astype(int)
        for px, py in visible_pixels:
            if 0 <= px < mask_overlay.shape[1] and 0 <= py < mask_overlay.shape[0]:
                mask_overlay[py, px] = [255, 0, 0, 255]  # Red for visible vertices
    
    axes[1, 0].imshow(mask_overlay)
    axes[1, 0].set_title('Visibility Mask Overlay')
    axes[1, 0].axis('off')
    
    # Statistics
    total_vertices = sum(len(mesh.vertices) for mesh in mesh_list)
    visible_vertices = sum(np.sum(mask) for mask in visibility_mask_list)
    visibility_percentage = (visible_vertices / total_vertices) * 100
    
    axes[1, 1].text(0.1, 0.8, f'Total Vertices: {total_vertices}', fontsize=12)
    axes[1, 1].text(0.1, 0.6, f'Visible Vertices: {visible_vertices}', fontsize=12)
    axes[1, 1].text(0.1, 0.4, f'Visibility: {visibility_percentage:.1f}%', fontsize=12)
    
    for i, (mesh, mask) in enumerate(zip(mesh_list, visibility_mask_list)):
        mesh_visibility = (np.sum(mask) / len(mesh.vertices)) * 100
        axes[1, 1].text(0.1, 0.2 - i*0.15, f'Mesh {i+1}: {mesh_visibility:.1f}%', fontsize=10)
    
    axes[1, 1].set_title('Visibility Statistics')
    axes[1, 1].axis('off')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()
