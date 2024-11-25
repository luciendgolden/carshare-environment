import os

def get_resource_path(file_name):
    current_file = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_file)

    directory_levels_to_project_root = current_directory.count(os.sep) - os.path.abspath(os.sep.join([current_file, '..', '..', '..'])).count(os.sep)
    project_root = current_directory

    for _ in range(directory_levels_to_project_root):
        project_root = os.path.dirname(project_root)

    resources_folder = os.path.join(project_root, 'resources')
    file_path = os.path.join(resources_folder, file_name)

    if os.path.exists(file_path):
        return file_path
    else:
        return None