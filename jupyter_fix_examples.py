#!/usr/bin/env python3
"""
Solutions for preventing automatic figure display in Jupyter notebooks
"""

import matplotlib.pyplot as plt
import numpy as np

def solution_1_turn_off_interactive():
    """Solution 1: Turn off interactive mode"""
    print("Solution 1: Turn off interactive mode")
    print("-" * 50)
    
    # Turn off interactive mode
    plt.ioff()
    
    # Create and draw your figure
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot([1, 2, 3, 4], [1, 4, 2, 3])
    ax.set_title("Test Plot")
    
    # Save without showing
    fig.savefig('test_plot.png', dpi=300, bbox_inches='tight')
    print("Figure saved without displaying")
    
    # Turn interactive mode back on
    plt.ion()
    
    return fig

def solution_2_close_figure():
    """Solution 2: Close the figure immediately"""
    print("\nSolution 2: Close figure immediately")
    print("-" * 50)
    
    # Create and draw your figure
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot([1, 2, 3, 4], [1, 4, 2, 3])
    ax.set_title("Test Plot")
    
    # Save the figure
    fig.savefig('test_plot2.png', dpi=300, bbox_inches='tight')
    print("Figure saved")
    
    # Close the figure to prevent display
    plt.close(fig)
    print("Figure closed - won't display")
    
    return fig

def solution_3_use_context_manager():
    """Solution 3: Use context manager to control display"""
    print("\nSolution 3: Use context manager")
    print("-" * 50)
    
    with plt.style.context('default'):
        # Turn off interactive mode temporarily
        plt.ioff()
        
        # Create and draw your figure
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot([1, 2, 3, 4], [1, 4, 2, 3])
        ax.set_title("Test Plot")
        
        # Save the figure
        fig.savefig('test_plot3.png', dpi=300, bbox_inches='tight')
        print("Figure saved")
        
        # Close the figure
        plt.close(fig)
        
        # Turn interactive mode back on
        plt.ion()
    
    return fig

def solution_4_for_sewing_pattern():
    """Solution 4: Specifically for SewingPattern"""
    print("\nSolution 4: For SewingPattern")
    print("-" * 50)
    
    # Import your sewing pattern
    from sewing_pattern import SewingPattern
    import svgpathtools as svgpath
    
    # Create a simple sewing pattern for testing
    panel_path = svgpath.Path(
        svgpath.Line(0+0j, 10+0j),
        svgpath.Line(10+0j, 10+10j),
        svgpath.Line(10+10j, 0+10j),
        svgpath.Line(0+10j, 0+0j)
    )
    
    panel_svg_path_dict = {"front_panel": [panel_path]}
    stitch_dict = {0: {"panel_0": "front_panel", "edge_0": 0, "panel_1": "front_panel", "edge_1": 2, "stitch_direction": True}}
    sewing_pattern = SewingPattern(panel_svg_path_dict, stitch_dict)
    
    # Turn off interactive mode
    plt.ioff()
    
    # Draw without showing
    fig, axs = sewing_pattern.draw(show=False)
    
    # Save the figure
    fig.savefig('sewing_pattern_test.png', dpi=300, bbox_inches='tight')
    print("Sewing pattern saved without displaying")
    
    # Close the figure
    plt.close(fig)
    
    # Turn interactive mode back on
    plt.ion()
    
    return fig

def solution_5_use_save_figure_method():
    """Solution 5: Use the save_figure method"""
    print("\nSolution 5: Use save_figure method")
    print("-" * 50)
    
    # Import your sewing pattern
    from sewing_pattern import SewingPattern
    import svgpathtools as svgpath
    
    # Create a simple sewing pattern for testing
    panel_path = svgpath.Path(
        svgpath.Line(0+0j, 10+0j),
        svgpath.Line(10+0j, 10+10j),
        svgpath.Line(10+10j, 0+10j),
        svgpath.Line(0+10j, 0+0j)
    )
    
    panel_svg_path_dict = {"front_panel": [panel_path]}
    stitch_dict = {0: {"panel_0": "front_panel", "edge_0": 0, "panel_1": "front_panel", "edge_1": 2, "stitch_direction": True}}
    sewing_pattern = SewingPattern(panel_svg_path_dict, stitch_dict)
    
    # Turn off interactive mode
    plt.ioff()
    
    # Use save_figure method
    fig = sewing_pattern.save_figure('sewing_pattern_save.png', dpi=300)
    
    # Close the figure
    plt.close(fig)
    
    # Turn interactive mode back on
    plt.ion()
    
    return fig

def solution_6_modify_make_thumbnail():
    """Solution 6: Modify your make_thumbnail function"""
    print("\nSolution 6: Modified make_thumbnail function")
    print("-" * 50)
    
    def make_thumbnail_fixed(
        scene,
        FIG_UNIT_W=10,
        FIG_UNIT_H=10,
        NROWs=3,
        NCOLs=4,
        save_path=None,
        show=False,
    ):
        # Turn off interactive mode
        plt.ioff()
        
        fig, axs = plt.subplots(NROWs, NCOLs, figsize=(FIG_UNIT_W * NCOLs, FIG_UNIT_H * NROWs))
        
        # Your existing code here...
        # (simplified for demonstration)
        for i in range(min(NROWs * NCOLs, 10)):
            row_idx = i // NCOLs
            col_idx = i % NCOLs
            axs[row_idx, col_idx].plot([1, 2, 3, 4], [1, 4, 2, 3])
            axs[row_idx, col_idx].set_title(f"Plot {i}")
        
        plt.tight_layout()
        
        if save_path is not None:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
            print(f"Figure saved to: {save_path}")
        
        if show:
            plt.show()
        else:
            # Close the figure to prevent display
            plt.close(fig)
        
        # Turn interactive mode back on
        plt.ion()
        
        return fig
    
    # Test the modified function
    fig = make_thumbnail_fixed(None, save_path='thumbnail_test.png', show=False)
    print("Thumbnail saved without displaying")
    
    return fig

if __name__ == "__main__":
    print("Jupyter Notebook Display Fix Examples")
    print("=" * 60)
    
    # Run all solutions
    solution_1_turn_off_interactive()
    solution_2_close_figure()
    solution_3_use_context_manager()
    solution_4_for_sewing_pattern()
    solution_5_use_save_figure_method()
    solution_6_modify_make_thumbnail()
    
    print("\nAll solutions completed!")
    print("\nRecommended approach for your notebook:")
    print("1. Use plt.ioff() before creating figures")
    print("2. Use plt.close(fig) after saving")
    print("3. Use plt.ion() to restore interactive mode")


