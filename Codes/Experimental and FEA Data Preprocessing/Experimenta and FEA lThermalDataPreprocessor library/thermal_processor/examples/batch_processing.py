"""
Example of batch processing multiple thermal image files.
"""

import os
import sys
import time

# Add the parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from thermal_processor import ThermalImageProcessor

def batch_process_files(source_directory, destination_directory):
    """
    Process all thermal image files in a directory.
    
    Args:
        source_directory (str): Path to the source directory
        destination_directory (str): Path to the destination directory
    """
    start_time = time.time()
    
    processor = ThermalImageProcessor()
    
    # Define processing parameters
    crop_params = {
        'start_row': 50,
        'end_row': 430,
        'start_col': 190,
        'end_col': 540
    }
    
    downsample_params = {
        'output_size': (100, 100),
        'method': 'nearest'
    }
    
    # Batch process the files
    processed_files = processor.batch_process(
        source_directory=source_directory,
        destination_directory=destination_directory,
        crop_params=crop_params,
        downsample_params=downsample_params,
        file_suffix="thermal_processed"
    )
    
    # Print processing time
    end_time = time.time()
    processing_time = end_time - start_time
    
    print(f"\nProcessing completed in {processing_time:.2f} seconds.")
    print(f"Processed {len(processed_files)} files.")

if __name__ == "__main__":
    # Check if source and destination directories were provided
    if len(sys.argv) > 2:
        source_dir = sys.argv[1]
        dest_dir = sys.argv[2]
        batch_process_files(source_dir, dest_dir)
    else:
        print("Please provide source and destination directories as command-line arguments.")
        print("Example: python -m thermal_processor.examples.batch_processing /path/to/source /path/to/destination")