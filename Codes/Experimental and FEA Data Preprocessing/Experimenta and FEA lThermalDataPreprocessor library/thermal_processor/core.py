"""
Core functionality for thermal image processing.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import time
from .utils import ensure_directory_exists
from .visualization import visualize_thermal_data

class ThermalImageProcessor:
    """
    A class for processing thermal image CSV data with various operations.
    
    This class provides methods for loading, cropping, downsampling, and visualizing
    thermal image data stored in CSV format.
    """
    
    def __init__(self):
        """Initialize the ThermalImageProcessor."""
        self.data = None
        self.file_path = None
        self.processing_history = []
    
    def load_csv(self, file_path, skiprows=10, drop_first_column=True):
        """
        Load CSV file containing thermal data.
        
        Args:
            file_path (str): Path to the CSV file
            skiprows (int): Number of header rows to skip
            drop_first_column (bool): Whether to drop the first column
            
        Returns:
            self: For method chaining
        """
        self.file_path = Path(file_path)
        try:
            self.data = pd.read_csv(file_path, header=None, skiprows=skiprows)
            
            if drop_first_column:
                self.data = self.data.iloc[:, 1:]  # Drop first column
                
            self.processing_history.append(f"Loaded {file_path}")
            print(f"Loaded data shape: {self.data.shape}")
            
        except Exception as e:
            print(f"Error loading file {file_path}: {e}")
        
        return self
    
    def crop(self, start_row=0, end_row=None, start_col=0, end_col=None):
        """
        Crop the thermal data to the specified region.
        
        Args:
            start_row (int): Starting row index
            end_row (int): Ending row index (None for end of data)
            start_col (int): Starting column index
            end_col (int): Ending column index (None for end of data)
            
        Returns:
            self: For method chaining
        """
        if self.data is None:
            print("No data loaded. Please load data first.")
            return self
        
        try:
            # Handle None values for end indices
            if end_row is None:
                end_row = self.data.shape[0]
            if end_col is None:
                end_col = self.data.shape[1]
            
            original_shape = self.data.shape
            self.data = self.data.iloc[start_row:end_row, start_col:end_col]
            
            self.processing_history.append(
                f"Cropped from {original_shape} to {self.data.shape}"
            )
            print(f"Cropped data shape: {self.data.shape}")
            
        except Exception as e:
            print(f"Error cropping data: {e}")
        
        return self
    
    def downsample(self, output_size=(100, 100), method='nearest'):
        """
        Downsample the thermal data to the specified dimensions.
        
        Args:
            output_size (tuple): Target dimensions (height, width)
            method (str): Interpolation method ('nearest', 'linear', 'cubic')
            
        Returns:
            self: For method chaining
        """
        if self.data is None:
            print("No data loaded. Please load data first.")
            return self
        
        try:
            from skimage.transform import resize
            
            # Convert interpolation method to order parameter
            order_map = {'nearest': 0, 'linear': 1, 'cubic': 3}
            order = order_map.get(method.lower(), 0)
            
            original_shape = self.data.shape
            numpy_data = self.data.values
            
            # Perform downsampling
            downsampled_data = resize(
                numpy_data, 
                output_size, 
                order=order, 
                anti_aliasing=(order > 0),  # Only use anti-aliasing for non-nearest neighbor
                preserve_range=True
            )
            
            # Convert back to dataframe
            self.data = pd.DataFrame(downsampled_data)
            
            self.processing_history.append(
                f"Downsampled from {original_shape} to {self.data.shape} using {method}"
            )
            print(f"Downsampled data shape: {self.data.shape}")
            
        except Exception as e:
            print(f"Error downsampling data: {e}")
        
        return self
    
    def visualize(self, cmap='viridis', show_original=False, original_data=None):
        """
        Visualize the current thermal data.
        
        Args:
            cmap (str): Colormap to use
            show_original (bool): Whether to show original data for comparison
            original_data (DataFrame): Original data to compare with (if None, no comparison)
            
        Returns:
            self: For method chaining
        """
        if self.data is None:
            print("No data loaded. Please load data first.")
            return self
        
        try:
            visualize_thermal_data(
                self.data.values, 
                cmap=cmap, 
                show_original=show_original,
                original_data=original_data.values if original_data is not None else None
            )
            
            self.processing_history.append("Visualized data")
            
        except Exception as e:
            print(f"Error visualizing data: {e}")
        
        return self
    
    def save(self, output_file=None, suffix=None):
        """
        Save the processed thermal data to a CSV file.
        
        Args:
            output_file (str): Path to save the output file
            suffix (str): Suffix to append to the original filename
            
        Returns:
            str: Path to the saved file
        """
        if self.data is None:
            print("No data loaded. Please load data first.")
            return None
        
        try:
            if output_file is None:
                if suffix:
                    stem = self.file_path.stem
                    output_file = self.file_path.with_name(f"{stem}_{suffix}.csv")
                else:
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    output_file = self.file_path.with_name(f"{self.file_path.stem}_processed_{timestamp}.csv")
            
            self.data.to_csv(output_file, header=False, index=False)
            
            self.processing_history.append(f"Saved to {output_file}")
            print(f"Saved processed data to {output_file}")
            
            return str(output_file)
            
        except Exception as e:
            print(f"Error saving data: {e}")
            return None
    
    def get_processing_history(self):
        """
        Get the processing history for this thermal data.
        
        Returns:
            list: List of processing steps applied
        """
        return self.processing_history
    
    def batch_process(self, 
                      source_directory, 
                      destination_directory, 
                      crop_params=None,
                      downsample_params=None,
                      file_pattern="*.csv",
                      skiprows=10,
                      drop_first_column=True,
                      file_suffix=None):
        """
        Batch process multiple CSV files with the same operations.
        
        Args:
            source_directory (str): Path to source directory with CSV files
            destination_directory (str): Path to save processed files
            crop_params (dict): Parameters for cropping (start_row, end_row, start_col, end_col)
            downsample_params (dict): Parameters for downsampling (output_size, method)
            file_pattern (str): Pattern to match files
            skiprows (int): Number of header rows to skip
            drop_first_column (bool): Whether to drop the first column
            file_suffix (str): Suffix to append to output filenames
            
        Returns:
            list: Paths to processed files

    
        # Example: Batch process multiple files
        processor = ThermalImageProcessor()
        processor.batch_process(
            source_directory="path/to/source/dir",
            destination_directory="path/to/dest/dir",
            crop_params={
                'start_row': 50,
                'end_row': 430,
                'start_col': 190,
                'end_col': 540
            },
            downsample_params={
                'output_size': (100, 100),
                'method': 'nearest'
            },
            file_suffix="cropped_downsampled_100x100"
         )
        """


        
        # Set default parameters if not provided
        if crop_params is None:
            crop_params = {}
        if downsample_params is None:
            downsample_params = {}
        
        # Convert to Path objects
        source_dir = Path(source_directory)
        dest_dir = Path(destination_directory)
        
        # Create destination directory if it doesn't exist
        ensure_directory_exists(dest_dir)
        
        # Get all CSV files
        try:
            csv_files = list(source_dir.glob(file_pattern))
        except Exception as e:
            raise Exception(f"Error accessing source directory: {e}")
        
        processed_files = []
        
        for file_path in csv_files:
            try:
                # Process the file
                output_suffix = file_suffix or "processed"
                if downsample_params.get('output_size'):
                    size_str = 'x'.join(map(str, downsample_params.get('output_size', (100, 100))))
                    output_suffix = f"{output_suffix}_{size_str}"
                
                output_file = dest_dir / f"{file_path.stem}_{output_suffix}.csv"
                
                # Chain operations
                self.load_csv(file_path, skiprows, drop_first_column)
                
                if crop_params:
                    self.crop(**crop_params)
                
                if downsample_params:
                    self.downsample(**downsample_params)
                
                saved_path = self.save(output_file)
                if saved_path:
                    processed_files.append(saved_path)
                
            except Exception as e:
                print(f"Error processing {file_path.name}: {e}")
                continue
        
        print(f"\nTotal files processed: {len(processed_files)}")
        return processed_files