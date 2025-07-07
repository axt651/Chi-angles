import os
import csv

def process_dat_files_to_csv(directory_path, output_csv_file):
    """
    Processes all .dat files in the directory, extracts the data, and writes it to a CSV file.

    Args:
      directory_path: Path to the directory containing .dat files.
      output_csv_file: Path to the output CSV file where data will be saved.
    """
    all_data = []

    # Loop through all files in the directory
    for filename in os.listdir(directory_path):
        # Only process files with .dat extension
        if filename.endswith("_chi_angles.dat"):
            pdb_id = filename.split('_')[1]  # Extract the PDB ID (e.g., '8pqm' from 'fold_8pqm_af3_model_0_chi_angles.dat')
            dat_file = os.path.join(directory_path, filename)

            # Open and process the .dat file
            with open(dat_file, "r") as f:
                lines = f.readlines()

                # Skip the header line
                for line in lines[1:]:
                    # Split each line into residue_number, residue_name, CHI1, CHI2, CHI3, CHI4
                    parts = line.strip().split()
                    residue_number = parts[0]
                    residue_name = parts[1]
                    chi1 = parts[2]
                    chi2 = parts[3]
                    chi3 = parts[4]
                    chi4 = parts[5]

                    # Add data to the list, including the pdb_id
                    all_data.append([pdb_id, residue_number, residue_name, chi1, chi2, chi3, chi4])

    # Write all data to a CSV file
    with open(output_csv_file, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['pdb_ID', 'residue_number', 'residue_name', 'CHI1', 'CHI2', 'CHI3', 'CHI4'])  # header
        writer.writerows(all_data)

    print(f"Data from all .dat files has been written to {output_csv_file}")

# Example usage:
directory_path = "/Users/thakura3/work/CHI/AF3_structures"  # Set the correct directory path where the .dat files are located
output_csv_file = "/Users/thakura3/work/CHI/AF3_structures_copy/AF3.csv"  # Set the path for the output CSV file

process_dat_files_to_csv(directory_path, output_csv_file)

