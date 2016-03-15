# The MIT License (MIT)
#
# Copyright (c) 2015 Richard Tuin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import yaml
import os
import click
import subprocess
from .version import __version__
from .osfilter import command_for_current_os

plafile = 'Plafile.yml'


@click.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True))
@click.argument('target', default='all')
@click.pass_context
def pla(context, target):
    click.echo(click.style('Pla ' + __version__ + ' by Richard Tuin - Coder\'s simplest workflow automation tool.'))

    if not os.path.exists(plafile):
        raise click.UsageError('Pla could not find a Plafile.yml in ' + os.getcwd())

    stream = open(plafile, 'r')
    pla_data = yaml.load(stream)
    stream.seek(0)
    pla_file_content = stream.read()
    stream.close()

    if not isinstance(pla_data, dict):
        raise click.UsageError('Plafile.yml does not contain any targets')

    pla_targets = {}
    using_descriptions = False
    for targetDef in pla_data:
        target_length = targetDef.find('[')
        target_name = targetDef
        target_arguments = []
        description = None
        for line in pla_file_content.split('\n'):
            if line.startswith(target_name) and line.find('#') > len(target_name):
                description = line[line.find('#') + 1:].strip()
                using_descriptions = True

        if target_length > 0:
            target_arguments = target_name[target_length + 1:-1].split(',')
            target_name = target_name[:target_length]

        pla_targets[target_name] = {
            'description': description,
            'arguments': target_arguments,
            'commands': pla_data[targetDef]
        }

    if using_descriptions:
        for plaTarget in pla_targets:
            if pla_targets[plaTarget]['description'] is None:
                pla_targets[plaTarget]['description'] = plaTarget + ' (no description)'

    if target not in pla_targets:
        raise click.BadParameter(
            'Target "' + target + '" not present in ' + plafile + '. \nValid targets are: ' + '\n    ' +
            ('\n    '.join(pla_targets.keys())))

    click.echo('\nRunning target "' + target + '":')

    target_runner = TargetRunner(pla_targets)
    run_result = target_runner.run(target, context.args)

    if run_result:
        context.exit(1)


class TargetRunner:
    def __init__(self, pla_targets):
        self.pla_targets = pla_targets

    def run(self, target, args, error=False):
        """

        :param target: string
        :param args: dict
        :param error:
        :return:
        """
        target_args = {}
        arg_no, cmd_no = 0, 0
        if len(self.pla_targets[target]['arguments']) > len(args):
            raise click.BadParameter('Not enough parameters given for target: ' + target)

        if self.pla_targets[target]['description'] is not None:
            click.secho('  ' + self.pla_targets[target]['description'], fg='white', dim=True)

        for arg_name in self.pla_targets[target]['arguments']:
            target_args[arg_name] = args[arg_no]
            arg_no += 1

        for raw_command in self.pla_targets[target]['commands']:
            cmd_no += 1
            command = command_for_current_os(raw_command)
            if not command:
                click.secho('    . ' + raw_command, fg='white', dim=True)
                continue

            for arg_name, argValue in target_args.iteritems():
                command = command.replace("%" + arg_name + "%", argValue)

            if command[:1] == '=':
                error = self.run(command[1:], args, error)
                if (self.pla_targets[target]['description'] and
                        cmd_no < len(self.pla_targets[target]['commands']) and
                        self.pla_targets[target]['commands'][cmd_no][:1] != '='):
                    click.secho('  ' + self.pla_targets[target]['description'] + ' (cont.)', fg='white', dim=True)
                continue

            if error:
                click.secho('    . ' + raw_command, fg='white', dim=True)
                continue

            raw_command = '    ' + u'\u231B'.encode('utf8') + ' ' + raw_command
            try:
                click.secho(raw_command, fg='white', dim=True, nl=False)
                subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)

                click.secho("\033[2K\r", nl=False)
                for i in range(len(raw_command) / click.get_terminal_size()[0]):
                    print "\b",
                    click.secho("\033[2K\r", nl=False)
                click.secho('    ' + u'\u2714'.encode('utf8') + ' ' + raw_command, fg='green')
            except subprocess.CalledProcessError as caught:
                click.secho("\033[2K\r", nl=False)
                for i in range(len(raw_command) / click.get_terminal_size()[0]):
                    print "\b",
                    click.secho("\033[2K\r", nl=False)

                click.secho('    ' + u'\u2718'.encode('utf8') + ' ' + raw_command + ':', fg='red')

                output = caught.output.splitlines()
                if len(output) == 0:
                    output = ['[no output]']

                click.secho('        ' + ('\n        '.join(output)), fg='red', dim=True)
                error = True
        return error
