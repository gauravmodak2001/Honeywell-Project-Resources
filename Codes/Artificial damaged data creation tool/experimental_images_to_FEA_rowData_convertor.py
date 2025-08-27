import csv
import pandas as pd
import os
import glob

def convert_multiple_matrices_to_single_file(folder_path, output_file, file_pattern="*.csv"):
    """
    Convert multiple square CSV matrices from a folder into a single CSV file.
    Each input file becomes one row in the output file.
    
    Args:
        folder_path: Path to folder containing CSV files
        output_file: Name of output CSV file
        file_pattern: Pattern to match files (default: "*.csv")
    """
    # Get all CSV files in the folder
    csv_files = glob.glob(os.path.join(folder_path, file_pattern))
    
    if not csv_files:
        print(f"No CSV files found in {folder_path}")
        return
    
    print(f"Found {len(csv_files)} CSV files to process")
    
    all_rows = []
    file_info = []
    
    for i, file_path in enumerate(csv_files):
        try:
            print(f"Processing file {i+1}/{len(csv_files)}: {os.path.basename(file_path)}")
            
            # Read the CSV file
            df = pd.read_csv(file_path, header=None)
            
            # Flatten the matrix to a single row
            flattened = df.values.flatten()
            
            # Add to our collection
            all_rows.append(flattened)
            file_info.append({
                'filename': os.path.basename(file_path),
                'original_shape': df.shape,
                'flattened_length': len(flattened)
            })
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            continue
    
    if all_rows:
        # Create DataFrame with all flattened rows
        result_df = pd.DataFrame(all_rows)
        
        # Save to output file
        result_df.to_csv(output_file, index=False, header=False)
        
        print(f"\nSuccessfully created {output_file}")
        print(f"Output shape: {result_df.shape}")
        print(f"({result_df.shape[0]} files × {result_df.shape[1]} values per file)")
        
        # Print summary of processed files
        print("\nProcessed files summary:")
        for info in file_info:
            print(f"  {info['filename']}: {info['original_shape']} → {info['flattened_length']} values")
    
    else:
        print("No files were successfully processed")

def convert_multiple_matrices_with_filenames(folder_path, output_file, file_pattern="*.csv"):
    """
    Same as above but includes filename as the first column of each row
    """
    csv_files = glob.glob(os.path.join(folder_path, file_pattern))
    
    if not csv_files:
        print(f"No CSV files found in {folder_path}")
        return
    
    print(f"Found {len(csv_files)} CSV files to process")
    
    all_rows = []
    
    for i, file_path in enumerate(csv_files):
        try:
            print(f"Processing file {i+1}/{len(csv_files)}: {os.path.basename(file_path)}")
            
            # Read and flatten the CSV
            df = pd.read_csv(file_path, header=None)
            flattened = df.values.flatten()
            
            # Create row with filename as first column
            filename = os.path.basename(file_path)
            row_with_filename = [filename] + flattened.tolist()
            all_rows.append(row_with_filename)
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            continue
    
    if all_rows:
        # Create DataFrame and save
        result_df = pd.DataFrame(all_rows)
        result_df.to_csv(output_file, index=False, header=False)
        
        print(f"\nSuccessfully created {output_file} with filenames")
        print(f"Output shape: {result_df.shape}")

def convert_specific_files_to_single_file(file_list, output_file):
    """
    Convert specific CSV files (provided as a list) to a single CSV file
    """
    all_rows = []
    
    for i, file_path in enumerate(file_list):
        if not os.path.exists(file_path):
            print(f"Warning: File not found - {file_path}")
            continue
            
        try:
            print(f"Processing file {i+1}/{len(file_list)}: {os.path.basename(file_path)}")
            
            df = pd.read_csv(file_path, header=None)
            flattened = df.values.flatten()
            all_rows.append(flattened)
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            continue
    
    if all_rows:
        result_df = pd.DataFrame(all_rows)
        result_df.to_csv(output_file, index=False, header=False)
        print(f"\nSuccessfully created {output_file}")
        print(f"Output shape: {result_df.shape}")

# Usage examples
if __name__ == "__main__":
    
    # Example 1: Process all CSV files in a folder
    folder_path = r"C:\Users\G_Modak\Desktop\Honeywell Project Final\Codes\ML Models\ML Experimental Codes\Experimental Processed Data for ML trained model testing"  # Update this path
    output_file = r"C:\Users\G_Modak\Desktop\Honeywell Project Final\Codes\ML Models\ML Experimental Codes\Experimental Processed Data for ML trained model testing\combine_experimental_for_data_testing.csv"
    convert_multiple_matrices_to_single_file(folder_path, output_file)
    
    # Example 2: Process all CSV files and include filenames
    # convert_multiple_matrices_with_filenames(folder_path, "combined_with_filenames.csv")
    
    # Example 3: Process specific files
    # specific_files = [
    #     "file1.csv",
    #     "file2.csv", 
    #     "file3.csv"
    # ]
    # convert_specific_files_to_single_file(specific_files, "specific_combined.csv")
    
    # Example 4: Process files with specific pattern
    # convert_multiple_matrices_to_single_file(folder_path, "rec_files_combined.csv", "Rec*.csv")