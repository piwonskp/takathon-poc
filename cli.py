#!/usr/local/bin/python
import glob, os

import click

from takathon.compiler import compile_files
from takathon.runner import run_file
from takathon.tester import test_files


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
    compile_files(files, dst)


@cli.command(help='Run file')
@click.argument('file', type=click.File())
@click.argument('argv', nargs=-1)
def run(file, argv):
    run_file(file, argv)


if __name__ == '__main__':
    cli()
