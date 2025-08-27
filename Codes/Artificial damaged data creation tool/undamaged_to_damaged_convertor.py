# use lableimgenv  environment

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.patches import Polygon
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os

class ThermalImageEditor:
    def __init__(self):
        self.data = None
        self.original_data = None
        self.fig = None
        self.ax = None
        self.im = None
        self.points = []
        self.drawing = False
        self.polygon = None
        self.current_selection = None
        
    def load_csv(self, filepath=None):
        """Load thermal image CSV file"""
        try:
            if filepath is None:
                # Use file dialog to select CSV
                root = tk.Tk()
                root.withdraw()
                filepath = filedialog.askopenfilename(
                    title="Select Thermal Image CSV",
                    filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
                )
                root.destroy()
                
            if not filepath:
                return False
                
            # Load CSV without headers (pure temperature data)
            self.data = pd.read_csv(filepath, header=None).values
            self.original_data = self.data.copy()
            
            print(f"Loaded thermal image: {self.data.shape}")
            print(f"Temperature range: {self.data.min():.3f}°C to {self.data.max():.3f}°C")
            
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV file:\n{str(e)}")
            return False
    
    def setup_plot(self):
        """Setup the interactive matplotlib plot"""
        self.fig, self.ax = plt.subplots(figsize=(12, 10))
        
        # Display thermal image
        self.im = self.ax.imshow(self.data, cmap='hot', interpolation='nearest')
        self.ax.set_title('Thermal Image - Click to draw region, then specify fill temperature')
        
        # Add colorbar
        cbar = plt.colorbar(self.im, ax=self.ax)
        cbar.set_label('Temperature (°C)')
        
        # Add buttons
        ax_reset = plt.axes([0.02, 0.02, 0.1, 0.05])
        ax_fill = plt.axes([0.13, 0.02, 0.1, 0.05])
        ax_save = plt.axes([0.24, 0.02, 0.1, 0.05])
        ax_load = plt.axes([0.35, 0.02, 0.1, 0.05])
        ax_undo = plt.axes([0.46, 0.02, 0.1, 0.05])
        
        self.btn_reset = Button(ax_reset, 'Reset')
        self.btn_fill = Button(ax_fill, 'Fill Region')
        self.btn_save = Button(ax_save, 'Save CSV')
        self.btn_load = Button(ax_load, 'Load CSV')
        self.btn_undo = Button(ax_undo, 'Undo')
        
        # Connect button events
        self.btn_reset.on_clicked(self.reset_image)
        self.btn_fill.on_clicked(self.fill_region)
        self.btn_save.on_clicked(self.save_csv)
        self.btn_load.on_clicked(self.load_new_csv)
        self.btn_undo.on_clicked(self.undo_last_action)
        
        # Connect mouse events
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        
        # Instructions
        self.ax.text(0.02, 0.98, 
                    'Instructions:\n• Click points to draw region\n• Press ENTER to close region\n• Click "Fill Region" to specify temperature\n• ESC to cancel current selection',
                    transform=self.ax.transAxes, 
                    verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
                    fontsize=9)
        
        plt.tight_layout()
        
    def on_click(self, event):
        """Handle mouse clicks for drawing regions"""
        if event.inaxes != self.ax:
            return
            
        if event.button == 1:  # Left click
            x, y = int(event.xdata), int(event.ydata)
            
            # Check bounds
            if 0 <= x < self.data.shape[1] and 0 <= y < self.data.shape[0]:
                self.points.append([x, y])
                
                # Plot the point
                self.ax.plot(x, y, 'ro', markersize=5)
                
                # Draw lines between points
                if len(self.points) > 1:
                    self.ax.plot([self.points[-2][0], self.points[-1][0]], 
                               [self.points[-2][1], self.points[-1][1]], 'r-', linewidth=2)
                
                self.fig.canvas.draw()
                print(f"Point added: ({x}, {y})")
    
    def on_key_press(self, event):
        """Handle keyboard events"""
        if event.key == 'enter' and len(self.points) >= 3:
            self.close_region()
        elif event.key == 'escape':
            self.cancel_selection()
    
    def close_region(self):
        """Close the current region and create polygon"""
        if len(self.points) < 3:
            messagebox.showwarning("Warning", "Need at least 3 points to create a region")
            return
        
        # Close the polygon by connecting last point to first
        self.ax.plot([self.points[-1][0], self.points[0][0]], 
                    [self.points[-1][1], self.points[0][1]], 'r-', linewidth=2)
        
        # Create polygon patch
        if self.polygon:
            self.polygon.remove()
        
        self.polygon = Polygon(self.points, closed=True, fill=False, 
                             edgecolor='red', linewidth=2, linestyle='--')
        self.ax.add_patch(self.polygon)
        
        self.current_selection = self.points.copy()
        self.fig.canvas.draw()
        
        print(f"Region closed with {len(self.points)} points")
        print("Press 'Fill Region' button to specify fill temperature")
    
    def cancel_selection(self):
        """Cancel current selection"""
        self.points = []
        if self.polygon:
            self.polygon.remove()
            self.polygon = None
        self.current_selection = None
        
        # Redraw without selection
        self.refresh_display()
        print("Selection cancelled")
    
    def fill_region(self, event=None):
        """Fill selected region with user-specified temperature"""
        if not self.current_selection:
            messagebox.showwarning("Warning", "Please select a region first")
            return
        
        try:
            # Create mask for the selected region
            mask = self.create_polygon_mask(self.current_selection)
            
            if not np.any(mask):
                messagebox.showwarning("Warning", "Selected region is empty")
                return
            
            # Calculate current average temperature in the region for reference
            region_temps = self.data[mask]
            current_avg = np.mean(region_temps)
            current_min = np.min(region_temps)
            current_max = np.max(region_temps)
            
            # Ask user for fill value
            root = tk.Tk()
            root.withdraw()
            
            fill_value = tk.simpledialog.askfloat(
                "Fill Temperature", 
                f"Enter temperature value (°C) to fill the region:\n\n"
                f"Current region stats:\n"
                f"• Average: {current_avg:.3f}°C\n"
                f"• Range: {current_min:.3f}°C to {current_max:.3f}°C\n"
                f"• Pixels: {np.sum(mask)} pixels\n\n"
                f"Overall image range: {self.data.min():.3f}°C to {self.data.max():.3f}°C",
                minvalue=0.0,
                maxvalue=100.0
            )
            root.destroy()
            
            if fill_value is None:
                print("Fill operation cancelled by user")
                return
            
            # Fill the region with user-specified temperature
            self.data[mask] = fill_value
            
            # Update display
            self.refresh_display()
            
            print(f"Filled region with temperature: {fill_value:.3f}°C")
            print(f"Modified {np.sum(mask)} pixels")
            print(f"Previous average was: {current_avg:.3f}°C")
            
            # Clear selection
            self.cancel_selection()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fill region:\n{str(e)}")
    
    def create_polygon_mask(self, points):
        """Create a boolean mask for the polygon region"""
        from matplotlib.path import Path
        
        # Create path from points
        path = Path(points)
        
        # Create coordinate grids
        y_coords, x_coords = np.mgrid[0:self.data.shape[0], 0:self.data.shape[1]]
        coords = np.column_stack((x_coords.ravel(), y_coords.ravel()))
        
        # Test which points are inside the polygon
        mask = path.contains_points(coords)
        mask = mask.reshape(self.data.shape)
        
        return mask
    
    def refresh_display(self):
        """Refresh the thermal image display"""
        self.im.set_array(self.data)
        self.im.set_clim(vmin=self.data.min(), vmax=self.data.max())
        
        # Clear any drawing artifacts
        for artist in self.ax.lines + self.ax.patches:
            if artist != self.polygon:  # Keep current polygon if exists
                artist.remove()
        
        self.fig.canvas.draw()
    
    def reset_image(self, event=None):
        """Reset image to original state"""
        if self.original_data is not None:
            self.data = self.original_data.copy()
            self.cancel_selection()
            self.refresh_display()
            print("Image reset to original state")
    
    def undo_last_action(self, event=None):
        """Undo last modification (simple reset for now)"""
        self.reset_image()
    
    def save_csv(self, event=None):
        """Save modified thermal image to CSV"""
        try:
            root = tk.Tk()
            root.withdraw()
            
            filepath = filedialog.asksaveasfilename(
                title="Save Modified Thermal Image",
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            root.destroy()
            
            if filepath:
                # Save without headers, matching original format
                pd.DataFrame(self.data).to_csv(filepath, header=False, index=False)
                print(f"Saved modified thermal image to: {filepath}")
                messagebox.showinfo("Success", f"File saved successfully:\n{filepath}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")
    
    def load_new_csv(self, event=None):
        """Load a new CSV file"""
        if self.load_csv():
            self.cancel_selection()
            self.refresh_display()
    
    def run(self, csv_path=None):
        """Run the thermal image editor"""
        # Load CSV file
        if csv_path:
            if not self.load_csv(csv_path):
                return
        else:
            if not self.load_csv():
                return
        
        # Setup and show plot
        self.setup_plot()
        plt.show()

# Usage example and main execution
if __name__ == "__main__":
    # Create and run the thermal image editor
    editor = ThermalImageEditor()
    
    # Option 1: Load specific file
    # editor.run("path/to/your/thermal_image.csv")
    
    # Option 2: Use file dialog to select file
    editor.run()
    
    print("\n=== Thermal Image Editor ===")
    print("Features:")
    print("• Interactive region selection by clicking points")
    print("• Press ENTER to close region")
    print("• Fill selected regions with custom temperature values")
    print("• Save modified thermal images")
    print("• Reset and undo functionality")
    print("• Real-time visualization with colormap")