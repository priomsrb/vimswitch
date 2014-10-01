import unittest
import textwrap


class BaseTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)

        # Python < 3.2 does not have assertNotRegex
        if not hasattr(self, 'assertNotRegex'):
            self.assertNotRegex = self.assertNotRegexpMatches

    def assertMultilineRegexpMatches(self, string, regexp):
        """
        Asserts that the entirety of `string` matches `regexp`. `regexp` can be
        a multiline string with indentation.
        """
        regexp = textwrap.dedent(regexp)
        regexp = regexp.strip()
        regexp = '^' + regexp + '$'
        self.assertRegexpMatches(string, regexp)

    def assertStdout(self, stdout, regex):
        "Asserts that the `stdout` io stream matches `regex`"
        self.assertMultilineRegexpMatches(stdout.getvalue(), regex)
