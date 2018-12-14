# -*- coding: UTF-8 -*-

import click
import click_log
logger = click_log.basic_config()

import sys
from os import path, getcwd, sep

from inspect import getsourcefile
from collections import namedtuple


current_dir = path.dirname(path.abspath(getsourcefile(lambda: 0)))
sys.path.insert(0, current_dir[: current_dir.rfind(path.sep)])


import cireqs.__version__  #pylint: disable=import-error


Conf = namedtuple('Config', 'dir_path python_version timeout env_vars, run_dry')

def exit_if_file_not_exists(filename, conf):
    dir_path = path.normpath(conf.dir_path) + sep
    if not path.isfile(dir_path + filename):
        click.echo(filename + " does not exist")
        exit(-1)

@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--pythonversion', nargs=1, type=str, default='3.6.1', help='python version to use for calculating dependencies, defaults to 3.6.1')
@click.option('--dirpath', nargs=1, help="path to directory containing requirement files, defaults to PWD")
@click.option('--timeout', nargs=1, type=int, default=120, help="how long to wait for docker commands, defaults to 120s")
@click.option('--envvar','-e', nargs=1, type=str, default='', multiple=True, help="environment var ENV_VAR=VALUE (or ENV_VAR to copy env_var), multiple allowed, defaults to None")
@click.option('--version', '-V', is_flag=True, help="show version and exit")
@click.option('--dry', is_flag=True, help="print out docker command line without running it")
@click_log.simple_verbosity_option()
@click_log.init('cireqs.cli')
def cli(ctx, dirpath, pythonversion, timeout, envvar, version, dry):
    ctx.obj = Conf(
        python_version=pythonversion,
        dir_path=dirpath or getcwd(),
        timeout=timeout,
        env_vars=envvar,
        run_dry=dry
    )
    cireqs.set_log_level(click_log.get_level())

    splash = r"""
           o8o
           `"'
 .ooooo.  oooo  oooo d8b  .ooooo.   .ooooo oo  .oooo.o
d88' `"Y8 `888  `888""8P d88' `88b d88' `888  d88(  "8
888        888   888     888ooo888 888   888  `"Y88b.
888   .o8  888   888     888    .o 888   888  o.  )88b
`Y8bod8P' o888o d888b    `Y8bod8P' `V8bod888  8""888P'
                                         888.
                                         8P'  """
    splash = click.style(splash, fg='green') + click.style(
        "v{}".format(cireqs.__version__.__version__), fg='red') + "\n"

    if ctx.invoked_subcommand is None:
        if version:
            click.echo(click.style(cireqs.__version__.__version__, fg='green'))
            return
        click.echo("\n".join([splash, ctx.get_help()]))
        return


@cli.command()
@click.argument('input_requirements_filename', nargs=1, type=str, default='requirements_to_expand.txt')
@click.argument('output_requirements_filename', nargs=1, type=str, default='requirements.txt')
@click.pass_obj
def expand(conf, output_requirements_filename, input_requirements_filename):
    """Expand given requirements file by extending it using pip freeze

    args:

    input_requirements_filename: the requirements filename to expand

    output_requirements_filename: the output filename for the expanded
    requirements file
    """
    exit_if_file_not_exists(input_requirements_filename, conf)
    cireqs.expand_requirements(
        requirements_filename=input_requirements_filename,
        expanded_requirements_filename=output_requirements_filename,
        **conf._asdict()
    )
    click.echo(click.style('✓', fg='green') + " {} has been expanded into {}".format(
        input_requirements_filename, output_requirements_filename
    ))


@cli.command()
@click.argument('input_requirements_filename', nargs=1, type=str, default='requirements_to_expand.txt')
@click.argument('output_requirements_filename', nargs=1, type=str, default='requirements.txt')
@click.pass_obj
@click.pass_context
def expand_requirements(ctx, conf, output_requirements_filename, input_requirements_filename):
    click.echo(click.style('expand_requirements is being deprecated, please use expand instead!', fg='red'))
    ctx.forward(expand)


@cli.command()
@click.argument('input_requirements_filename', nargs=1, type=str, default='requirements.txt')
@click.pass_obj
def verify(conf, input_requirements_filename):
    """Verifying that given requirements file is not missing any pins

    args:

    input_requirements_filename: requriements file to verify

    """
    exit_if_file_not_exists(input_requirements_filename, conf)

    cireqs.check_if_requirements_are_up_to_date(
        requirements_filename=input_requirements_filename,
        **conf._asdict())
    click.echo(click.style('✓', fg='green') + " {} has been verified".format(input_requirements_filename))


@cli.command()
@click.argument('input_requirements_filename', nargs=1, type=str, default='requirements.txt')
@click.pass_obj
@click.pass_context
def verify_requirements(ctx, conf, input_requirements_filename):
    click.echo(click.style('verify_requirements is being deprecated, please use verify instead!', fg='red'))
    ctx.forward(verify)


if __name__ == "__main__":
    cli() #pylint: disable=no-value-for-parameter
