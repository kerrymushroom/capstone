import os


def lowercase_files_in_folder(folder_path):
    # Walk through the directory and its subdirectories
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            # Construct the full file path
            file_path = os.path.join(root, file_name)

            # Convert the file name to lowercase
            lower_file_name = file_name.lower()
            lower_file_path = os.path.join(root, lower_file_name)

            # Rename the file if the lowercase name is different
            if file_path != lower_file_path:
                os.rename(file_path, lower_file_path)
                print(f"Renamed: {file_path} -> {lower_file_path}")


# Specify the folder path where you want to start renaming
folder_path = "./visEval_dataset/databases"
lowercase_files_in_folder(folder_path)
