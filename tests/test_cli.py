import pytest
import os.path
import sys
from cireqs.cli import cli
from click.testing import CliRunner

test_dir_path = os.path.dirname(os.path.realpath(__file__))


def test_expand_requirements():

    input_requirements_filename = 'input_requirements_1.txt'
    output_requirements_filename = 'output_requirements_1.txt'

    runner = CliRunner()

    result = runner.invoke(cli,
                           ['-v','DEBUG','--dirpath', test_dir_path, 'expand',
                            input_requirements_filename,
                            output_requirements_filename])

    asserted_output = [
        'cireqs==1.0.4\n',
        '## The following requirements were added by pip freeze:\n',
        'click==6.7\n',
        'click-log==0.1.8\n'
    ]

    print(result.output)
    assert result.exit_code == 0
    with open(os.path.join(test_dir_path, 'output_requirements_1.txt'), 'r') as output_requirements_file:
        output_requirements_file_lines = output_requirements_file.readlines()
        assert asserted_output == output_requirements_file_lines


def test_verify_requirements_with_error():
    requirements_filename = 'input_requirements_2.txt'
    runner = CliRunner()
    result = runner.invoke(cli,
                           ['--dirpath', test_dir_path, 'verify',
                            requirements_filename])
    assert result.exit_code == -1

@pytest.mark.skipif(sys.version_info < (3,3),
                    reason="requires python3")
def test_timeout_error():
    requirements_filename = 'input_requirements_3.txt'
    runner = CliRunner()
    result = runner.invoke(cli,
                           ['--dirpath', test_dir_path, '--timeout', 0, 'verify',
                            requirements_filename])
    assert result.exit_code == -1


def test_verify_requirements_success():
    requirements_filename = 'input_requirements_3.txt'
    runner = CliRunner()
    result = runner.invoke(cli,
                           ['--dirpath', test_dir_path, 'verify',
                            requirements_filename])
    print(result.output)
    assert result.exit_code == 0

def test_expand_requirements_with_env_var():
    requirements_filename = 'input_requirements_3.txt'
    runner = CliRunner()
    result = runner.invoke(cli,
                           ['--dirpath', test_dir_path, '-e' 'foo=bar', '--dry','verify',
                            requirements_filename])
    assserted_docker_command_line  ='docker run --rm --name cireqs_container -e foo=bar -v'
    assert assserted_docker_command_line in result.output
    assert result.exit_code == 0


def test_missing_input_requirements_file():
    requirements_filename = 'not_existing.txt'
    runner = CliRunner()
    result = runner.invoke(cli,
                           ['--dirpath', test_dir_path, '-e' 'foo=bar', '--dry','verify',
                            requirements_filename])
    assert result.output.strip() == requirements_filename + ' does not exist'
    assert result.exit_code == -1

def test_wrong_python_version():
    requirements_filename = 'input_requirements_4.txt'
    runner = CliRunner()
    result = runner.invoke(cli,
                           ['--pythonversion','2.7','--dirpath', test_dir_path,'expand',
                            requirements_filename])
    assert result.output.strip() == "error: wrong python version, 'aiostream' requires:3.6, try setting --pythonversion to 3.6"
    assert result.exit_code == -1

def test_image_does_not_exist():
    requirements_filename = 'input_requirements_4.txt'
    runner = CliRunner()
    result = runner.invoke(cli,
                           ['--pythonversion','2.7.666','--dirpath', test_dir_path,'expand',
                            requirements_filename])
    assert result.output.strip() == "error: Couldn't pull image:python:2.7.666, does it exist?"
    assert result.exit_code == -1
