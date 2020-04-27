import os

from takathon.importlib.splitter import get_code


def build_directory_structure(destination, path):
    directory = os.path.join(destination, os.path.dirname(path))
    os.makedirs(directory, exist_ok=True)


def save_compiled_file(destination, source):
    open(destination, 'w').write(get_code(open(source).read()))


def compile_files(paths, destination):
    for src in paths:
        build_directory_structure(destination, src)

        filename, ext = os.path.splitext(src)
        if ext == '.taka':
            save_compiled_file(os.path.join(destination, filename) + '.py', src)
        else:
            os.symlink(src, os.path.join(destination, src))
