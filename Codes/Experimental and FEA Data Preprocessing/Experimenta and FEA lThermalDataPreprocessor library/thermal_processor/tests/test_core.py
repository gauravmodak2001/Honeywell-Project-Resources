"""
Tests for the core functionality of the thermal processor module.
"""

import unittest
import os
import tempfile
import pandas as pd
import numpy as np
from pathlib import Path

# Add the parent directory to the path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from thermal_processor import ThermalImageProcessor

class TestThermalImageProcessor(unittest.TestCase):
    """
    Tests for the ThermalImageProcessor class.
    """
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary CSV file with test data
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_file = os.path.join(self.temp_dir.name, "test_data.csv")
        
        # Create test data
        data = np.random.normal(25.0, 1.0, (500, 600))
        
        # Add header rows
        with open(self.temp_file, 'w') as f:
            f.write("File: ,Test thermal image\n")
            f.write("Parameters:,Emissivity:,0.94 \n")
            f.write(",Refl. temp.:,20.0 °C\n")
            f.write(",Distance:,1.0 m\n")
            f.write(",Atmospheric temp.:,20.0 °C\n")
            f.write(",Ext. optics temp.:,20.0 °C\n")
            f.write(",Ext. optics trans.:,1.0 \n")
            f.write(",Relative humidity:,50.0 %\n")
            f.write(",\n")
            f.write(",\n")
        
        # Save data to CSV
        np.savetxt(self.temp_file, data, delimiter=',', fmt='%.3f', mode='a')
        
        # Create processor instance
        self.processor = ThermalImageProcessor()
    
    def tearDown(self):
        """Tear down test fixtures."""
        self.temp_dir.cleanup()
    
    def test_load_csv(self):
        """Test loading a CSV file."""
        self.processor.load_csv(self.temp_file, skiprows=10)
        self.assertIsNotNone(self.processor.data)
        self.assertEqual(self.processor.data.shape, (500, 600))
    
    def test_crop(self):
        """Test cropping the data."""
        self.processor.load_csv(self.temp_file, skiprows=10)
        self.processor.crop(start_row=50, end_row=250, start_col=100, end_col=400)
        self.assertEqual(self.processor.data.shape, (200, 300))
    
    def test_downsample(self):
        """Test downsampling the data."""
        self.processor.load_csv(self.temp_file, skiprows=10)
        self.processor.downsample(output_size=(100, 100))
        self.assertEqual(self.processor.data.shape, (100, 100))
    
    def test_save(self):
        """Test saving the data."""
        self.processor.load_csv(self.temp_file, skiprows=10)
        output_file = os.path.join(self.temp_dir.name, "output.csv")
        saved_path = self.processor.save(output_file)
        self.assertTrue(os.path.exists(saved_path))
    
    def test_method_chaining(self):
        """Test method chaining."""
        output_file = os.path.join(self.temp_dir.name, "chained_output.csv")
        self.processor.load_csv(self.temp_file, skiprows=10) \
                      .crop(start_row=50, end_row=250, start_col=100, end_col=400) \
                      .downsample(output_size=(100, 100)) \
                      .save(output_file)
        
        self.assertTrue(os.path.exists(output_file))
        self.assertEqual(self.processor.data.shape, (100, 100))

if __name__ == "__main__":
    unittest.main()