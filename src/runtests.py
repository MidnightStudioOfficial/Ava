import unittest

testmodules = [
    'tests.testChatbot',
    #'test.chatterbot_preprocessors'
 #   'tests.testOtherModule',
    # add more test modules here
]

suite = unittest.TestSuite()

for t in testmodules:
    suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

unittest.TextTestRunner().run(suite)
