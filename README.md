# **"Using AlphaFold2 to Predict the Conformations of Side Chains in Folded Proteins"** 
**doi: 10.1101/2025.02.10.637534** 

## Code to reproduce the CHI values reported in the manuscript:

### Step 1: Convert AlphaFold (AF3) CIF files to PDB

AlphaFold3 currently outputs protein models in `.cif` format. To calculate side-chain χ (chi) angles, we first convert these CIF files to the standard `.pdb` format using PyMOL.

You can do this with the provided script:

**[convert_cif2pdb.py](https://github.com/axt651/Chi-angles/blob/main/convert_cif2pdb.py)**
This script:
- Loads all `.cif` files in the working directory
- Converts them to `.pdb` format
- Saves them with the same base filename
- How to Use:
  Make sure to update the os.chdir(r"/working/directory") at the bottom of the script to your actual path.
  Then run script directly inside the PYMOL


### Step 2: Compute Side-Chain Chi (χ) Angles for All Residues in Chain A

After converting `.cif` to `.pdb` files, this step computes χ1–χ4 angles for residues in **chain A** across all models (PDB files) using:

🔗 **[Chi_compute_multiple_pdbs.py](https://github.com/axt651/Chi-angles/blob/main/Chi_compute_multiple_pdbs.py)**

This script:
- Iterates over all `.pdb` files in a directory
- Computes χ angles using PyMOL dihedral calculations
- Outputs a `.dat` file for each structure with residue-level χ1–χ4 angles
- How to Use:
  Make sure to update the `directory_path` at the bottom of the script to your actual path.
  Then run script directly inside the PYMOL

### Step 3: Merge All Chi Angle Files into a Single CSV for Analysis

Each `.dat` file generated in Step 2 corresponds to one PDB structure. This script aggregates all those into a single CSV file with one row per residue per structure:

🔗 **[convert_dat_csv.py](https://github.com/axt651/Chi-angles/blob/main/convert_dat_csv.py)**

This script:
- Parses all `*_chi_angles.dat` files in a directory
- Extracts χ1–χ4 values for each residue
- Adds a column for the PDB ID (parsed from the filename)
- Merges all data into a unified CSV file for downstream analysis
- How to Use
Update the paths at the bottom of the script:
directory_path = "/path/to/folder/with/dat/files"
output_csv_file = "/desired/output/path/AF3_chi_angles.csv"

python convert_dat_csv.py


#### Example files are uploaded in the **[Example_AF3](https://github.com/axt651/Chi-angles/tree/main/Example_AF3) for quick test

