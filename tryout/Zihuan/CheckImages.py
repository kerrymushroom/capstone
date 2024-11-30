import os

# Define the path to the image folder
base_dir = '/Users/subring/capstone/findRule/saved_data'
output_file = '/Users/subring/capstone/tryout/Zihuan/image_files.txt'

# Open the text file in write mode
with open(output_file, 'w') as f:
    # Traverse all subfolders and files
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            # Check if the file name ends with "_gpt.png"
            if file.lower().endswith('_gpt.png'):
                # Get the full file path
                file_path = os.path.join(root, file)
                try:
                    # Get the folder name and print it to the terminal
                    folder_name = os.path.basename(root)
                    print(f"Folder: {folder_name}")
                    # Write the image path to the file
                    f.write(file_path + '\n')
                except Exception as e:
                    print(f"Unable to process image {file_path}: {e}")

print(f"All paths of images ending with '_gpt.png' have been saved to {output_file}")
