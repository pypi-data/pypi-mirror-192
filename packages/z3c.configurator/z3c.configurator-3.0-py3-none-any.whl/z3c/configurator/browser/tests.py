import doctest
import unittest

import z3c.configurator.browser


try:
    from zope.app.wsgi import testlayer
    HAVE_FTEST = True
except ImportError:
    HAVE_FTEST = False

TestLayer = None
if HAVE_FTEST:
    TestLayer = testlayer.BrowserLayer(
        z3c.configurator.browser, 'ftesting.zcml')


def setUp(test):
    """Setup a reasonable environment for the category tests"""
    pass


def tearDown(test):
    pass


def test_suite():
    suite = unittest.TestSuite()
    if HAVE_FTEST:
        suites = (
            doctest.DocFileSuite(
                'README.txt', setUp=setUp, tearDown=tearDown,
                globs={'layer': TestLayer}
            ),
        )
        for s in suites:
            s.layer = TestLayer
            suite.addTest(s)
    return suite
