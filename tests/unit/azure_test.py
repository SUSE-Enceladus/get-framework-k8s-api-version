from unittest.mock import (
    patch, Mock
)
from getframeworkk8sapiversion.azure import AzureKubeCtlVersion
import requests
from pytest import raises

class TestAzureKubeCtlVersion(object):
    def setup(self):
        self.azure_kubectl = AzureKubeCtlVersion(
            client_id='client_id',
            client_secret='secret',
            tenant_id='tenant',
            subscription_id='subscription',
            location='westus2'
        )

    @patch('requests.post')
    def test_get_access_token(self, mock_post_request):
        response_json = { 'access_token': 'foo' }
        mock_response = Mock()
        mock_post_request.return_value = mock_response
        mock_response.json.return_value = response_json
        assert self.azure_kubectl.get_access_token() == 'foo'


    @patch('getframeworkk8sapiversion.azure.AzureKubeCtlVersion.get_access_token')
    @patch('requests.get')
    def test_get_orchestrators(self, mock_get_request, mock_get_access_token):
        response_json = {
            'properties': {
                'orchestrators': [
                    {
                        'orchestratorType': 'Kubernetes',
                        'orchestratorVersion': '1.6.9'
                    }
                ]
            }
        }
        mock_response = Mock()
        mock_get_request.return_value = mock_response
        mock_response.json.return_value = response_json
        mock_get_access_token.return_value = 'foo'
        assert self.azure_kubectl.get_orchestrators() ==  [
            {
                'orchestratorType': 'Kubernetes',
                'orchestratorVersion': '1.6.9'
            }
        ]

    @patch('getframeworkk8sapiversion.azure.AzureKubeCtlVersion.get_access_token')
    @patch('getframeworkk8sapiversion.azure.AzureKubeCtlVersion.get_orchestrators')
    def test_get_latest_k8s_version(
        self, mock_get_orchestrators, mock_get_access_token
    ):
        orchestrators = [
            {
                'orchestratorType': 'Kubernetes',
                'orchestratorVersion': '1.6.9'
            }
        ]
        mock_get_orchestrators.return_value = orchestrators
        mock_get_access_token.return_value = 'foo;'

        assert self.azure_kubectl.get_latest_k8s_version() == '1.6.9'


    @patch('requests.post')
    def test_get_latest_k8s_version_raise_exception(
        self, mock_post_request
    ):
        mock_post_request.side_effect = requests.exceptions.RequestException
        with raises(requests.exceptions.RequestException):
            self.azure_kubectl.get_latest_k8s_version()

    @patch('requests.post')
    def test_get_latest_k8s_version_raise_exception_key(
        self, mock_post_request
    ):
        mock_response = Mock()
        mock_response.json.return_value = {'foo': 'bar'}
        mock_post_request.return_value = mock_response

        with raises(KeyError):
            self.azure_kubectl.get_latest_k8s_version()
