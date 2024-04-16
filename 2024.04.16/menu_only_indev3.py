import os
import csv
from pathlib import Path

# Define base paths once
base_dir = Path(r"V:\_GitRepos_old\GardenProject\seed_labels_3dprint")
stake_scad_dir = base_dir / "stakes_scad_temp"
tag_scad_dir = base_dir / "tag_scad_temp"

stake_stl_dir = base_dir / "stake_stls_out"
tag_stl_dir = base_dir / "tag_stls_out"
csv_file_path = base_dir / "testseeds.csv"

# Ensure temp and output directories exist
stake_scad_dir.mkdir(parents=True, exist_ok=True)
tag_scad_dir.mkdir(parents=True, exist_ok=True)
stake_stl_dir.mkdir(parents=True, exist_ok=True)
tag_stl_dir.mkdir(parents=True, exist_ok=True)

def clear_screen():
    if os.name == 'nt':  # for Windows
        os.system('cls')
    else:  # for macOS and Linux
        os.system('clear')

def create_individual_stake():
    name = input("Enter the name of the plant: ")
    variety = input("Enter the variety of the plant: ")
    print(f"\nPlant stake for '{name}' ({variety}) created!")
    input("\nPress Enter to continue...")

def create_individual_tag():
    name = input("Enter the name of the plant: ")
    variety = input("Enter the variety of the plant: ")
    print(f"\nPlant tag for '{name}' ({variety}) created!")
    input("\nPress Enter to continue...")

def create_bulk_stake():
    try:
        with open(csv_file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                name, variety = row
                print(f"\nPlant stake created for '{name}' ({variety})")
            input("\nPress Enter to continue...")
    except FileNotFoundError:
        print("\nFile not found. Please check the path and try again.")
        input("\nPress Enter to continue...")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        input("\nPress Enter to continue...")

def create_bulk_tag():
    try:
        with open(csv_file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                name, variety = row
                print(f"\nPlant tag created for '{name}' ({variety})")
            input("\nPress Enter to continue...")
    except FileNotFoundError:
        print("\nFile not found. Please check the path and try again.")
        input("\nPress Enter to continue...")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        input("\nPress Enter to continue...")

def main_menu():
    while True:
        print("\nMain Menu")
        print("1. Create Plant Stake")
        print("2. Create Plant Tag")
        print("0. Delete temp SCAD directories and Exit")
        choice = input("Enter your choice (1, 2, or 0 to exit): ")
        clear_screen()

        if choice == '1':
            stake_menu()
        elif choice == '2':
            tag_menu()
        elif choice == '0':
            if stake_scad_dir.exists():
                for child in stake_scad_dir.iterdir():
                    child.unlink()
                stake_scad_dir.rmdir()
            if tag_scad_dir.exists():
                for child in tag_scad_dir.iterdir():
                    child.unlink()
                tag_scad_dir.rmdir()
            print("Temporary directories deleted. Exiting the program.")
            break
        else:
            print("Invalid choice. Please choose again.")
            input("\nPress Enter to continue...")

def stake_menu():
    while True:
        print("\nPlant Stake Menu")
        print("1. Individual Creation")
        print("2. Bulk Creation")
        print("0. Return to Main Menu")
        choice = input("Enter your choice (1, 2, or 0 to return): ")
        clear_screen()

        if choice == '1':
            create_individual_stake()
        elif choice == '2':
            create_bulk_stake()
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please choose again.")
            input("\nPress Enter to continue...")

def tag_menu():
    while True:
        print("\nPlant Tag  Menu")
        print("1. Individual Creation")
        print("2. Bulk Creation")
        print("0. Return to Main Menu")
        choice = input("Enter your choice (1, 2, or 0 to return): ")
        clear_screen()

        if choice == '1':
            create_individual_tag()
        elif choice == '2':
            create_bulk_tag()
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please choose again.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main_menu()

### Key Changes:
#1. **Directory Management**: The script ensures the existence of necessary directories at the start and handles the deletion of temporary directories upon exiting the program.
#2. **Exit Option Updated**: The main menu's exit option now deletes any temporary directories before exiting, as specified.
#3. **Path Management**: Utilizing the `pathlib` module to handle paths in a platform-independent and readable manner.
#4. Clear Screen Function (clear_screen): This function detects the operating system and uses the appropriate command (cls for Windows, clear for Unix/Linux) to clear the console. This function is called at the beginning of each menu function to ensure that the screen is clear before displaying new menu options.
# 5. **Clear Screen Placement**: The screen is now cleared right after the user makes a selection and before displaying a new menu or message, ensuring that prior outputs don't interfere visually with subsequent interactions.
# 6. **User Prompts**: Added `input("\nPress Enter to continue...")` after key actions so users can read the output and choose when to continue, which also prevents the screen from clearing too quickly.
# 7. **New Lines in Outputs**: Added `\n` to enhance the readability of outputs by spacing them more pleasantly.



