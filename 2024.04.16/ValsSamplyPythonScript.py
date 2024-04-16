#Final Final Version
#sigh  this works but produces an error.  follow up on error later!!
# vlb 2024.04.11
#You can consolidate the handling of input—whether it's coming from a CSV file or directly from user input—into a single DataFrame. This approach allows you to streamline the processing portion of your script, treating both sources of data uniformly in the subsequent steps for generating SCAD and STL files.

# Here's how you could modify the script to incorporate this unified approach:

# !pip install pyarrow
import pyarrow
import pandas as pd
import subprocess
from pathlib import Path

# Define base paths once
base_dir = Path(r"V:\_GitRepos_old\GardenProject\seed_labels_3dprint")
scad_dir = base_dir / "output_scad_files"
stl_dir = base_dir / "output_stl_files"
csv_file_path = base_dir / "testseeds.csv"

# Ensure output directories exist
scad_dir.mkdir(parents=True, exist_ok=True)
stl_dir.mkdir(parents=True, exist_ok=True)


# SCAD template
scad_template = """
// Customizable Garden Plant Label Stake
// by Mark Thompson

text_string = "{}";
text_size = 12;
text_thickness = 3;
text_font = "Nimbus Sans L:Bold";
text_y_offset_adjust = 0;

subtext_string = "{}";
subtext_size = 6;
subtext_thickness = 4;
subtext_font = "Nimbus Sans L:Bold";
subtext_y_offset_adjust = -8;

//stake_length = 175;
stake_length = 215;
stake_thickness = 5;
stake_height = 5;

point_length = 10;
tip_size = 0.5;

{{
    translate([0,text_y_offset_adjust,0])
        linear_extrude(height=text_thickness, convexity=4)
            text(text_string,size=text_size,font=text_font);

    translate([0,subtext_y_offset_adjust,0])
        linear_extrude(height=subtext_thickness, convexity=4)
            text(subtext_string,size=subtext_size,font=subtext_font);

    translate([stake_length/2,-stake_height/2,stake_thickness/2]) {{
        difference() {{
            hull() {{
                cube([stake_length,stake_height,stake_thickness],true);
                translate([stake_length/2+point_length,stake_height/2-tip_size/2,-stake_thickness/2+tip_size/2])
                    cube([tip_size,tip_size,tip_size],true);
            }}

            translate([0,-stake_height/2,stake_thickness/2])
                cube([stake_length+point_length*2+0.1,stake_height,stake_thickness],true);
        }}
    }}
}}
"""

def generate_scad_file(plant_name, plant_variety, output_dir=scad_dir):
    """Generate a SCAD file for a given plant name and variety."""
    scad_content = scad_template.format(plant_name, plant_variety)
    file_name = f"{plant_name} - {plant_variety}.scad"
    file_path = output_dir / file_name

    with open(file_path, 'w') as file:
        file.write(scad_content)
    print(f"SCAD file saved: {file_path}")

def convert_scad_to_stl(scad_file, stl_file):
    """Convert a SCAD file to STL format using OpenSCAD."""
    command = ['C:\\Program Files\\OpenSCAD\\openscad.exe', '-o', str(stl_file), str(scad_file)]
    subprocess.run(command, check=True)
    print(f"Converted to STL: {stl_file}")

def process_dataframe(df, scad_output_dir, stl_output_dir, source_from_csv=True):
    """Process each row in the DataFrame to generate SCAD and STL files.
       The `source_from_csv` parameter indicates whether the data frame comes from a CSV file."""

    for index, row in df.iterrows():

        # Choose the way to access data based on the data source
        if source_from_csv:
            # Assuming the CSV has the necessary data in the 5th and 6th columns
            plant_name, plant_variety = row[4], row[5]
        else:
            # For data frames created from user input with explicit column names
            plant_name, plant_variety = row['category'], row['variety']

        generate_scad_file(plant_name, plant_variety, scad_output_dir)

        scad_file_path = scad_output_dir / f"{plant_name} - {plant_variety}.scad"
        stl_file_path = stl_output_dir / f"{plant_name} - {plant_variety}.stl"
        convert_scad_to_stl(scad_file_path, stl_file_path)

def get_data_frame_from_input():
    """Get DataFrame from user input for a single plant tag."""
    plant_name = input("Enter the plant category (e.g., Tomato): ")
    plant_variety = input("Enter the plant variety (e.g., Early Girl): ")
    return pd.DataFrame([[plant_name, plant_variety]], columns=['category', 'variety'])

def main_menu():
    print("\nMenu:")
    print("1. Create plant tags from a CSV")
    print("2. Create plant tag from user input")
    choice = input("Select an option: ")

    if choice == '1':
        df = pd.read_csv(csv_file_path)
        # Assuming the data frame from CSV needs index-based access
        process_dataframe(df, scad_dir, stl_dir, source_from_csv=True)
    elif choice == '2':
        df = get_data_frame_from_input()
        # Data frame from user input uses column names
        process_dataframe(df, scad_dir, stl_dir, source_from_csv=False)
    else:
        print("Invalid choice. Please enter 1 or 2.")
        return

    process_dataframe(df, scad_dir, stl_dir)

if __name__ == "__main__":
    main_menu()


### Key Changes and Assumptions:

# - **Data Handling Unified**: Whether the data comes from a CSV file or user input, it's converted into a Pandas DataFrame. This approach simplifies the rest of the script, as it can process the DataFrame without caring about the data's origin.
# - **DataFrame Structure**: The DataFrame is assumed to have two columns: 'category' and 'variety'. Adjust the column names based on your actual data structure or requirements.
# - **Simplified Input Handling**: The function `get_data_frame_from_input` is introduced to handle user input, creating a DataFrame with a single row based on the input. This is useful for when the script is used to generate a tag for just one plant.
# - **Menu Function**: The `main_menu` function directs the flow based on the user's choice, loading data into a DataFrame from the appropriate source.

