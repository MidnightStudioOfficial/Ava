import unittest
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

testmodules = [
    'tests.testChatbot',
    # 'tests.testOtherModule',
    # add more test modules here
]

suite = unittest.TestSuite()

for t in testmodules:
    suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

with ThreadPoolExecutor() as executor:
    results = list(tqdm(executor.map(unittest.TextTestRunner(verbosity=2).run, suite), total=suite.countTestCases()))
