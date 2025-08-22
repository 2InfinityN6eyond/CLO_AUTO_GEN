#!/usr/bin/env python3
"""
Example showing how to modify the make_thumbnail function to use 
the new SewingPattern.draw() method with external subplots.
"""

import matplotlib.pyplot as plt
import numpy as np

def make_thumbnail_modified(
    scene,
    FIG_UNIT_W = 10,
    FIG_UNIT_H = 10,
    NROWs = 4,
    NCOLs = 3,
) :
    fig, axs = plt.subplots(NROWs, NCOLs, figsize=(FIG_UNIT_W * NCOLs, FIG_UNIT_H * NROWs))
    
    view_name_list = scene.view_name_list[-10:]
    
    for view_idx, view_name in view_name_list :
        row_idx = view_idx // NCOLs
        col_idx = view_idx % NCOLs
        
        vis_seam_seg_pos_list = []
        for garment_id in scene.seam_annotation_dict[view_name].keys() :
            for stch_idx, sema_line in scene.seam_annotation_dict[view_name][garment_id].items() :
                for segment_pos_arr in sema_line['segment_pos_arr_list'] :
                    vis_seam_seg_pos_list.append(segment_pos_arr)
        
        color_list = plt.cm.rainbow(np.linspace(0, 1, len(vis_seam_seg_pos_list)))
        
        axs[row_idx, col_idx].imshow(scene.image_dict[view_name])
        for pos_arr, color in zip(vis_seam_seg_pos_list, color_list) :
            axs[row_idx, col_idx].plot(pos_arr[:, 0], pos_arr[:, 1], color=color)
        axs[row_idx, col_idx].axis("off")
    
    # NEW: Draw sewing patterns on the first row using the modified method
    for idx, sewing_pattern in enumerate(scene.sewing_pattern_dict.values()) :
        if idx < NCOLs:  # Only draw if we have enough columns
            # Option 1: Use draw_on_axes for a single pattern on one subplot
            sewing_pattern.draw_on_axes(axs[0, idx])
            axs[0, idx].set_title(f"Sewing Pattern {idx}")
            axs[0, idx].axis("off")
    
    plt.tight_layout()
    plt.show()

def make_thumbnail_alternative(
    scene,
    FIG_UNIT_W = 10,
    FIG_UNIT_H = 10,
    NROWs = 4,
    NCOLs = 3,
) :
    fig, axs = plt.subplots(NROWs, NCOLs, figsize=(FIG_UNIT_W * NCOLs, FIG_UNIT_H * NROWs))
    
    view_name_list = scene.view_name_list[-10:]
    
    for view_idx, view_name in view_name_list :
        row_idx = view_idx // NCOLs
        col_idx = view_idx % NCOLs
        
        vis_seam_seg_pos_list = []
        for garment_id in scene.seam_annotation_dict[view_name].keys() :
            for stch_idx, sema_line in scene.seam_annotation_dict[view_name][garment_id].items() :
                for segment_pos_arr in sema_line['segment_pos_arr_list'] :
                    vis_seam_seg_pos_list.append(segment_pos_arr)
        
        color_list = plt.cm.rainbow(np.linspace(0, 1, len(vis_seam_seg_pos_list)))
        
        axs[row_idx, col_idx].imshow(scene.image_dict[view_name])
        for pos_arr, color in zip(vis_seam_seg_pos_list, color_list) :
            axs[row_idx, col_idx].plot(pos_arr[:, 0], pos_arr[:, 1], color=color)
        axs[row_idx, col_idx].axis("off")
    
    # NEW: Alternative approach - create a separate figure for sewing patterns
    # and use the modified draw method
    sewing_patterns = list(scene.sewing_pattern_dict.values())
    if sewing_patterns:
        # Create a separate figure for sewing patterns
        pattern_fig, pattern_axs = plt.subplots(1, min(len(sewing_patterns), NCOLs), 
                                               figsize=(FIG_UNIT_W * min(len(sewing_patterns), NCOLs), FIG_UNIT_H))
        
        # Handle single subplot case
        if len(sewing_patterns) == 1:
            pattern_axs = [pattern_axs]
        
        for idx, sewing_pattern in enumerate(sewing_patterns[:NCOLs]):
            sewing_pattern.draw_on_axes(pattern_axs[idx])
            pattern_axs[idx].set_title(f"Sewing Pattern {idx}")
            pattern_axs[idx].axis("off")
        
        pattern_fig.tight_layout()
        pattern_fig.show()
    
    plt.tight_layout()
    plt.show()

# Example usage in your notebook:
"""
# Instead of the original code:
for idx, sewing_pattern in enumerate(scene.sewing_pattern_dict.values()) :
    axs[0, idx].imshow(sewing_pattern.draw())
    axs[0, idx].axis("off")

# You can now use:
for idx, sewing_pattern in enumerate(scene.sewing_pattern_dict.values()) :
    sewing_pattern.draw_on_axes(axs[0, idx])
    axs[0, idx].set_title(f"Sewing Pattern {idx}")
    axs[0, idx].axis("off")

# Or if you want to use the modified draw method:
sewing_patterns = list(scene.sewing_pattern_dict.values())
if sewing_patterns:
    # Create subplots for the first row
    pattern_axs = axs[0, :min(len(sewing_patterns), NCOLs)]
    for idx, sewing_pattern in enumerate(sewing_patterns[:NCOLs]):
        sewing_pattern.draw_on_axes(pattern_axs[idx])
        pattern_axs[idx].set_title(f"Sewing Pattern {idx}")
        pattern_axs[idx].axis("off")
"""



