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
from runners import TargetRunner

plafile = 'Plafile.yml'

@click.command()
@click.argument('target', default='all')
@click.pass_context
def pla(context, target):
    click.echo(click.style('Pla 0.2.0 by Richard Tuin - Make, but with a yaml file'));
    """Pla 0.2.0 by Richard Tuin - Make, but with a yaml file"""

    if not os.path.exists(plafile):
        raise click.UsageError('Pla could not find a Plafile.yml in ' + os.getcwd())

    stream = open(plafile, 'r')
    plaData = yaml.load(stream)

    if not isinstance(plaData, dict):
        raise click.UsageError('Plafile.yml does not contain any targets')

    if not target in plaData:
        raise click.UsageError('Target "' + target + '" not present in ' + plafile)

    click.echo('\nRunning target "' + target + '":')

    targetRunner = TargetRunner(plaData)
    runResult = targetRunner.run(target)

    if runResult:
        context.exit(1);

if __name__ == '__main__':
    pla()
