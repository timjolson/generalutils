from types import SimpleNamespace


def ensure_file(path):
    """Takes a path string representing a file path and name, creates
    the file if it does not exist, and returns a namespace with creation results:

    :param path: str, file path (relative or absolute)
    :return: namespace (see below)

    result.fullpath: str, full absolute filepath
    result.directory: str, absolute file location
    result.filename: str, filename
    result.made_directory: bool, whether directory had to be created
    result.made_file: bool, whether file had to be created
    """
    if not isinstance(path, str):
        raise TypeError('Provide a filename string.')
    from os.path import abspath, dirname, basename, isfile, isdir, realpath, normpath
    from os import makedirs

    result = SimpleNamespace()
    result.fullpath = abspath(realpath(normpath(path)))
    result.directory = dirname(result.fullpath)
    result.filename = basename(result.fullpath)
    assert result.filename != ''

    if isdir(result.directory):
        result.made_directory = False
    else:
        makedirs(result.directory, exist_ok=True)
        result.made_directory = True

    if not isfile(result.fullpath):
        with open(result.fullpath, 'a') as f:
            f.close()
        result.made_file = True
    else:
        result.made_file = False

    return result
