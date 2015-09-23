from alt import AltTest, request


class SampleSimpleTest:

    @AltTest
    def simple_test(self, expected_response_code, **kwargs):
        """
        Simple test.
        """
        response = request(**kwargs)
        assert response.status_code == expected_response_code