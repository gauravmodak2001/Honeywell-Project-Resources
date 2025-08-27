"""
Visualization functions for thermal data.
"""

import matplotlib.pyplot as plt
import numpy as np

def visualize_thermal_data(data, cmap='viridis', show_original=False, original_data=None, title=None):
    """
    Visualize thermal data.
    
    Args:
        data (numpy.ndarray): Thermal data to visualize
        cmap (str): Colormap to use
        show_original (bool): Whether to show original data for comparison
        original_data (numpy.ndarray): Original data to compare with
        title (str): Title for the plot
        
    Returns:
        matplotlib.figure.Figure: The created figure
    """
    if show_original and original_data is not None:
        # Create a side-by-side comparison
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        im1 = axes[0].imshow(original_data, cmap=cmap)
        axes[0].set_title(f'Original ({original_data.shape[0]}×{original_data.shape[1]})')
        plt.colorbar(im1, ax=axes[0], label='Temperature (°C)')
        
        im2 = axes[1].imshow(data, cmap=cmap)
        axes[1].set_title(f'Processed ({data.shape[0]}×{data.shape[1]})')
        plt.colorbar(im2, ax=axes[1], label='Temperature (°C)')
    else:
        # Just show the current data
        fig = plt.figure(figsize=(10, 8))
        im = plt.imshow(data, cmap=cmap)
        plt.colorbar(im, label='Temperature (°C)')
        plt.title(title or f'Thermal Image ({data.shape[0]}×{data.shape[1]})')
    
    plt.tight_layout()
    plt.show()
    
    return fig

def plot_temperature_histogram(data, bins=50, title='Temperature Distribution'):
    """
    Plot a histogram of temperature values.
    
    Args:
        data (numpy.ndarray): Thermal data
        bins (int): Number of histogram bins
        title (str): Title for the plot
        
    Returns:
        matplotlib.figure.Figure: The created figure
    """
    fig = plt.figure(figsize=(10, 6))
    plt.hist(data.flatten(), bins=bins)
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Frequency')
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    return fig

def plot_temperature_profile(data, axis=0, position=None, title=None):
    """
    Plot a temperature profile along a line.
    
    Args:
        data (numpy.ndarray): Thermal data
        axis (int): Axis along which to plot (0 for horizontal, 1 for vertical)
        position (int): Position along the other axis (defaults to middle)
        title (str): Title for the plot
        
    Returns:
        matplotlib.figure.Figure: The created figure
    """
    if position is None:
        # Default to middle
        position = data.shape[1-axis] // 2
    
    if axis == 0:
        # Horizontal profile
        profile = data[position, :]
        x_label = 'Column'
        profile_type = 'Horizontal'
        pos_label = f'Row {position}'
    else:
        # Vertical profile
        profile = data[:, position]
        x_label = 'Row'
        profile_type = 'Vertical'
        pos_label = f'Column {position}'
    
    fig = plt.figure(figsize=(12, 6))
    plt.plot(profile)
    plt.xlabel(x_label)
    plt.ylabel('Temperature (°C)')
    plt.title(title or f'{profile_type} Temperature Profile at {pos_label}')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    return fig