from unittest.mock import (
    patch, Mock
)
from getframeworkk8sapiversion.azure import AzureKubeCtlVersion
from pytest import raises
from msrestazure.azure_exceptions import CloudError
from requests import Response
from azure.core.exceptions import (
    ResourceNotFoundError,
    ClientAuthenticationError
)


class TestAzureKubeCtlVersion(object):
    def setup(self):
        self.azure_kubectl = AzureKubeCtlVersion(
            client_id='client_id',
            client_secret='secret',
            tenant_id='tenant',
            subscription_id='subscription',
            location='westus2'
        )

    @patch('azure.mgmt.containerservice.v2017_07_01.operations._container_services_operations.ContainerServicesOperations.list_orchestrators')
    @patch('azure.mgmt.containerservice.ContainerServiceClient')
    @patch('azure.identity.ClientSecretCredential')
    def test_get_orchestrators(
        self, mock_credential, mock_container_service, mock_ok
    ):
        expected_orchestrators = [
            {
                'orchestrator_version': '1.1.1',
                'orchestrator_type': 'Kubernetes'
            },
            {
                'orchestrator_version': '2.1.1',
                'orchestrator_type': 'Kubernetes'
            }
        ]
        mock_ok.return_value.orchestrators = expected_orchestrators
        assert self.azure_kubectl.get_orchestrators() == [
            {
                'orchestrator_version': '1.1.1',
                'orchestrator_type': 'Kubernetes'
            },
            {
                'orchestrator_version': '2.1.1',
                'orchestrator_type': 'Kubernetes'
            }
        ]

    @patch('getframeworkk8sapiversion.azure.AzureKubeCtlVersion.get_orchestrators')
    def test_get_latest_k8s_version(self, mock_get_orchestrators):
        orchestrator_mocked = Mock()
        orchestrator_mocked.orchestrator_version = '1.6.9'
        orchestrator_mocked.orchestrator_type = 'Kubernetes'
        orchestrator_mocked_b = Mock()
        orchestrator_mocked_b.orchestrator_version = '21.6.9'
        orchestrator_mocked_b.orchestrator_type = 'Kubernetes'

        mock_get_orchestrators.return_value = [
            orchestrator_mocked,
            orchestrator_mocked_b
        ]
        assert self.azure_kubectl.get_latest_k8s_version() == '21.6.9'

    @patch('azure.mgmt.containerservice.v2017_07_01.operations._container_services_operations.ContainerServicesOperations.list_orchestrators')
    @patch('azure.mgmt.containerservice.ContainerServiceClient')
    @patch('azure.identity.ClientSecretCredential')
    def test_get_orchestrators_raise_exception(
        self, mock_credential, mock_container_client,
        mock_list_orchestrators
    ):
        fake_response = Response()
        fake_response.message = 'foo'
        fake_response.status_code = 400
        fake_response.reason = 'Bad Request'
        mock_list_orchestrators.side_effect = CloudError(fake_response)
        with raises(Exception):
            assert self.azure_kubectl.get_orchestrators()

    @patch('logging.Logger.error')
    @patch('azure.mgmt.containerservice.v2017_07_01.operations._container_services_operations.ContainerServicesOperations.list_orchestrators')
    @patch('azure.mgmt.containerservice.ContainerServiceClient')
    @patch('azure.identity.ClientSecretCredential')
    def test_get_latest_k8s_version_raise_exception_auth(
        self, mock_credential, mock_container_client,
            mock_list_orchestrators, mock_log_error
    ):
        mock_list_orchestrators.side_effect = ClientAuthenticationError('foo')
        with raises(ClientAuthenticationError):
            self.azure_kubectl.get_orchestrators()
            assert mock_log_error.called
            mock_log_error.assert_called_with('foo')

    @patch('logging.Logger.error')
    @patch('azure.mgmt.containerservice.v2017_07_01.operations._container_services_operations.ContainerServicesOperations.list_orchestrators')
    @patch('azure.mgmt.containerservice.ContainerServiceClient')
    @patch('azure.identity.ClientSecretCredential')
    def test_get_latest_k8s_version_raise_exception_wrong_subscription(
        self, mock_credential, mock_container_client,
        mock_list_orchestrators, mock_log_error
    ):
        mock_list_orchestrators.side_effect = ResourceNotFoundError('foo')

        with raises(Exception):
            self.azure_kubectl.get_orchestrators()
            assert mock_log_error.called
