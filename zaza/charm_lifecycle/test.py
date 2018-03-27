import argparse
import logging
import unittest
import sys

import zaza.charm_lifecycle.utils as utils


def run_test_list(tests):
    """Run the tests as defined in the list of test classes in series.

    :param tests: List of test class strings
    :type tests: ['zaza.charms_tests.svc.TestSVCClass1', ...]
    :raises: AssertionError if test run fails
    """
    for _testcase in tests:
        testcase = utils.get_class(_testcase)
        suite = unittest.TestLoader().loadTestsFromTestCase(testcase)
        test_result = unittest.TextTestRunner(verbosity=2).run(suite)
        assert test_result.wasSuccessful(), "Test run failed"


def test(tests):
    """Run all steps to execute tests against the model"""
    run_test_list(tests)


def parse_args(args):
    """Parse command line arguments

    :param args: List of configure functions functions
    :type list: [str1, str2,...] List of command line arguments
    :returns: Parsed arguments
    :rtype: Namespace
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--tests', nargs='+',
                        help='Space sperated list of test classes',
                        required=False)
    return parser.parse_args(args)


def main():
    """Run the tests defined by the command line args or if none were provided
       read the tests from the charms tests.yaml config file"""
    logging.basicConfig(level=logging.INFO)
    args = parse_args(sys.argv[1:])
    tests = args.tests or utils.get_charm_config()['tests']
    test(tests)
