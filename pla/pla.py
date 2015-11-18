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

import yaml, os, click, subprocess

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
    plaData = yaml.load(stream)

    if not isinstance(plaData, dict):
        raise click.UsageError('Plafile.yml does not contain any targets')

    plaTargets = {}
    for targetDef in plaData:
        targetLength = targetDef.find('[')
        targetName = targetDef
        targetArguments = []
        if targetLength > 0:
            targetArguments = targetName[targetLength+1:-1].split(',')
            targetName = targetName[:targetLength]
        plaTargets[targetName] = {'arguments': targetArguments, 'commands': plaData[targetDef]}

    if not target in plaTargets:
        raise click.BadParameter(
            'Target "' + target + '" not present in ' + plafile + '. \nValid targets are: ' + '\n    ' +
            ('\n    '.join(plaTargets.keys())))

    click.echo('\nRunning target "' + target + '":')

    targetRunner = TargetRunner(plaTargets)
    runResult = targetRunner.run(target, context.args)

    if runResult:
        context.exit(1)

class TargetRunner:
    def __init__(self, plafile):
        self.plafile = plafile

    def run(self, target, args, error=False):
        """

        :param target: string
        :param args: dict
        :param error:
        :return:
        """
        targetArgs = {}
        argNo = 0
        if len(self.plafile[target]['arguments']) > len(args):
            raise click.BadParameter('Not enough parameters given for target: ' + target)

        for argName in self.plafile[target]['arguments']:
            targetArgs[argName] = args[argNo]
            argNo += 1
        for rawCommand in self.plafile[target]['commands']:
            command = command_for_current_os(rawCommand)
            if not command:
                click.secho('    . ' + rawCommand, fg='white', dim=True)
                continue

            for argName, argValue in targetArgs.iteritems():
                command = command.replace("%" + argName + "%", argValue)

            if command[:1] == '=':
                error = self.run(command[1:], args, error)
                continue

            if error:
                click.secho('    . ' + rawCommand, fg='white', dim=True)
                continue

            raw_command = '    ' + u'\u231B'.encode('utf8') + ' ' + rawCommand
            try:
                click.secho(raw_command, fg='white', dim=True, nl=False)
                subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)

                click.secho("\033[2K\r", nl=False)
                for i in range(len(raw_command) / click.get_terminal_size()[0]):
                    print "\b",
                    click.secho("\033[2K\r", nl=False)
                click.secho('    ' + u'\u2714'.encode('utf8') + ' ' + rawCommand, fg='green')
            except subprocess.CalledProcessError as caught:
                click.secho("\033[2K\r", nl=False)
                for i in range(len(raw_command) / click.get_terminal_size()[0]):
                    print "\b",
                    click.secho("\033[2K\r", nl=False)

                click.secho('    ' + u'\u2718'.encode('utf8') + ' ' + rawCommand + ':', fg='red')

                output = caught.output.splitlines()
                if len(output) == 0:
                    output = ['[no output]']

                click.secho('        ' + ('\n        '.join(output)), fg='red', dim=True)
                error = True
        return error