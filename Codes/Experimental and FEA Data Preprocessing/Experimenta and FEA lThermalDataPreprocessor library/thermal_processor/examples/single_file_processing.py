"""
Example of processing a single thermal image file.
"""

import os
import sys
import matplotlib.pyplot as plt

# Add the parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from thermal_processor import ThermalImageProcessor

def process_single_file(file_path):
    """
    Process a single thermal image file.
    
    Args:
        file_path (str): Path to the thermal image CSV file
    """
    processor = ThermalImageProcessor()
    
    # Load, crop, and downsample the data
    processor.load_csv(file_path) \
             .crop(start_row=50, end_row=430, start_col=190, end_col=540) \
             .downsample(output_size=(100, 100), method='nearest') \
             .visualize() \
             .save(suffix="100x100_nearest")
    
    # Print processing history
    print("\nProcessing History:")
    for step in processor.get_processing_history():
        print(f"- {step}")

if __name__ == "__main__":
    # Check if a file path was provided
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        process_single_file(file_path)
    else:
        print("Please provide a file path as a command-line argument.")
        print("Example: python -m thermal_processor.examples.single_file_processing /path/to/your/file.csv")