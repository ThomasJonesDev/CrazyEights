import os


class FilePath:

    @staticmethod
    def get_file_path(relative_path_from_root) -> str:
        root_path = os.path.dirname(__file__)
        file_path = os.path.join(root_path, relative_path_from_root)
        return file_path
