from pymol import cmd
import glob, os

# Change to your directory with CIF files
os.chdir(r"/working/directory")

cmd.reinitialize()
for cif in glob.glob("*.cif"):
    base = cif[:-4]
    print(f"Converting {cif} → {base}.pdb")
    cmd.load(cif, base)
    cmd.save(f"{base}.pdb", base)
    cmd.delete(base)

