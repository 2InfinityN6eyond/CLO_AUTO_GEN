#!/usr/bin/env python3
"""
Test script to demonstrate the modified SewingPattern.draw() method
that can accept external matplotlib figures and axes.
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

def test_original_draw():
    """Test the original draw method (creates its own figure)."""
    print("Testing original draw method...")
    sewing_pattern = create_simple_sewing_pattern()
    sewing_pattern.draw(show=False)
    plt.title("Original draw method")
    plt.show()

def test_external_figure():
    """Test drawing on an external figure."""
    print("Testing external figure...")
    sewing_pattern = create_simple_sewing_pattern()
    
    # Create external figure
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    
    # Draw on the first subplot
    sewing_pattern.draw_on_axes(axs[0, 0])
    axs[0, 0].set_title("Sewing Pattern on Subplot (0,0)")
    
    # Draw on the second subplot
    sewing_pattern.draw_on_axes(axs[0, 1])
    axs[0, 1].set_title("Sewing Pattern on Subplot (0,1)")
    
    # Add some other content to other subplots
    axs[1, 0].plot([1, 2, 3, 4], [1, 4, 2, 3])
    axs[1, 0].set_title("Some other plot")
    
    axs[1, 1].scatter([1, 2, 3, 4], [1, 4, 2, 3])
    axs[1, 1].set_title("Some scatter plot")
    
    plt.tight_layout()
    plt.show()

def test_modified_draw_method():
    """Test the modified draw method with external figure/axes."""
    print("Testing modified draw method...")
    sewing_pattern = create_simple_sewing_pattern()
    
    # Create external figure
    fig, axs = plt.subplots(1, 2, figsize=(15, 6))
    
    # Use the modified draw method
    fig, axs = sewing_pattern.draw(fig=fig, axs=axs, show=False)
    axs[0].set_title("Sewing Pattern using modified draw()")
    
    # Add some other content to the second subplot
    axs[1].plot([1, 2, 3, 4], [1, 4, 2, 3])
    axs[1].set_title("Some other plot")
    
    plt.tight_layout()
    plt.show()

def test_your_use_case():
    """Test the specific use case from the notebook."""
    print("Testing your specific use case...")
    sewing_pattern = create_simple_sewing_pattern()
    
    # Create figure with subplots like in your notebook
    fig, axs = plt.subplots(4, 3, figsize=(30, 40))
    
    # Draw sewing pattern on the first row
    for idx in range(min(3, len(sewing_pattern.panel_dict))):
        sewing_pattern.draw_on_axes(axs[0, idx])
        axs[0, idx].set_title(f"Sewing Pattern {idx}")
        axs[0, idx].axis("off")
    
    # You can now add other content to the remaining subplots
    # For example, images, other plots, etc.
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Run all tests
    test_original_draw()
    test_external_figure()
    test_modified_draw_method()
    test_your_use_case()



