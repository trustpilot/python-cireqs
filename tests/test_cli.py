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
                           ['--dirpath', test_dir_path, 'expand_requirements',
                            input_requirements_filename,
                            output_requirements_filename])

    asserted_output = ['click-log==0.1.8\n',
                       '## The following requirements were added by pip freeze:\n',
                       'click==6.7\n']
    print(result)
    assert result.exit_code == 0
    with open(os.path.join(test_dir_path, 'output_requirements_1.txt'), 'r') as output_requirements_file:
        output_requirements_file_lines = output_requirements_file.readlines()
        assert asserted_output == output_requirements_file_lines


def test_verify_requirements_with_error():
    requirements_filename = 'input_requirements_2.txt'
    runner = CliRunner()
    result = runner.invoke(cli,
                           ['--dirpath', test_dir_path, 'verify_requirements',
                            requirements_filename])
    assert result.exit_code == -1

@pytest.mark.skipif(sys.version_info < (3,3),
                    reason="requires python3")
def test_timeout_error():
    requirements_filename = 'input_requirements_3.txt'
    runner = CliRunner()
    result = runner.invoke(cli,
                           ['--dirpath', test_dir_path, '--timeout', 0, 'verify_requirements',
                            requirements_filename])
    assert result.exit_code == -1


def test_verify_requirements():
    requirements_filename = 'input_requirements_3.txt'
    runner = CliRunner()
    result = runner.invoke(cli,
                           ['--dirpath', test_dir_path, 'verify_requirements',
                            requirements_filename])
    assert result.exit_code == 0
