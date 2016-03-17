# The MIT License (MIT)
#
# Copyright (c) 2016 Richard Tuin
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

from unittest import TestCase
import os
from pla.plafile_finder import find_pla_file


class TestFindPlaFile(TestCase):
    basepath = os.path.dirname(os.path.realpath(__file__)) + '/fixtures/test_find_pla_file'

    test_path_data = (
        dict(
            path=basepath,
            result=os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/Plafile.yml'
        ),
        dict(
            path=basepath + '/root_dir',
            result=basepath + '/root_dir/Plafile.yml'
        ),
        dict(
            path=basepath + '/root_dir/child-dir',
            result=basepath + '/root_dir/Plafile.yml'
        ),
        dict(
            path=basepath + '/root_dir/child-dir/child-of-child',
            result=basepath + '/root_dir/Plafile.yml'
        ),
    )

    def test_find_pla_file(self):
        for test in self.test_path_data:
            result = find_pla_file(test['path'], 'Plafile.yml')
            self.assertEqual(
                test['result'],
                result,
                test['result'] + ' != ' + result.__str__() + ' (for path "' + test['path'] + '")'
            )
