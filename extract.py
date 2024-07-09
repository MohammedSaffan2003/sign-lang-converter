import os
import shutil

def extract_image(source_dir, destination_dir_letters, destination_dir_numbers):
  """
  Extracts one image from each folder in the source directory and saves it 
  with the folder name in separate "letters" and "numbers" folders.

  Args:
      source_dir: Path to the root directory containing subfolders (test, a, ..., z).
      destination_dir_letters: Path to the destination folder for letters.
      destination_dir_numbers: Path to the destination folder for numbers.
  """
  for folder_name in os.listdir(source_dir):
    folder_path = os.path.join(source_dir, folder_name)
    if os.path.isdir(folder_path):
      # Check if folder name contains only digits (numbers)
      if folder_name.isdigit():
        destination_dir = destination_dir_numbers
      else:
        destination_dir = destination_dir_letters

      # Get list of files in the folder
      files = os.listdir(folder_path)

      # Check if there are any files
      if files:
        # Assuming there's at least one image, pick the first one
        image_name = files[0]
        image_path = os.path.join(folder_path, image_name)

        # Create destination directory if it doesn't exist
        if not os.path.exists(destination_dir):
          os.makedirs(destination_dir)

        # Copy the image to the destination folder with the folder name
        destination_image_path = os.path.join(destination_dir, f"{folder_name}.{os.path.splitext(image_name)[1]}")
        shutil.copy2(image_path, destination_image_path)

# Modify these paths according to your dataset location
source_dir = "/home/codespace/.python/current/bin/python3/workspaces/codespaces-blank/Sign-Lang/isl_data_grey_split/test"
destination_dir_letters = "/home/codespace/.python/current/bin/python3/workspaces/codespaces-blank/Sign-Lang/letters"
destination_dir_numbers = "/home/codespace/.python/current/bin/python3/workspaces/codespaces-blank/Sign-Lang/numbers"

extract_image(source_dir, destination_dir_letters, destination_dir_numbers)

print("Images extracted and saved successfully!")
