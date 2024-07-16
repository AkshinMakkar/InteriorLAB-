import subprocess
import os

class SCADtoSTL:
    def scad_to_stl(self, scad_file, stl_file, openscad_path):
        """
        Convert a .scad file to a .stl file using OpenSCAD.

        :param scad_file: Path to the input .scad file.
        :param stl_file: Path to the output .stl file.
        :param openscad_path: Full path to the OpenSCAD executable.
        """
        # Check if OpenSCAD is installed
        if not os.path.isfile(openscad_path):
            raise EnvironmentError(f"OpenSCAD is not found at {openscad_path}")
        
        # Run the OpenSCAD CLI command
        command = [openscad_path, "-o", stl_file, scad_file]
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
        else:
            print(f"Successfully converted {scad_file} to {stl_file}")