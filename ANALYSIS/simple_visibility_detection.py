import numpy as np
import trimesh
import matplotlib.pyplot as plt
from dataclasses import dataclass


@dataclass
class CloCamera:
    name: str
    cam2world: np.ndarray
    fov: float
    width: int
    height: int


def render(
    
) :
    pass


def get_visible_vertices_simple(
    mesh, 
    camera: CloCamera,
    depth_map=None,
    depth_tolerance=2.0,
    use_depth_test=True
):
    """
    Simple and accurate visibility detection for CLO camera and mesh.
    
    Args:
        mesh: Trimesh object
        camera: CloCamera object with cam2world, fov, width, height
        depth_map: Optional depth map for occlusion testing
        depth_tolerance: Tolerance for depth comparison
        use_depth_test: Whether to use depth map for occlusion testing
    
    Returns:
        visibility_mask: Boolean array indicating visible vertices
        pixel_coords: Pixel coordinates for each vertex
        depths: Depth values for each vertex
    """
    
    # Get camera parameters
    cam2world = camera.cam2world
    fov_rad = np.deg2rad(camera.fov)
    width, height = camera.width, camera.height
    
    # Camera position (inverse of cam2world translation)
    camera_pos = -cam2world[:3, :3].T @ cam2world[:3, 3]
    
    # Create projection matrix
    aspect = width / height
    near, far = 0.1, 10000.0
    
    proj_matrix = np.array([
        [1/(aspect * np.tan(fov_rad/2)), 0, 0, 0],
        [0, 1/np.tan(fov_rad/2), 0, 0],
        [0, 0, -(far + near)/(far - near), -2*far*near/(far - near)],
        [0, 0, -1, 0]
    ])
    
    # Transform vertices to camera space
    vertices_homog = np.hstack([mesh.vertices, np.ones((mesh.vertices.shape[0], 1))])
    view_matrix = np.linalg.inv(cam2world)
    view_proj = proj_matrix @ view_matrix
    projected = vertices_homog @ view_proj.T
    
    # Store w coordinates before perspective division
    w_coords = projected[:, 3].copy()
    
    # Perspective division
    depths = projected[:, 2].copy()
    projected = projected[:, :3] / projected[:, 3:4]
    
    # Convert to pixel coordinates
    pixel_coords = np.zeros((projected.shape[0], 2))
    pixel_coords[:, 0] = (projected[:, 0] + 1.0) * width / 2.0
    pixel_coords[:, 1] = height - (projected[:, 1] + 1.0) * height / 2.0
    
    # Initialize visibility mask
    visibility_mask = np.zeros(len(mesh.vertices), dtype=bool)
    
    # Basic frustum culling
    in_frustum = (
        (depths > 0) &  # In front of camera
        (w_coords > 0) &  # Valid projection (w > 0)
        (pixel_coords[:, 0] >= 0) & (pixel_coords[:, 0] < width) &
        (pixel_coords[:, 1] >= 0) & (pixel_coords[:, 1] < height)
    )
    
    # Mark vertices in frustum as potentially visible
    visibility_mask[in_frustum] = True
    
    # If depth map is provided, perform occlusion testing
    if use_depth_test and depth_map is not None:
        for i in np.where(in_frustum)[0]:
            px, py = int(pixel_coords[i, 0]), int(pixel_coords[i, 1])
            
            if 0 <= px < width and 0 <= py < height:
                depth_at_pixel = depth_map[py, px]
                vertex_depth = depths[i]
                
                # Check if vertex is occluded
                if abs(vertex_depth - depth_at_pixel) > depth_tolerance:
                    visibility_mask[i] = False
    
    return visibility_mask, pixel_coords, depths


def get_visible_vertices_with_occlusion(
    mesh_list, 
    camera: CloCamera,
    depth_map,
    depth_tolerance=2.0
):
    """
    Get visible vertices for multiple meshes with occlusion testing.
    
    Args:
        mesh_list: List of trimesh objects
        camera: CloCamera object
        depth_map: Depth map from rendering
        depth_tolerance: Tolerance for depth comparison
    
    Returns:
        visibility_mask_list: List of visibility masks for each mesh
        pixel_coords_list: List of pixel coordinates for each mesh
        depths_list: List of depth values for each mesh
    """
    
    visibility_mask_list = []
    pixel_coords_list = []
    depths_list = []
    
    for mesh in mesh_list:
        vis_mask, pix_coords, depths = get_visible_vertices_simple(
            mesh, camera, depth_map, depth_tolerance, use_depth_test=True
        )
        
        visibility_mask_list.append(vis_mask)
        pixel_coords_list.append(pix_coords)
        depths_list.append(depths)
    
    return visibility_mask_list, pixel_coords_list, depths_list


def visualize_visibility_simple(
    mesh_list,
    visibility_mask_list,
    pixel_coords_list,
    camera: CloCamera,
    rendered_image=None,
    save_path=None
):
    """
    Simple visualization of visibility results.
    
    Args:
        mesh_list: List of meshes
        visibility_mask_list: List of visibility masks
        pixel_coords_list: List of pixel coordinates
        camera: CloCamera object
        rendered_image: Optional rendered image for background
        save_path: Optional path to save visualization
    """
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Create a blank image if no rendered image provided
    if rendered_image is None:
        rendered_image = np.ones((camera.height, camera.width, 3))
    
    # Original image
    axes[0, 0].imshow(rendered_image)
    axes[0, 0].set_title('Original Image')
    axes[0, 0].axis('off')
    
    # Visible vertices overlay
    axes[0, 1].imshow(rendered_image)
    colors = plt.cm.rainbow(np.linspace(0, 1, len(mesh_list)))
    
    for i, (vis_mask, pix_coords) in enumerate(zip(visibility_mask_list, pixel_coords_list)):
        visible_pixels = pix_coords[vis_mask]
        if len(visible_pixels) > 0:
            axes[0, 1].scatter(
                visible_pixels[:, 0], visible_pixels[:, 1],
                s=2, alpha=0.8, color=colors[i], label=f'Mesh {i+1}'
            )
    
    axes[0, 1].set_title('Visible Vertices')
    axes[0, 1].legend()
    axes[0, 1].axis('off')
    
    # Visibility mask
    mask_overlay = np.zeros((camera.height, camera.width, 4), dtype=np.uint8)
    mask_overlay[:, :, 3] = 255  # Alpha channel
    
    for i, (vis_mask, pix_coords) in enumerate(zip(visibility_mask_list, pixel_coords_list)):
        visible_pixels = pix_coords[vis_mask].astype(int)
        color = (colors[i][:3] * 255).astype(np.uint8)
        
        for px, py in visible_pixels:
            if 0 <= px < camera.width and 0 <= py < camera.height:
                mask_overlay[py, px, :3] = color
                mask_overlay[py, px, 3] = 255
    
    axes[1, 0].imshow(mask_overlay)
    axes[1, 0].set_title('Visibility Mask')
    axes[1, 0].axis('off')
    
    # Statistics
    total_vertices = sum(len(mesh.vertices) for mesh in mesh_list)
    visible_vertices = sum(np.sum(mask) for mask in visibility_mask_list)
    visibility_percentage = (visible_vertices / total_vertices) * 100 if total_vertices > 0 else 0
    
    axes[1, 1].text(0.1, 0.9, f'Camera: {camera.name}', fontsize=12, fontweight='bold')
    axes[1, 1].text(0.1, 0.8, f'Resolution: {camera.width}x{camera.height}', fontsize=10)
    axes[1, 1].text(0.1, 0.7, f'FOV: {camera.fov}°', fontsize=10)
    axes[1, 1].text(0.1, 0.6, f'Total Vertices: {total_vertices}', fontsize=10)
    axes[1, 1].text(0.1, 0.5, f'Visible Vertices: {visible_vertices}', fontsize=10)
    axes[1, 1].text(0.1, 0.4, f'Visibility: {visibility_percentage:.1f}%', fontsize=10)
    
    for i, (mesh, mask) in enumerate(zip(mesh_list, visibility_mask_list)):
        mesh_visibility = (np.sum(mask) / len(mesh.vertices)) * 100 if len(mesh.vertices) > 0 else 0
        axes[1, 1].text(0.1, 0.3 - i*0.08, f'Mesh {i+1}: {mesh_visibility:.1f}% ({np.sum(mask)}/{len(mesh.vertices)})', 
                        fontsize=9, color=colors[i])
    
    axes[1, 1].set_title('Visibility Statistics')
    axes[1, 1].axis('off')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()


# Example usage function
def example_usage():
    """
    Example of how to use the visibility detection functions.
    """
    
    # Example camera (replace with your actual camera)
    camera = CloCamera(
        name='Custom_View_1',
        cam2world=np.array([
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 896.122],
            [0.0, 0.0, 1.0, 7998.56],
            [0.0, 0.0, 0.0, 1.0]
        ]),
        fov=15,
        width=480,
        height=640
    )
    
    # Example usage:
    # 1. For single mesh without depth testing:
    # vis_mask, pix_coords, depths = get_visible_vertices_simple(mesh, camera)
    
    # 2. For multiple meshes with depth testing:
    # vis_masks, pix_coords_list, depths_list = get_visible_vertices_with_occlusion(
    #     mesh_list, camera, depth_map
    # )
    
    # 3. Visualize results:
    # visualize_visibility_simple(mesh_list, vis_masks, pix_coords_list, camera, rendered_image)
    
    print("Visibility detection functions ready to use!")
    print("Use get_visible_vertices_simple() for single mesh")
    print("Use get_visible_vertices_with_occlusion() for multiple meshes with occlusion")
    print("Use visualize_visibility_simple() for visualization")
