#!/usr/bin/env python3
"""
Examples showing how to control figure display and save figures
with the modified SewingPattern class.
"""

import matplotlib.pyplot as plt
import numpy as np
from sewing_pattern import SewingPattern
import svgpathtools as svgpath

def create_simple_sewing_pattern():
    """Create a simple sewing pattern for testing."""
    # Create a simple rectangular panel
    panel_path = svgpath.Path(
        svgpath.Line(0+0j, 10+0j),      # Bottom edge
        svgpath.Line(10+0j, 10+10j),    # Right edge  
        svgpath.Line(10+10j, 0+10j),    # Top edge
        svgpath.Line(0+10j, 0+0j)       # Left edge
    )
    
    panel_svg_path_dict = {
        "front_panel": [panel_path]
    }
    
    # Create a simple stitch (self-stitch for demonstration)
    stitch_dict = {
        0: {
            "panel_0": "front_panel",
            "edge_0": 0,
            "panel_1": "front_panel", 
            "edge_1": 2,
            "stitch_direction": True
        }
    }
    
    return SewingPattern(panel_svg_path_dict, stitch_dict)

def example_1_no_display():
    """Example 1: Draw without displaying the figure."""
    print("Example 1: Draw without displaying the figure")
    print("-" * 50)
    
    sewing_pattern = create_simple_sewing_pattern()
    
    # Draw without showing (no figure will appear)
    fig, axs = sewing_pattern.draw(show=False)
    
    print("Figure created but not displayed")
    print("You can now save it or modify it further")
    
    return fig, axs

def example_2_save_figure():
    """Example 2: Save figure to file."""
    print("\nExample 2: Save figure to file")
    print("-" * 50)
    
    sewing_pattern = create_simple_sewing_pattern()
    
    # Method 1: Use the new save_figure method
    fig = sewing_pattern.save_figure('sewing_pattern.png', dpi=300)
    
    # Method 2: Manual save after drawing
    fig, axs = sewing_pattern.draw(show=False)
    fig.savefig('sewing_pattern_manual.png', dpi=300, bbox_inches='tight')
    print("Figure saved manually to: sewing_pattern_manual.png")
    
    return fig, axs

def example_3_control_display():
    """Example 3: Control when and how the figure is displayed."""
    print("\nExample 3: Control figure display")
    print("-" * 50)
    
    sewing_pattern = create_simple_sewing_pattern()
    
    # Option 1: Show with blocking (waits for user to close)
    print("Showing figure with blocking (close window to continue)...")
    fig, axs = sewing_pattern.draw(show=True, block=True)
    
    # Option 2: Show without blocking (continues immediately)
    print("Showing figure without blocking (continues immediately)...")
    fig, axs = sewing_pattern.draw(show=True, block=False)
    
    # Option 3: Don't show at all
    print("Drawing without showing...")
    fig, axs = sewing_pattern.draw(show=False)
    
    return fig, axs

def example_4_multiple_formats():
    """Example 4: Save in multiple formats."""
    print("\nExample 4: Save in multiple formats")
    print("-" * 50)
    
    sewing_pattern = create_simple_sewing_pattern()
    
    # Save in different formats
    formats = ['png', 'pdf', 'svg', 'jpg']
    
    for fmt in formats:
        filename = f'sewing_pattern.{fmt}'
        sewing_pattern.save_figure(filename, dpi=300)
    
    print("Saved in all formats!")

def example_5_custom_figure():
    """Example 5: Create custom figure and save."""
    print("\nExample 5: Custom figure and save")
    print("-" * 50)
    
    sewing_pattern = create_simple_sewing_pattern()
    
    # Create custom figure
    fig, axs = plt.subplots(1, 2, figsize=(15, 6))
    
    # Draw sewing pattern on first subplot
    sewing_pattern.draw_on_axes(axs[0])
    axs[0].set_title("Sewing Pattern")
    
    # Add something else on second subplot
    axs[1].plot([1, 2, 3, 4], [1, 4, 2, 3])
    axs[1].set_title("Some other plot")
    
    # Save the custom figure
    fig.savefig('custom_figure.png', dpi=300, bbox_inches='tight')
    print("Custom figure saved to: custom_figure.png")
    
    return fig, axs

def example_6_your_use_case():
    """Example 6: Your specific use case from the notebook."""
    print("\nExample 6: Your notebook use case")
    print("-" * 50)
    
    # Simulate your notebook scenario
    sewing_pattern = create_simple_sewing_pattern()
    
    # Your original code (this would show the figure):
    # data = sewing_pattern.draw(show=True)
    
    # Better approach - control the display:
    print("Drawing without showing...")
    fig, axs = sewing_pattern.draw(show=False)
    
    # Now you can save it:
    fig.savefig('notebook_pattern.png', dpi=300, bbox_inches='tight')
    print("Saved to: notebook_pattern.png")
    
    # Or show it when you want:
    print("Showing figure...")
    plt.show()
    
    return fig, axs

def example_7_jupyter_notebook_tips():
    """Example 7: Tips for Jupyter notebook usage."""
    print("\nExample 7: Jupyter notebook tips")
    print("-" * 50)
    
    sewing_pattern = create_simple_sewing_pattern()
    
    # In Jupyter, you might want to use:
    # %matplotlib inline  # For inline plots
    # %matplotlib notebook  # For interactive plots
    
    # For saving without showing:
    fig, axs = sewing_pattern.draw(show=False)
    fig.savefig('jupyter_pattern.png', dpi=300, bbox_inches='tight')
    
    # For inline display in Jupyter:
    # fig, axs = sewing_pattern.draw(show=False)
    # plt.show()  # This will display inline in Jupyter
    
    print("Figure saved for Jupyter notebook usage")

if __name__ == "__main__":
    print("SewingPattern Figure Control Examples")
    print("=" * 60)
    
    # Run examples
    example_1_no_display()
    example_2_save_figure()
    example_3_control_display()
    example_4_multiple_formats()
    example_5_custom_figure()
    example_6_your_use_case()
    example_7_jupyter_notebook_tips()
    
    print("\nAll examples completed!")
    print("\nKey points:")
    print("1. Use show=False to prevent automatic display")
    print("2. Use save_figure() method for easy saving")
    print("3. Use block=False to show without blocking execution")
    print("4. You can save in multiple formats (png, pdf, svg, jpg)")

