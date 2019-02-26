#!/usr/local/bin/python
import glob, os, sys

import click

from takathon.main import test_files
from takathon.path_finder import TestModuleFinder
from takathon.splitter import get_code


@click.group()
def cli():
    pass


@cli.command(help='Test files')
@click.argument('target', type=click.Path(), default='.')
@click.argument('root', type=click.Path(), default='.')
def test(root, target):
    os.chdir(root)
    test_files(target)


@cli.command(help='Compile Taka project to Python')
@click.argument('src', type=click.Path(), default='.')
@click.argument('dst', type=click.Path(), default='compiled_project')
def compile(src, dst):
    os.chdir(src)
    files = glob.iglob('**', recursive=True)
    files = [f for f in files if not os.path.isdir(f)]

    for path in files:
        directory = os.path.join(dst, os.path.dirname(path))
        os.makedirs(directory, exist_ok=True)

        filename, ext = os.path.splitext(path)
        if ext == '.taka':
            out_path = os.path.join(dst, filename) + '.py'
            open(out_path, 'w').write(get_code(open(path).read()))
        else:
            os.symlink(path, os.path.join(dst, path))


@cli.command(help='Run file')
@click.argument('file', type=click.File())
@click.argument('argv', nargs=-1)
def run(file, argv):
    sys.argv = (file.name, ) + argv
    sys.meta_path.append(TestModuleFinder())
    exec(get_code(file.read()), {'__name__': '__main__'})


if __name__ == '__main__':
    cli()
