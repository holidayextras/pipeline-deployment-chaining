import sys
import unittest
import mox
import event_loader

sys.argv = [1, 2, 3, 4]
import circlestatus.check_circle_status as cs


# This method will be used by the mock to replace requests.get
def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, status_code):
            self.json_data = event_loader.sample_circle_response
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'http://someurl.com/test.json':
        return MockResponse(200)
    else:
        return MockResponse(200)

    return MockResponse({}, 404)


class Test_Generator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None

    def setUp(self):
        self.mox = mox.Mox()
        self.result = unittest.TestResult()
        self.argv = ['some/path', 'holidayextras', 'pipeline-controller-staging', 'xxxxxxxxxxxxxxxxxx']

        self.circle_response_sample = event_loader.sample_circle_response

    def tearDown(self):
        # In case one of our tests fail before UnsetStubs is called.
        self.mox.UnsetStubs()

    def test_circle_request(self):
        self.mox.StubOutWithMock(cs.requests, 'get')
        cs.requests.get(mox.IgnoreArg()).AndReturn(mocked_requests_get(200))
        self.mox.StubOutWithMock(cs.requests.Response, 'json')
        cs.requests.Response.json(mox.IgnoreArg()).AndReturn(self.circle_response_sample)
        self.mox.ReplayAll()

        circle_response = cs.circle_request()

        self.assertEqual(circle_response, self.circle_response_sample[0])
        self.tearDown()

    def test_circle_status(self):
        self.mox.StubOutWithMock(cs, 'circle_request')
        cs.circle_request().AndReturn(self.circle_response_sample[0])
        self.mox.ReplayAll()

        circle_status = cs.circle_status()

        self.assertEqual(circle_status, True)
        self.tearDown()

    def test_circle_status_empty_json(self):
        circle_request = {}
        self.mox.StubOutWithMock(cs, 'circle_request')
        cs.circle_request().AndReturn(circle_request)
        self.mox.ReplayAll()

        circle_status = cs.circle_status()

        self.assertIsNone(circle_status)
        self.tearDown()

    def test_circle_status_completed_status(self):
        circle_request = {"lifecycle": "successful", "outcome": "completed"}
        self.mox.StubOutWithMock(cs, 'circle_request')
        cs.circle_request().AndReturn(circle_request)
        self.mox.ReplayAll()

        circle_status = cs.circle_status()

        self.assertTrue(circle_status)
        self.tearDown()

    def test_circle_status_running_status(self):
        import circlestatus.check_circle_status as cs1

        circle_request = {"lifecycle": "running", "outcome": None}
        cs1.config_json_attempts = 3
        cs1.config_poll_tries = 5
        cs1.sleep_time = 2
        cs1.response_limit = '1'

        self.mox.StubOutWithMock(cs1, 'circle_request')
        cs1.circle_request().MultipleTimes().AndReturn(circle_request)
        self.mox.ReplayAll()

        circle_status = cs1.circle_status()

        self.assertIsNone(circle_status)
        self.tearDown()
