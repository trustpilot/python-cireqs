import tempfile
import os.path
from cireqs.cli import cli
from click.testing import CliRunner


def test_expand_requirements():
    with tempfile.NamedTemporaryFile(mode='w+t',
                                     dir='/tmp') as requirements_to_expand_file, \
            tempfile.NamedTemporaryFile(mode='w+t',
                                        dir='/tmp') as requirements_file:
        requirements_to_expand_file.writelines(['click-log==0.1.8'])
        requirements_to_expand_file.seek(0)

        dir_path, requirements_to_expand_filename = os.path.split(
            requirements_to_expand_file.name)

        requirements_filename = os.path.basename(requirements_file.name)
        runner = CliRunner()
        result = runner.invoke(cli,
                               ['--dirpath', dir_path, 'expand_requirements',
                                requirements_to_expand_filename,
                                requirements_filename])

        requirements_file.seek(0)

        asserted_output = ['click-log==0.1.8\n',
                           '## The following requirements were added by pip freeze:\n',
                           'click==6.7\n']
        expanded_requirements_file_lines = requirements_file.readlines()
        assert asserted_output == expanded_requirements_file_lines
        assert result.exit_code == 0


def test_verify_requirements():
    with tempfile.NamedTemporaryFile(mode='w+t',
                                     dir='/tmp') as requirements_file:
        requirements_file.writelines(['click-log==0.1.8\n',
                                      '## The following requirements were added by pip freeze:\n',
                                      'click==6.7\n'])
        requirements_file.seek(0)

        dir_path, requirements_filename = os.path.split(requirements_file.name)
        runner = CliRunner()
        result = runner.invoke(cli,
                               ['--dirpath', dir_path, 'verify_requirements',
                                requirements_filename])

        requirements_file.seek(0)

        asserted_output = ['click-log==0.1.8\n',
                           '## The following requirements were added by pip freeze:\n',
                           'click==6.7\n']
        expanded_requirements_file_lines = requirements_file.readlines()
        assert asserted_output == expanded_requirements_file_lines
        assert result.exit_code == 0
