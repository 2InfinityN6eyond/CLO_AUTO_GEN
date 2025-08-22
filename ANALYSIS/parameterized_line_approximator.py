import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
import matplotlib.pyplot as plt

class ParameterizedLineApproximator:
    def __init__(
        self,
        t_arr,
        u_arr,
        v_arr,
        hidden_size=64,
        num_layers=3,
        learning_rate=0.001,
        epochs=1000
    ):
        self.t_arr = t_arr
        self.u_arr = u_arr
        self.v_arr = v_arr
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.model = None
        self.is_fitted = False
        
    def _build_model(self):
        """Build a neural network model"""
        layers = []
        
        # Input layer
        layers.append(nn.Linear(1, self.hidden_size))
        layers.append(nn.ReLU())
        
        # Hidden layers
        for _ in range(self.num_layers - 1):
            layers.append(nn.Linear(self.hidden_size, self.hidden_size))
            layers.append(nn.ReLU())
        
        # Output layer (2 outputs: u and v)
        layers.append(nn.Linear(self.hidden_size, 2))
        
        return nn.Sequential(*layers)
    
    def fit(self):
        """Fit the neural network to the data"""
        # Convert numpy arrays to torch tensors
        t_tensor = torch.FloatTensor(self.t_arr.reshape(-1, 1))
        u_tensor = torch.FloatTensor(self.u_arr.reshape(-1, 1))
        v_tensor = torch.FloatTensor(self.v_arr.reshape(-1, 1))
        
        # Combine u and v into a single target tensor
        target_tensor = torch.cat([u_tensor, v_tensor], dim=1)
        
        # Create dataset and dataloader
        dataset = TensorDataset(t_tensor, target_tensor)
        dataloader = DataLoader(dataset, batch_size=min(32, len(self.t_arr)), shuffle=True)
        
        # Build model
        self.model = self._build_model()
        
        # Loss function and optimizer
        criterion = nn.MSELoss()
        optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)
        
        # Training loop
        self.model.train()
        losses = []
        for epoch in range(self.epochs):
            total_loss = 0
            for batch_t, batch_target in dataloader:
                optimizer.zero_grad()
                
                # Forward pass
                output = self.model(batch_t)
                loss = criterion(output, batch_target)
                
                # Backward pass
                loss.backward()
                optimizer.step()
                
                total_loss += loss.item()
            
            avg_loss = total_loss / len(dataloader)
            losses.append(avg_loss)
            
            # Print progress every 100 epochs
            if (epoch + 1) % 100 == 0:
                print(f"Epoch [{epoch+1}/{self.epochs}], Loss: {avg_loss:.6f}")
        
        self.is_fitted = True
        print("Training completed!")
        
        # Plot training loss
        plt.figure(figsize=(10, 6))
        plt.plot(losses)
        plt.title('Training Loss Over Time')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.yscale('log')
        plt.grid(True)
        plt.show()
        
        return losses
    
    def predict(self, t_arr):
        """Predict u and v values for given t values"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before making predictions")
        
        # Convert input to tensor
        if isinstance(t_arr, np.ndarray):
            t_tensor = torch.FloatTensor(t_arr.reshape(-1, 1))
        else:
            t_tensor = torch.FloatTensor(t_arr).reshape(-1, 1)
        
        # Make predictions
        self.model.eval()
        with torch.no_grad():
            output = self.model(t_tensor)
        
        # Convert back to numpy
        output_np = output.numpy()
        u_pred = output_np[:, 0]
        v_pred = output_np[:, 1]
        
        return u_pred, v_pred
    
    def evaluate(self):
        """Evaluate the model on training data"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before evaluation")
        
        u_pred, v_pred = self.predict(self.t_arr)
        
        # Calculate MSE
        u_mse = np.mean((self.u_arr - u_pred) ** 2)
        v_mse = np.mean((self.v_arr - v_pred) ** 2)
        
        # Calculate R² score
        u_r2 = 1 - np.sum((self.u_arr - u_pred) ** 2) / np.sum((self.u_arr - np.mean(self.u_arr)) ** 2)
        v_r2 = 1 - np.sum((self.v_arr - v_pred) ** 2) / np.sum((self.v_arr - np.mean(self.v_arr)) ** 2)
        
        print(f"Evaluation Results:")
        print(f"U - MSE: {u_mse:.6f}, R²: {u_r2:.6f}")
        print(f"V - MSE: {v_mse:.6f}, R²: {v_r2:.6f}")
        
        return {
            'u_mse': u_mse,
            'v_mse': v_mse,
            'u_r2': u_r2,
            'v_r2': v_r2
        }
    
    def visualize_fit(self, num_points=1000):
        """Visualize the fitted curve"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before visualization")
        
        # Generate smooth t values for visualization
        t_smooth = np.linspace(self.t_arr.min(), self.t_arr.max(), num_points)
        u_smooth, v_smooth = self.predict(t_smooth)
        
        # Plot original data and fitted curve
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Plot u vs t
        ax1.scatter(self.t_arr, self.u_arr, alpha=0.6, label='Original Data', color='blue')
        ax1.plot(t_smooth, u_smooth, 'r-', linewidth=2, label='Fitted Curve')
        ax1.set_xlabel('t')
        ax1.set_ylabel('u')
        ax1.set_title('U vs T')
        ax1.legend()
        ax1.grid(True)
        
        # Plot v vs t
        ax2.scatter(self.t_arr, self.v_arr, alpha=0.6, label='Original Data', color='green')
        ax2.plot(t_smooth, v_smooth, 'r-', linewidth=2, label='Fitted Curve')
        ax2.set_xlabel('t')
        ax2.set_ylabel('v')
        ax2.set_title('V vs T')
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        plt.show()
        
        # Plot u vs v (parametric plot)
        plt.figure(figsize=(10, 8))
        plt.scatter(self.u_arr, self.v_arr, alpha=0.6, label='Original Data', color='purple')
        plt.plot(u_smooth, v_smooth, 'r-', linewidth=2, label='Fitted Curve')
        plt.xlabel('u')
        plt.ylabel('v')
        plt.title('Parametric Plot: V vs U')
        plt.legend()
        plt.grid(True)
        plt.axis('equal')
        plt.show()
    
    def get_model_summary(self):
        """Get a summary of the model architecture"""
        if self.model is None:
            return "Model not built yet"
        
        total_params = sum(p.numel() for p in self.model.parameters())
        trainable_params = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
        
        return f"""
        Model Architecture:
        - Hidden size: {self.hidden_size}
        - Number of layers: {self.num_layers}
        - Total parameters: {total_params}
        - Trainable parameters: {trainable_params}
        - Input: 1 (t values)
        - Output: 2 (u, v values)
        """

# Example usage function
def example_usage():
    """Example of how to use the ParameterizedLineApproximator"""
    
    # Generate sample data (replace with your actual data)
    np.random.seed(42)
    t = np.linspace(0, 2*np.pi, 100)
    u = np.sin(t) + 0.1 * np.random.randn(100)  # u = sin(t) + noise
    v = np.cos(t) + 0.1 * np.random.randn(100)  # v = cos(t) + noise
    
    # Create and fit the model
    approximator = ParameterizedLineApproximator(
        t_arr=t,
        u_arr=u,
        v_arr=v,
        hidden_size=32,
        num_layers=2,
        learning_rate=0.01,
        epochs=500
    )
    
    # Fit the model
    losses = approximator.fit()
    
    # Evaluate the model
    metrics = approximator.evaluate()
    
    # Visualize the results
    approximator.visualize_fit()
    
    # Print model summary
    print(approximator.get_model_summary())
    
    # Make predictions on new data
    t_new = np.linspace(0, 2*np.pi, 50)
    u_pred, v_pred = approximator.predict(t_new)
    
    print(f"Predicted u values: {u_pred[:5]}...")
    print(f"Predicted v values: {v_pred[:5]}...")

if __name__ == "__main__":
    example_usage()
