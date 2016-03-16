from unittest import TestCase

from pla.osfilter import command_for_current_os


class TestCommandForCurrentOs(TestCase):

    test_command_os_data = (
        dict(
            command='(darwin) echo "Mac OS"',
            os='Darwin-15.3.0-x86_64-i386-64bit',
            expected='echo "Mac OS"'
        ),
        dict(
            command='(darwin) echo "Mac OS"',
            os='Windows-2008ServerR2-6.1.7600',
            expected=False
        ),
        dict(
            command='(darwin) echo "Mac OS"',
            os='Linux-2.6.18-194.3.1.el5-i686-with-redhat-5.5-Final',
            expected=False
        ),
        dict(
            command='(darwin) echo "Mac OS"',
            os='Linux-3.13.0-74-generic-x86_64-with-Ubuntu-14.04-trusty',
            expected=False
        ),
        dict(
            command='(darwin) echo "Mac OS"',
            os='Linux-3.16.0-4-amd64-x86_64-with-debian-8.3',
            expected=False
        ),

        dict(
            command='(redhat) echo "RedHat family"',
            os='Darwin-15.3.0-x86_64-i386-64bit',
            expected=False
        ),
        dict(
            command='(redhat) echo "RedHat family"',
            os='Windows-2008ServerR2-6.1.7600',
            expected=False
        ),
        dict(
            command='(redhat) echo "RedHat family"',
            os='Linux-2.6.18-194.3.1.el5-i686-with-redhat-5.5-Final',
            expected='echo "RedHat family"'
        ),
        dict(
            command='(redhat) echo "RedHat family"',
            os='Linux-3.13.0-74-generic-x86_64-with-Ubuntu-14.04-trusty',
            expected=False
        ),
        dict(
            command='(redhat) echo "RedHat family"',
            os='Linux-3.16.0-4-amd64-x86_64-with-debian-8.3',
            expected=False
        ),

        dict(
            command='(ubuntu|darwin) echo "Ubuntu or Mac OS"',
            os='Darwin-15.3.0-x86_64-i386-64bit',
            expected='echo "Ubuntu or Mac OS"'
        ),
        dict(
            command='(ubuntu|darwin) echo "Ubuntu or Mac OS"',
            os='Windows-2008ServerR2-6.1.7600',
            expected=False
        ),
        dict(
            command='(ubuntu|darwin) echo "Ubuntu or Mac OS"',
            os='Linux-2.6.18-194.3.1.el5-i686-with-redhat-5.5-Final',
            expected=False
        ),
        dict(
            command='(ubuntu|darwin) echo "Ubuntu or Mac OS"',
            os='Linux-3.13.0-74-generic-x86_64-with-Ubuntu-14.04-trusty',
            expected='echo "Ubuntu or Mac OS"'
        ),
        dict(
            command='(ubuntu|darwin) echo "Ubuntu or Mac OS"',
            os='Linux-3.16.0-4-amd64-x86_64-with-debian-8.3',
            expected=False
        ),

        dict(
            command='(debian) echo "Debian"',
            os='Darwin-15.3.0-x86_64-i386-64bit',
            expected=False
        ),
        dict(
            command='(debian) echo "Debian"',
            os='Windows-2008ServerR2-6.1.7600',
            expected=False
        ),
        dict(
            command='(debian) echo "Debian"',
            os='Linux-2.6.18-194.3.1.el5-i686-with-redhat-5.5-Final',
            expected=False
        ),
        dict(
            command='(debian) echo "Debian"',
            os='Linux-3.13.0-74-generic-x86_64-with-Ubuntu-14.04-trusty',
            expected=False
        ),
        dict(
            command='(debian) echo "Debian"',
            os='Linux-3.16.0-4-amd64-x86_64-with-debian-8.3',
            expected='echo "Debian"'
        )
    )

    def test_command_for_current_os(self):
        for test in self.test_command_os_data:
            self.assertEqual(command_for_current_os(test['command'], test['os']), test['expected'])