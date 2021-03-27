# generalutils.files

    ensure_file(path_string):
        Takes a path string representing a file path and name, creates
        the file if it does not exist, and returns a namespace with creation results:
    
        :param path: str, file path (relative or absolute)
        :return: namespace (see below)
    
        result.fullpath: str, full absolute filepath
        result.directory: str, absolute file location
        result.filename: str, filename
        result.made_directory: bool, whether directory had to be created
        result.made_file: bool, whether file had to be created
