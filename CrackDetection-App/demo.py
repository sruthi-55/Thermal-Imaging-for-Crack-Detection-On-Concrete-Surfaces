import os

folder_path = '../test'

# Get all filenames in the folder
filenames = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

# Print the list of filenames
#print(filenames)
