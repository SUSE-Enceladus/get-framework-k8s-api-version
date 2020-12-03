from unittest.mock import patch

import logging
import botocore
from azure.core.exceptions import ClientAuthenticationError

from getframeworkk8sapiversion.frameworkfactory import get_k8s_version

log = logging.getLogger('foo')

aws_dict = {
    'ec2_parser': True, 'aws_access_key_id': 'access_key',
    'aws_secret_access_key': 'secret',
    'region_name': 'eu-west-1'
}

azure_dict = {
    'az_parser': True, 'client_id': 'client_id',
    'client_secret': 'secret',
    'tenant_id': 'tenant',
    'subscription_id': 'subscription',
    'location': 'westus2'
}

gce_dict = {'gce_parser': True}


class TestGetKubeVersion(object):
    @patch('getframeworkk8sapiversion.azure.AzureKubeCtlVersion.get_latest_k8s_version')
    def test_get_k8s_version_azure(self, mock_az_kubectl):
        get_k8s_version(log, azure_dict)

    @patch('logging.Logger.error')
    @patch('azure.mgmt.containerservice.v2017_07_01.operations._container_services_operations.ContainerServicesOperations.list_orchestrators')
    @patch('azure.mgmt.containerservice.ContainerServiceClient')
    @patch('azure.identity.ClientSecretCredential')
    def test_get_latest_k8s_version_raise_exception(
        self, mock_credential, mock_container_client,
        mock_list_orchestrators, mock_log_error
    ):
        mock_list_orchestrators.side_effect = ClientAuthenticationError('foo')
        get_k8s_version(log, azure_dict)
        assert mock_log_error.called

    @patch('logging.Logger.error')
    @patch('boto3.client')
    def test_get_k8s_version_raise_exception(self, mock_boto3, mock_log_error):
        mock_boto3.return_value = mock_boto3
        mock_boto3.side_effect = botocore.exceptions.ClientError(
            error_response={'foo': 'foo'}, operation_name='bar'
        )
        get_k8s_version(log, aws_dict)
        assert mock_log_error.called

    @patch('getframeworkk8sapiversion.aws.AWSKubeCtlVersion.get_latest_k8s_version')
    @patch('boto3.client')
    def test_get_k8s_version(self, mock_boto3_client, mock_aws_kubectl):
        aws_data = {
            'Parameters': [
                {
                    'Name': '/aws/service/eks/optimized-ami/1/foo/bar',
                }
            ]
        }
        mock_boto3_client.return_value = mock_boto3_client
        mock_boto3_client.get_parameters_by_path.return_value = aws_data
        mock_aws_kubectl.return_value = 1

        assert get_k8s_version(log, aws_dict) == 1

    @patch('getframeworkk8sapiversion.gce.GceKubeCtlVersion.get_latest_k8s_version')
    def test_get_k8s_version_gce(self, mock_gce_latest_kubectl):
        mock_gce_latest_kubectl.side_effect = Exception
        get_k8s_version(log, gce_dict)

    @patch('getframeworkk8sapiversion.gce.GceKubeCtlVersion.get_latest_k8s_version')
    def test_get_k8s_version_gce_raise_exception(
        self, mock_gce_latest_kubectl
    ):
        mock_gce_latest_kubectl.side_effect = Exception
        assert get_k8s_version(log, {'gce_parser': True}) == None
