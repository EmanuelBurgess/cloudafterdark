import mock
from mock import MagicMock
import unittest
import api_generate
import json


class TestCheckJwt(unittest.TestCase):

    def test_ado_jwt(self):
        mock_event = {
            "pathParameters": {
                "subject": "TEST:DentalAdju:01"
            },
            "requestContext": {
                "identity": {
                    "userArn": "arn:aws:blahblah/ado-prod-da-admin/AB23"
                }
            }
        }

        mock_jwt = "abcd.1234.xyz="
        mocklib = MagicMock()
        mocklib.return_value.generate_jwt.return_value = mock_jwt
        with mock.patch('mpse_jwt_generator.MpseJwtGenerator', mocklib):
            response = api_generate.handler(mock_event, {})

        self.assertEqual(json.loads(response["body"])["jwt"], mock_jwt)

    def test_pvt_dev_ado(self):
        mock_event = {
            "pathParameters": {
                "subject": "TEST:DentalAdju:01"
            },
            "requestContext": {
                "identity": {
                    "userArn": "arn:aws:blahblah/ado-dev-da-admin/AB23"
                }
            }
        }

        mock_jwt = "abcd.1234.xyz="
        mocklib = MagicMock()
        mocklib.return_value.generate_jwt.return_value = mock_jwt
        with mock.patch('mpse_jwt_generator.MpseJwtGenerator', mocklib):
            response = api_generate.handler(mock_event, {})

        self.assertEqual(json.loads(response["body"])["jwt"], mock_jwt)

    def test_osre_jwt(self):
        mock_event = {
            "pathParameters": {
                "subject": "MPSM:DentalBene:01"
            },
            "requestContext": {
                "identity": {
                    "userArn": "arn:aws:blahblah/ct-ado-mpsm-poweruser/AB23"
                }
            }
        }
        mock_jwt = "abcd.1234.xyz="
        mocklib = MagicMock()
        mocklib.return_value.generate_jwt.return_value = mock_jwt
        with mock.patch('mpse_jwt_generator.MpseJwtGenerator', mocklib):
            response = api_generate.handler(mock_event, {})

        self.assertEqual(json.loads(response["body"])["jwt"], mock_jwt)

    def test_unknown_ado_error(self):
        mock_event = {
            "pathParameters": {
                "subject": "TEST:DentalAdju:01"
            },
            "requestContext": {
                "identity": {
                    "userArn": "arn:aws:blahblah/xyz-admin/AB23"
                }
            }
        }

        mock_jwt = "abcd.1234.xyz="
        mocklib = MagicMock()
        mocklib.return_value.generate_jwt.return_value = mock_jwt
        with mock.patch('mpse_jwt_generator.MpseJwtGenerator', mocklib):
            response = api_generate.handler(mock_event, {})

        self.assertEqual(response["statusCode"], 403)

    def test_unauthorized_ado_error(self):
        mock_event = {
            "pathParameters": {
                "subject": "TEST:DentalBene:01"
            },
            "requestContext": {
                "identity": {
                    "userArn": "arn:aws:blahblah/ado-prod-da-admin/AB23"
                }
            }
        }

        mock_jwt = "abcd.1234.xyz="
        mocklib = MagicMock()
        mocklib.return_value.generate_jwt.return_value = mock_jwt
        with mock.patch('mpse_jwt_generator.MpseJwtGenerator', mocklib):
            response = api_generate.handler(mock_event, {})

        self.assertEqual(response["statusCode"], 403)

    def test_lib_exception_error(self):
        mock_event = {
            "pathParameters": {
                "subject": "TEST:DentalAdju:01"
            },
            "requestContext": {
                "identity": {
                    "userArn": "arn:aws:blahblah/ado-prod-da-admin/AB23"
                }
            }
        }

        mocklib = MagicMock()
        mocklib.return_value.generate_jwt.side_effect = Exception(
            "a very good reason")

        with mock.patch('mpse_jwt_generator.MpseJwtGenerator', mocklib):
            response = api_generate.handler(mock_event, {})

        self.assertEqual(response["statusCode"], 400)
        self.assertTrue("a very good reason" in json.loads(
            response["body"])["message"])


if __name__ == '__main__':
    unittest.main()
