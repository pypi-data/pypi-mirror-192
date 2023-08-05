"""
    Turbinia API Server

    Turbinia API server  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""


import unittest

import turbinia_api_lib
from turbinia_api_lib.api.turbinia_configuration_api import TurbiniaConfigurationApi  # noqa: E501


class TestTurbiniaConfigurationApi(unittest.TestCase):
    """TurbiniaConfigurationApi unit test stubs"""

    def setUp(self):
        self.api = TurbiniaConfigurationApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_evidence_attributes_by_name(self):
        """Test case for get_evidence_attributes_by_name

        Get Evidence Attributes By Name  # noqa: E501
        """
        pass

    def test_get_evidence_types(self):
        """Test case for get_evidence_types

        Get Evidence Types  # noqa: E501
        """
        pass

    def test_get_request_options(self):
        """Test case for get_request_options

        Get Request Options  # noqa: E501
        """
        pass

    def test_read_config(self):
        """Test case for read_config

        Read Config  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
