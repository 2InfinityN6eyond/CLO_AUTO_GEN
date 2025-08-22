#!/usr/bin/env python3
"""
Integration example showing how to use the neural network ParameterizedLineApproximator
with your existing SeamLine data structure from the notebook.
"""

import numpy as np
import matplotlib.pyplot as plt
from parameterized_line_approximator import ParameterizedLineApproximator

def integrate_with_seam_line_data(seam_line):
    """
    Integrate the neural network approximator with your existing SeamLine data
    
    Args:
        seam_line: A SeamLine object from your notebook with segment_t_arr_list, 
                  segment_u_arr_list, segment_v_arr_list
    """
    
    print(f"Processing seam line with {len(seam_line.segment_t_arr_list)} segments")
    
    approximators = []
    
    for segment_idx in range(len(seam_line.segment_t_arr_list)):
        print(f"\n--- Processing Segment {segment_idx} ---")
        
        # Extract data for this segment
        t_arr = seam_line.segment_t_arr_list[segment_idx]
        u_arr = seam_line.segment_u_arr_list[segment_idx]
        v_arr = seam_line.segment_v_arr_list[segment_idx]
        
        print(f"Segment {segment_idx} data shape: t={t_arr.shape}, u={u_arr.shape}, v={v_arr.shape}")
        print(f"t range: [{t_arr.min():.3f}, {t_arr.max():.3f}]")
        print(f"u range: [{u_arr.min():.3f}, {u_arr.max():.3f}]")
        print(f"v range: [{v_arr.min():.3f}, {v_arr.max():.3f}]")
        
        # Create approximator for this segment
        approximator = ParameterizedLineApproximator(
            t_arr=t_arr,
            u_arr=u_arr,
            v_arr=v_arr,
            hidden_size=32,      # Smaller network for individual segments
            num_layers=2,        # Fewer layers for faster training
            learning_rate=0.01,  # Slightly higher learning rate
            epochs=300           # Fewer epochs for faster training
        )
        
        # Fit the model
        print(f"Training neural network for segment {segment_idx}...")
        losses = approximator.fit()
        
        # Evaluate the model
        metrics = approximator.evaluate()
        
        # Store the approximator
        approximators.append(approximator)
        
        print(f"Segment {segment_idx} training completed!")
    
    return approximators

def predict_smooth_curves(approximators, seam_line, num_points_per_segment=100):
    """
    Generate smooth curves for all segments using the fitted approximators
    
    Args:
        approximators: List of fitted ParameterizedLineApproximator objects
        seam_line: Original SeamLine object
        num_points_per_segment: Number of points to generate per segment
    
    Returns:
        List of smooth curve data for each segment
    """
    
    smooth_curves = []
    
    for segment_idx, approximator in enumerate(approximators):
        # Get original t range for this segment
        t_orig = seam_line.segment_t_arr_list[segment_idx]
        t_min, t_max = t_orig.min(), t_orig.max()
        
        # Generate smooth t values
        t_smooth = np.linspace(t_min, t_max, num_points_per_segment)
        
        # Predict smooth u, v values
        u_smooth, v_smooth = approximator.predict(t_smooth)
        
        smooth_curves.append({
            'segment_idx': segment_idx,
            't': t_smooth,
            'u': u_smooth,
            'v': v_smooth,
            'approximator': approximator
        })
        
        print(f"Generated smooth curve for segment {segment_idx} with {len(t_smooth)} points")
    
    return smooth_curves

def visualize_seam_line_approximation(seam_line, smooth_curves):
    """
    Visualize the original seam line data and the smooth approximations
    
    Args:
        seam_line: Original SeamLine object
        smooth_curves: List of smooth curve data from predict_smooth_curves
    """
    
    # Create color map for segments
    colors = plt.cm.rainbow(np.linspace(0, 1, len(seam_line.segment_t_arr_list)))
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Plot 1: Original data - u vs t
    for segment_idx in range(len(seam_line.segment_t_arr_list)):
        t_orig = seam_line.segment_t_arr_list[segment_idx]
        u_orig = seam_line.segment_u_arr_list[segment_idx]
        ax1.scatter(t_orig, u_orig, alpha=0.6, color=colors[segment_idx], 
                   label=f'Segment {segment_idx} (Original)')
    ax1.set_xlabel('t')
    ax1.set_ylabel('u')
    ax1.set_title('Original Data: U vs T')
    ax1.legend()
    ax1.grid(True)
    
    # Plot 2: Original data - v vs t
    for segment_idx in range(len(seam_line.segment_t_arr_list)):
        t_orig = seam_line.segment_t_arr_list[segment_idx]
        v_orig = seam_line.segment_v_arr_list[segment_idx]
        ax2.scatter(t_orig, v_orig, alpha=0.6, color=colors[segment_idx], 
                   label=f'Segment {segment_idx} (Original)')
    ax2.set_xlabel('t')
    ax2.set_ylabel('v')
    ax2.set_title('Original Data: V vs T')
    ax2.legend()
    ax2.grid(True)
    
    # Plot 3: Smooth approximations - u vs t
    for curve_data in smooth_curves:
        segment_idx = curve_data['segment_idx']
        ax3.plot(curve_data['t'], curve_data['u'], '-', linewidth=2, 
                color=colors[segment_idx], label=f'Segment {segment_idx} (Smooth)')
    ax3.set_xlabel('t')
    ax3.set_ylabel('u')
    ax3.set_title('Smooth Approximations: U vs T')
    ax3.legend()
    ax3.grid(True)
    
    # Plot 4: Smooth approximations - v vs t
    for curve_data in smooth_curves:
        segment_idx = curve_data['segment_idx']
        ax4.plot(curve_data['t'], curve_data['v'], '-', linewidth=2, 
                color=colors[segment_idx], label=f'Segment {segment_idx} (Smooth)')
    ax4.set_xlabel('t')
    ax4.set_ylabel('v')
    ax4.set_title('Smooth Approximations: V vs T')
    ax4.legend()
    ax4.grid(True)
    
    plt.tight_layout()
    plt.show()
    
    # Parametric plot: u vs v
    plt.figure(figsize=(12, 10))
    
    # Plot original data
    for segment_idx in range(len(seam_line.segment_t_arr_list)):
        u_orig = seam_line.segment_u_arr_list[segment_idx]
        v_orig = seam_line.segment_v_arr_list[segment_idx]
        plt.scatter(u_orig, v_orig, alpha=0.6, color=colors[segment_idx], 
                   label=f'Segment {segment_idx} (Original)')
    
    # Plot smooth curves
    for curve_data in smooth_curves:
        segment_idx = curve_data['segment_idx']
        plt.plot(curve_data['u'], curve_data['v'], '-', linewidth=2, 
                color=colors[segment_idx], label=f'Segment {segment_idx} (Smooth)')
    
    plt.xlabel('u')
    plt.ylabel('v')
    plt.title('Parametric Plot: V vs U (Original + Smooth Approximations)')
    plt.legend()
    plt.grid(True)
    plt.axis('equal')
    plt.show()

def example_usage_with_mock_data():
    """
    Example usage with mock data that mimics your SeamLine structure
    """
    
    # Create mock SeamLine data structure
    class MockSeamLine:
        def __init__(self):
            # Create some sample parametric curves
            np.random.seed(42)
            
            # Segment 0: Circle-like curve
            t0 = np.linspace(0, 2*np.pi, 50)
            u0 = np.cos(t0) + 0.05 * np.random.randn(50)
            v0 = np.sin(t0) + 0.05 * np.random.randn(50)
            
            # Segment 1: Spiral-like curve
            t1 = np.linspace(0, 3*np.pi, 60)
            u1 = t1 * np.cos(t1) + 0.1 * np.random.randn(60)
            v1 = t1 * np.sin(t1) + 0.1 * np.random.randn(60)
            
            # Segment 2: Figure-8 curve
            t2 = np.linspace(0, 2*np.pi, 40)
            u2 = np.sin(t2) + 0.05 * np.random.randn(40)
            v2 = np.sin(t2) * np.cos(t2) + 0.05 * np.random.randn(40)
            
            self.segment_t_arr_list = [t0, t1, t2]
            self.segment_u_arr_list = [u0, u1, u2]
            self.segment_v_arr_list = [v0, v1, v2]
    
    # Create mock seam line
    mock_seam_line = MockSeamLine()
    
    print("="*60)
    print("NEURAL NETWORK SEAM LINE APPROXIMATION")
    print("="*60)
    
    # Integrate with the mock data
    approximators = integrate_with_seam_line_data(mock_seam_line)
    
    # Generate smooth curves
    smooth_curves = predict_smooth_curves(approximators, mock_seam_line)
    
    # Visualize results
    visualize_seam_line_approximation(mock_seam_line, smooth_curves)
    
    # Example of how to use the fitted models for new predictions
    print("\n" + "="*60)
    print("EXAMPLE: MAKING NEW PREDICTIONS")
    print("="*60)
    
    for segment_idx, approximator in enumerate(approximators):
        # Get the original t range
        t_orig = mock_seam_line.segment_t_arr_list[segment_idx]
        t_min, t_max = t_orig.min(), t_orig.max()
        
        # Predict at some new t values
        t_new = np.array([t_min + 0.5, t_min + 1.0, t_max - 1.0, t_max - 0.5])
        u_new, v_new = approximator.predict(t_new)
        
        print(f"\nSegment {segment_idx} predictions:")
        for i, t_val in enumerate(t_new):
            print(f"  t={t_val:.3f} -> u={u_new[i]:.3f}, v={v_new[i]:.3f}")

if __name__ == "__main__":
    example_usage_with_mock_data()
