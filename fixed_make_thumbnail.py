#!/usr/bin/env python3
"""
Fixed make_thumbnail function that prevents automatic display in Jupyter notebooks
"""

import matplotlib.pyplot as plt
import numpy as np
import os

def make_thumbnail_fixed(
    scene,
    FIG_UNIT_W=10,
    FIG_UNIT_H=10,
    NROWs=3,
    NCOLs=4,
    save_path=None,
    show=False,
):
    """
    Fixed version of make_thumbnail that prevents automatic display in Jupyter
    """
    # Turn off interactive mode to prevent automatic display
    plt.ioff()
    
    fig, axs = plt.subplots(NROWs, NCOLs, figsize=(FIG_UNIT_W * NCOLs, FIG_UNIT_H * NROWs))
    
    view_name_list = scene.view_name_list[-10:]
    
    for view_idx, view_name in enumerate(view_name_list):
        row_idx = view_idx // NCOLs
        col_idx = view_idx % NCOLs
        
        vis_seam_seg_pos_list = []
        for garment_id in scene.seam_annotation_dict[view_name].keys():
            for stch_idx, sema_line in scene.seam_annotation_dict[view_name][garment_id].items():
                for segment_pos_arr in sema_line['segment_pos_arr_list']:
                    vis_seam_seg_pos_list.append(segment_pos_arr)
        
        color_list = plt.cm.rainbow(np.linspace(0, 1, len(vis_seam_seg_pos_list)))
        
        # set title
        axs[row_idx, col_idx].set_title(view_name)
        
        # plot seam line
        axs[row_idx, col_idx].imshow(scene.image_dict[view_name])
        for pos_arr, color in zip(vis_seam_seg_pos_list, color_list):
            axs[row_idx, col_idx].plot(pos_arr[:, 0], pos_arr[:, 1], color=color)
        axs[row_idx, col_idx].axis("off")
    
    plt.tight_layout()
    
    if save_path is not None:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"Figure saved to: {save_path}")
    
    if show:
        plt.show()
    else:
        # Close the figure to prevent automatic display
        plt.close(fig)
    
    # Turn interactive mode back on
    plt.ion()
    
    return fig

# Alternative version with more control
def make_thumbnail_advanced(
    scene,
    FIG_UNIT_W=10,
    FIG_UNIT_H=10,
    NROWs=3,
    NCOLs=4,
    save_path=None,
    show=False,
    close_figure=True,
):
    """
    Advanced version with more control over figure display
    """
    # Turn off interactive mode
    plt.ioff()
    
    fig, axs = plt.subplots(NROWs, NCOLs, figsize=(FIG_UNIT_W * NCOLs, FIG_UNIT_H * NROWs))
    
    view_name_list = scene.view_name_list[-10:]
    
    for view_idx, view_name in enumerate(view_name_list):
        row_idx = view_idx // NCOLs
        col_idx = view_idx % NCOLs
        
        vis_seam_seg_pos_list = []
        for garment_id in scene.seam_annotation_dict[view_name].keys():
            for stch_idx, sema_line in scene.seam_annotation_dict[view_name][garment_id].items():
                for segment_pos_arr in sema_line['segment_pos_arr_list']:
                    vis_seam_seg_pos_list.append(segment_pos_arr)
        
        color_list = plt.cm.rainbow(np.linspace(0, 1, len(vis_seam_seg_pos_list)))
        
        # set title
        axs[row_idx, col_idx].set_title(view_name)
        
        # plot seam line
        axs[row_idx, col_idx].imshow(scene.image_dict[view_name])
        for pos_arr, color in zip(vis_seam_seg_pos_list, color_list):
            axs[row_idx, col_idx].plot(pos_arr[:, 0], pos_arr[:, 1], color=color)
        axs[row_idx, col_idx].axis("off")
    
    plt.tight_layout()
    
    if save_path is not None:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"Figure saved to: {save_path}")
    
    if show:
        plt.show()
    elif close_figure:
        # Close the figure to prevent automatic display
        plt.close(fig)
        fig = None  # Return None since figure is closed
    
    # Turn interactive mode back on
    plt.ion()
    
    return fig

# Usage examples:
"""
# Example 1: Save without showing (recommended for Jupyter)
scene = scene_list[0]
fig = make_thumbnail_fixed(
    scene,
    save_path=os.path.join(scene.garment_dir, "thumbnail.png"),
    show=False
)

# Example 2: Show the figure
fig = make_thumbnail_fixed(
    scene,
    save_path=os.path.join(scene.garment_dir, "thumbnail.png"),
    show=True
)

# Example 3: Advanced control
fig = make_thumbnail_advanced(
    scene,
    save_path=os.path.join(scene.garment_dir, "thumbnail.png"),
    show=False,
    close_figure=True  # This will close the figure and return None
)
"""

# Quick fix for your existing code:
def quick_fix_for_existing_code():
    """
    If you want to keep your existing make_thumbnail function,
    just wrap it with these commands:
    """
    
    # Before calling your function:
    plt.ioff()
    
    # Your existing function call:
    # make_thumbnail(scene, save_path="...", show=False)
    
    # After calling your function:
    plt.ion()
    
    print("This prevents automatic display in Jupyter")

if __name__ == "__main__":
    print("Fixed make_thumbnail functions")
    print("=" * 40)
    print("Use make_thumbnail_fixed() instead of make_thumbnail()")
    print("This will prevent automatic display in Jupyter notebooks")


