import pymol
from pymol import cmd, stored
import os

def calculate_chi_angles(pdb_file, output_file, chi_angle_definitions):
    """
    Calculates Chi1-4 angles for specific residues in chain A of a PDB file and writes them to a file.

    Args:
      pdb_file: Path to the PDB file.
      output_file: Path to the output file.
      chi_angle_definitions: A dictionary where keys are residue names and values are lists of atom names
                             defining the Chi angles for that residue.
    """

    # Load PDB file and reset
    cmd.reinitialize()
    cmd.load(pdb_file)

    # Open output file for writing
    with open(output_file, "w") as f:
        f.write(f"Residue Chi1 Chi2 Chi3 Chi4\n")

        # Get all residues of chain A
        stored.list = []
        cmd.iterate("chain A and name CA", "stored.list.append((resi, resn))")

        # Iterate over all residues in chain A
        for residue_index, residue_name in stored.list:
            # Skip non-standard residues or those without definitions
            if residue_name not in chi_angle_definitions:
                continue
            
            # Get chi angle definitions for this residue type
            chi_angles = chi_angle_definitions[residue_name]
            
            # Calculate each chi angle
            chi_values = []
            
            # Debug information
            print(f"Processing residue {residue_name} {residue_index}")
            
            # Process each chi angle
            for i, chi_def in enumerate(chi_angles, 1):
                if chi_def == "N/A":
                    chi_values.append("N/A")
                    continue
                    
                # Parse the atom names
                atoms = chi_def.split('-')
                if len(atoms) != 4:
                    chi_values.append("N/A")
                    continue
                
                # Build the full atom selections
                sel_atoms = [f"chain A and resi {residue_index} and name {atom}" for atom in atoms]
                
                # Debug
                print(f"  Chi{i} atoms: {', '.join(sel_atoms)}")
                
                # Check if all atoms exist
                all_atoms_exist = True
                for sel in sel_atoms:
                    if cmd.count_atoms(sel) == 0:
                        print(f"  Warning: Atom not found: {sel}")
                        all_atoms_exist = False
                        break
                
                # Calculate dihedral if possible
                if all_atoms_exist:
                    try:
                        angle = cmd.get_dihedral(sel_atoms[0], sel_atoms[1], sel_atoms[2], sel_atoms[3])
                        chi_values.append(f"{angle:.2f}")
                        print(f"  Chi{i}: {angle:.2f}")
                    except Exception as e:
                        print(f"  Error calculating Chi{i}: {e}")
                        chi_values.append("ERROR")
                else:
                    chi_values.append("MISSING")
            
            # Pad with N/A for missing chi angles
            while len(chi_values) < 4:
                chi_values.append("N/A")
                
            # Write values to file
            f.write(f"{residue_index} {residue_name} {' '.join(chi_values)}\n")

def process_all_pdb_files_in_directory(directory_path, chi_angle_definitions):
    """
    Processes all PDB files in the specified directory, calculates Chi angles, and saves the results
    to output files named after the PDB files.

    Args:
      directory_path: Path to the directory containing PDB files.
      chi_angle_definitions: A dictionary where keys are residue names and values are lists of atom names
                             defining the Chi angles for that residue.
    """
    for filename in os.listdir(directory_path):
        # Only process files with .pdb extension
        if filename.endswith(".pdb"):
            pdb_file = os.path.join(directory_path, filename)
            output_file = os.path.join(directory_path, f"{os.path.splitext(filename)[0]}_chi_angles.dat")
            
            print(f"Processing file: {pdb_file}")
            
            # Call the calculate_chi_angles function
            calculate_chi_angles(pdb_file, output_file, chi_angle_definitions)

# Define Chi angle definitions based on the provided table
chi_angle_definitions = {
    "ALA": ["N/A"],
    "ARG": ["N-CA-CB-CG", "CA-CB-CG-CD", "CB-CG-CD-NE", "CG-CD-NE-CZ"],
    "ASN": ["N-CA-CB-CG", "CA-CB-CG-OD1"],
    "ASP": ["N-CA-CB-CG", "CA-CB-CG-OD1"],
    "CYS": ["N-CA-CB-SG"],
    "GLN": ["N-CA-CB-CG", "CA-CB-CG-CD", "CB-CG-CD-OE1"],
    "GLU": ["N-CA-CB-CG", "CA-CB-CG-CD", "CB-CG-CD-OE1"],
    "GLY": ["N/A"],
    "HIS": ["N-CA-CB-CG", "CA-CB-CG-ND1"],
    "ILE": ["N-CA-CB-CG1", "CA-CB-CG1-CD1"],  
    "LEU": ["N-CA-CB-CG", "CA-CB-CG-CD1"],
    "LYS": ["N-CA-CB-CG", "CA-CB-CG-CD", "CB-CG-CD-CE", "CG-CD-CE-NZ"],  
    "MET": ["N-CA-CB-CG", "CA-CB-CG-SD", "CB-CG-SD-CE"],
    "PHE": ["N-CA-CB-CG", "CA-CB-CG-CD1"],
    "PRO": ["N-CA-CB-CG", "CA-CB-CG-CD"],
    "SER": ["N-CA-CB-OG"],
    "THR": ["N-CA-CB-OG1"],
    "TRP": ["N-CA-CB-CG", "CA-CB-CG-CD1"],
    "TYR": ["N-CA-CB-CG", "CA-CB-CG-CD1"],
    "VAL": ["N-CA-CB-CG1"]
}

# Example usage
directory_path = "/working/directory/where/pdb/files/are/stored"
process_all_pdb_files_in_directory(directory_path, chi_angle_definitions)
