#!/usr/bin/env python3
"""
Test script for the neural network-based ParameterizedLineApproximator
This shows how to use it with your existing data structure.
"""

import numpy as np
import matplotlib.pyplot as plt
from parameterized_line_approximator import ParameterizedLineApproximator

def test_with_sample_data():
    """Test the approximator with sample parametric curve data"""
    
    # Generate sample parametric curve data (replace with your actual t_arr, u_arr, v_arr)
    np.random.seed(42)
    
    # Create a parametric curve (e.g., a spiral)
    t = np.linspace(0, 4*np.pi, 200)
    u = t * np.cos(t) + 0.1 * np.random.randn(200)  # x-coordinate with noise
    v = t * np.sin(t) + 0.1 * np.random.randn(200)  # y-coordinate with noise
    
    print(f"Data shape: t={t.shape}, u={u.shape}, v={v.shape}")
    print(f"t range: [{t.min():.3f}, {t.max():.3f}]")
    print(f"u range: [{u.min():.3f}, {u.max():.3f}]")
    print(f"v range: [{v.min():.3f}, {v.max():.3f}]")
    
    # Create the approximator
    approximator = ParameterizedLineApproximator(
        t_arr=t,
        u_arr=u,
        v_arr=v,
        hidden_size=64,      # Number of neurons in hidden layers
        num_layers=3,        # Number of hidden layers
        learning_rate=0.001, # Learning rate
        epochs=1000          # Number of training epochs
    )
    
    # Print model summary before training
    print("\n" + "="*50)
    print("MODEL SUMMARY")
    print("="*50)
    print(approximator.get_model_summary())
    
    # Fit the model
    print("\n" + "="*50)
    print("TRAINING")
    print("="*50)
    losses = approximator.fit()
    
    # Evaluate the model
    print("\n" + "="*50)
    print("EVALUATION")
    print("="*50)
    metrics = approximator.evaluate()
    
    # Visualize the results
    print("\n" + "="*50)
    print("VISUALIZATION")
    print("="*50)
    approximator.visualize_fit()
    
    # Test predictions on new data
    print("\n" + "="*50)
    print("PREDICTION TEST")
    print("="*50)
    
    # Generate new t values for prediction
    t_new = np.linspace(0, 4*np.pi, 100)
    u_pred, v_pred = approximator.predict(t_new)
    
    print(f"Predicted {len(t_new)} new points")
    print(f"First 5 predictions:")
    for i in range(5):
        print(f"  t={t_new[i]:.3f} -> u={u_pred[i]:.3f}, v={v_pred[i]:.3f}")
    
    return approximator, metrics

def test_with_actual_seam_data():
    """Test with actual seam line data from your notebook structure"""
    
    # This is a placeholder - you would replace this with your actual data
    # from the SeamLine.segment_t_arr_list, segment_u_arr_list, segment_v_arr_list
    
    print("To test with actual seam data, you would:")
    print("1. Extract t_arr, u_arr, v_arr from your SeamLine objects")
    print("2. Pass them to the ParameterizedLineApproximator")
    print("3. Use the fitted model for predictions")
    
    # Example of how you might use it with your data:
    """
    # Assuming you have a seam_line object from your notebook
    for segment_idx in range(len(seam_line.segment_t_arr_list)):
        t_arr = seam_line.segment_t_arr_list[segment_idx]
        u_arr = seam_line.segment_u_arr_list[segment_idx]
        v_arr = seam_line.segment_v_arr_list[segment_idx]
        
        # Create approximator for this segment
        approximator = ParameterizedLineApproximator(
            t_arr=t_arr,
            u_arr=u_arr,
            v_arr=v_arr,
            hidden_size=32,
            num_layers=2,
            learning_rate=0.01,
            epochs=500
        )
        
        # Fit the model
        approximator.fit()
        
        # Now you can predict u, v for any t value
        t_new = np.linspace(t_arr.min(), t_arr.max(), 100)
        u_pred, v_pred = approximator.predict(t_new)
        
        print(f"Segment {segment_idx}: Fitted curve with {len(t_new)} points")
    """

def compare_with_polynomial_fit():
    """Compare neural network with polynomial fitting"""
    
    # Generate data
    np.random.seed(42)
    t = np.linspace(0, 2*np.pi, 100)
    u = np.sin(t) + 0.1 * np.random.randn(100)
    v = np.cos(t) + 0.1 * np.random.randn(100)
    
    # Neural network approach
    nn_approximator = ParameterizedLineApproximator(
        t_arr=t, u_arr=u, v_arr=v,
        hidden_size=32, num_layers=2,
        learning_rate=0.01, epochs=500
    )
    nn_approximator.fit()
    
    # Polynomial approach (for comparison)
    u_poly = np.polyfit(t, u, 5)  # 5th degree polynomial
    v_poly = np.polyfit(t, v, 5)
    
    # Test predictions
    t_test = np.linspace(0, 2*np.pi, 200)
    u_nn, v_nn = nn_approximator.predict(t_test)
    u_poly_pred = np.polyval(u_poly, t_test)
    v_poly_pred = np.polyval(v_poly, t_test)
    
    # Plot comparison
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    # U vs T comparison
    ax1.scatter(t, u, alpha=0.6, label='Original Data', color='blue')
    ax1.plot(t_test, u_nn, 'r-', linewidth=2, label='Neural Network')
    ax1.plot(t_test, u_poly_pred, 'g--', linewidth=2, label='Polynomial')
    ax1.set_xlabel('t')
    ax1.set_ylabel('u')
    ax1.set_title('U vs T - Comparison')
    ax1.legend()
    ax1.grid(True)
    
    # V vs T comparison
    ax2.scatter(t, v, alpha=0.6, label='Original Data', color='green')
    ax2.plot(t_test, v_nn, 'r-', linewidth=2, label='Neural Network')
    ax2.plot(t_test, v_poly_pred, 'g--', linewidth=2, label='Polynomial')
    ax2.set_xlabel('t')
    ax2.set_ylabel('v')
    ax2.set_title('V vs T - Comparison')
    ax2.legend()
    ax2.grid(True)
    
    # Parametric plot comparison
    ax3.scatter(u, v, alpha=0.6, label='Original Data', color='purple')
    ax3.plot(u_nn, v_nn, 'r-', linewidth=2, label='Neural Network')
    ax3.set_xlabel('u')
    ax3.set_ylabel('v')
    ax3.set_title('Parametric Plot - Neural Network')
    ax3.legend()
    ax3.grid(True)
    ax3.axis('equal')
    
    ax4.scatter(u, v, alpha=0.6, label='Original Data', color='purple')
    ax4.plot(u_poly_pred, v_poly_pred, 'g--', linewidth=2, label='Polynomial')
    ax4.set_xlabel('u')
    ax4.set_ylabel('v')
    ax4.set_title('Parametric Plot - Polynomial')
    ax4.legend()
    ax4.grid(True)
    ax4.axis('equal')
    
    plt.tight_layout()
    plt.show()
    
    # Calculate and print comparison metrics
    u_nn_mse = np.mean((u - nn_approximator.predict(t)[0]) ** 2)
    v_nn_mse = np.mean((v - nn_approximator.predict(t)[1]) ** 2)
    u_poly_mse = np.mean((u - np.polyval(u_poly, t)) ** 2)
    v_poly_mse = np.mean((v - np.polyval(v_poly, t)) ** 2)
    
    print("Comparison Results:")
    print(f"Neural Network - U MSE: {u_nn_mse:.6f}, V MSE: {v_nn_mse:.6f}")
    print(f"Polynomial     - U MSE: {u_poly_mse:.6f}, V MSE: {v_poly_mse:.6f}")

if __name__ == "__main__":
    print("Testing ParameterizedLineApproximator with sample data...")
    approximator, metrics = test_with_sample_data()
    
    print("\n" + "="*50)
    print("COMPARISON WITH POLYNOMIAL FITTING")
    print("="*50)
    compare_with_polynomial_fit()
    
    print("\n" + "="*50)
    print("ACTUAL SEAM DATA INTEGRATION")
    print("="*50)
    test_with_actual_seam_data()
