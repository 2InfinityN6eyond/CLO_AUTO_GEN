# Neural Network ParameterizedLineApproximator

This implementation provides a neural network-based approach to fit parametric curves where `u_arr` and `v_arr` are dependent on `t_arr`.

## Overview

The `ParameterizedLineApproximator` class uses a feedforward neural network to learn the relationship between:
- **Input**: `t_arr` (1D array of parameter values)
- **Output**: `u_arr` and `v_arr` (1D arrays of dependent variables)

## Files

1. **`parameterized_line_approximator.py`** - Main implementation with the neural network class
2. **`test_parameterized_approximator.py`** - Test script with examples and comparisons
3. **`integration_example.py`** - Integration example with your existing SeamLine data structure
4. **`README_neural_network_approximator.md`** - This documentation

## Requirements

```bash
pip install torch numpy matplotlib
```

## Basic Usage

### Simple Example

```python
import numpy as np
from parameterized_line_approximator import ParameterizedLineApproximator

# Your data
t_arr = np.linspace(0, 2*np.pi, 100)
u_arr = np.sin(t_arr) + 0.1 * np.random.randn(100)
v_arr = np.cos(t_arr) + 0.1 * np.random.randn(100)

# Create and fit the model
approximator = ParameterizedLineApproximator(
    t_arr=t_arr,
    u_arr=u_arr,
    v_arr=v_arr,
    hidden_size=64,      # Number of neurons in hidden layers
    num_layers=3,        # Number of hidden layers
    learning_rate=0.001, # Learning rate
    epochs=1000          # Number of training epochs
)

# Fit the model
losses = approximator.fit()

# Make predictions
t_new = np.linspace(0, 2*np.pi, 50)
u_pred, v_pred = approximator.predict(t_new)

# Evaluate the model
metrics = approximator.evaluate()

# Visualize results
approximator.visualize_fit()
```

### Integration with Your SeamLine Data

```python
from integration_example import integrate_with_seam_line_data, predict_smooth_curves

# Assuming you have a seam_line object from your notebook
# seam_line has: segment_t_arr_list, segment_u_arr_list, segment_v_arr_list

# Fit neural networks for all segments
approximators = integrate_with_seam_line_data(seam_line)

# Generate smooth curves
smooth_curves = predict_smooth_curves(approximators, seam_line)

# Use the fitted models for predictions
for segment_idx, approximator in enumerate(approximators):
    t_orig = seam_line.segment_t_arr_list[segment_idx]
    t_min, t_max = t_orig.min(), t_orig.max()
    
    # Predict at new t values
    t_new = np.linspace(t_min, t_max, 100)
    u_new, v_new = approximator.predict(t_new)
```

## Class Methods

### `__init__(t_arr, u_arr, v_arr, hidden_size=64, num_layers=3, learning_rate=0.001, epochs=1000)`

Initialize the approximator with your data and hyperparameters.

**Parameters:**
- `t_arr`: 1D numpy array of parameter values
- `u_arr`: 1D numpy array of u values (dependent on t)
- `v_arr`: 1D numpy array of v values (dependent on t)
- `hidden_size`: Number of neurons in each hidden layer
- `num_layers`: Number of hidden layers
- `learning_rate`: Learning rate for Adam optimizer
- `epochs`: Number of training epochs

### `fit()`

Train the neural network on your data. Returns training loss history.

### `predict(t_arr)`

Predict u and v values for given t values.

**Parameters:**
- `t_arr`: 1D numpy array or list of t values

**Returns:**
- `u_pred`: Predicted u values
- `v_pred`: Predicted v values

### `evaluate()`

Evaluate the model on training data. Returns MSE and R² scores.

### `visualize_fit(num_points=1000)`

Create plots showing the original data and fitted curves.

### `get_model_summary()`

Print information about the neural network architecture.

## Hyperparameter Tuning

### For Simple Curves
```python
approximator = ParameterizedLineApproximator(
    hidden_size=32,
    num_layers=2,
    learning_rate=0.01,
    epochs=500
)
```

### For Complex Curves
```python
approximator = ParameterizedLineApproximator(
    hidden_size=128,
    num_layers=4,
    learning_rate=0.001,
    epochs=2000
)
```

### For Individual Segments (from your SeamLine data)
```python
approximator = ParameterizedLineApproximator(
    hidden_size=32,
    num_layers=2,
    learning_rate=0.01,
    epochs=300
)
```

## Advantages over Traditional Methods

1. **Non-linear Relationships**: Can capture complex non-linear relationships between t and u/v
2. **Smooth Interpolation**: Provides smooth curves between data points
3. **Robust to Noise**: Handles noisy data better than polynomial fitting
4. **Flexible Architecture**: Adjustable network size for different complexity levels
5. **Continuous Output**: Can predict at any t value within the training range

## Comparison with Polynomial Fitting

The test script includes a comparison with polynomial fitting:

```python
from test_parameterized_approximator import compare_with_polynomial_fit
compare_with_polynomial_fit()
```

## Integration with Your Notebook

To integrate with your existing `make_residual.ipynb`:

1. **Import the class:**
```python
from parameterized_line_approximator import ParameterizedLineApproximator
```

2. **Use with your SeamLine data:**
```python
# For each segment in your seam line
for segment_idx in range(len(seam_line.segment_t_arr_list)):
    t_arr = seam_line.segment_t_arr_list[segment_idx]
    u_arr = seam_line.segment_u_arr_list[segment_idx]
    v_arr = seam_line.segment_v_arr_list[segment_idx]
    
    approximator = ParameterizedLineApproximator(t_arr, u_arr, v_arr)
    approximator.fit()
    
    # Now you can predict smooth curves
    t_smooth = np.linspace(t_arr.min(), t_arr.max(), 100)
    u_smooth, v_smooth = approximator.predict(t_smooth)
```

## Troubleshooting

### Training Issues
- **High Loss**: Try increasing `hidden_size` or `num_layers`
- **Slow Training**: Reduce `epochs` or increase `learning_rate`
- **Overfitting**: Reduce `hidden_size` or `num_layers`

### Memory Issues
- **Large Datasets**: Reduce `hidden_size` or use smaller batch sizes
- **Many Segments**: Process segments one at a time

### Prediction Issues
- **Out of Range**: Ensure prediction t values are within training range
- **Poor Quality**: Retrain with more epochs or adjust hyperparameters

## Example Output

The neural network will provide:
- Training progress updates
- Loss plots
- Evaluation metrics (MSE, R²)
- Visualization of original data vs fitted curves
- Parametric plots showing the relationship between u and v

## Performance Tips

1. **Start Small**: Begin with smaller networks and increase complexity as needed
2. **Monitor Loss**: Watch the training loss to ensure convergence
3. **Validate**: Use the `evaluate()` method to check model performance
4. **Visualize**: Always plot results to verify the fit looks reasonable
5. **Save Models**: Consider saving fitted models for reuse (not implemented in this version)
