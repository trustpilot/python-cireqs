import click
import click_log
logger = click_log.basic_config()

import sys
from os import path, getcwd

from inspect import getsourcefile
from collections import namedtuple


current_dir = path.dirname(path.abspath(getsourcefile(lambda: 0)))
sys.path.insert(0, current_dir[: current_dir.rfind(path.sep)])

import cireqs


conf = namedtuple('Config', 'dir_path python_version timeout')


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--pythonversion', nargs=1, type=str, default='3.5.2', help='python version to use for calculating dependencies')
@click.option('--dirpath', nargs=1, help="path to directory containing requirement files, defaults to PWD")
@click.option('--timeout', nargs=1, type=int, default=10, help="how long to wait for docker commands")
@click_log.simple_verbosity_option()
@click_log.init('cireqs.cli')
def cli(ctx, dirpath, pythonversion, timeout):
    ctx.obj = conf(
        python_version=pythonversion,
        dir_path=dirpath or getcwd(),
        timeout=timeout
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
        "v{}".format(cireqs.__version__), fg='red') + "\n"

    if ctx.invoked_subcommand is None:
        click.echo("\n".join([splash, ctx.get_help()]))
        return


@cli.command()
@click.argument('input_requirements_filename', nargs=1, type=str, default='requirements_to_expand.txt')
@click.argument('output_requirements_filename', nargs=1, type=str, default='requirements.txt')
@click.pass_obj
def expand_requirements(conf, output_requirements_filename, input_requirements_filename):
    '''Expand given requirements file by extending it using pip freeze

    args:

    input_requirements_filename: the requirements filename to expand

    output_requirements_filename: the output filename for the expanded
    requirements file
    '''

    cireqs.expand_requirements(
        requirements_filename=input_requirements_filename,
        expanded_requirements_filename=output_requirements_filename,
        **conf._asdict()
    )
    logger.info("{} expanded to {} using pip freeze".format(
        input_requirements_filename, output_requirements_filename))


@cli.command()
@click.argument('input_requirements_filename', nargs=1, type=str, default='requirements.txt')
@click.pass_obj
def verify_requirements(conf, input_requirements_filename):
    '''verifying that given requirements file is not missing any pins

    args:

    input_requirements_filename: requriements file to verify

    '''
    cireqs.check_if_requirements_are_up_to_date(
        requirements_filename=input_requirements_filename,
        **conf._asdict())
    logger.debug("Requirements are up to date")


if __name__ == "__main__":
    cli()