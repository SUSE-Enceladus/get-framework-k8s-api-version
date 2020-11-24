from unittest.mock import patch
from pytest import raises
import botocore

from getframeworkk8sapiversion.aws import AWSKubeCtlVersion

class TestAWSKubeCtlVersion(object):
    @patch('boto3.client')
    def setup(self, mock_boto3_client):
        aws_data = {
            'Parameters': [
                {
                    'Name': '/aws/service/eks/optimized-ami/1.11/foo/bar',
                    'Type': 'String',
                    'Value': '{"schema_version":"1","image_id":"ami-1234", "image_name":"amazon-eks-arm64-node-1.11-v20191119"}',
                    'Version': 1
                }
            ]
        }
        mock_boto3_client.return_value = mock_boto3_client
        mock_boto3_client.get_parameters_by_path.return_value = aws_data
        self.aws_kubectl = AWSKubeCtlVersion(
            aws_access_key_id='access_key',
            aws_secret_access_key='secret_access',
            region_name='eu-west-1'
        )

    def test_get_latest_kubectl_version(self):
        assert self.aws_kubectl.get_latest_k8s_version() == '1.11'

    @patch('boto3.client')
    def test_raise_client_exception(self, mock_boto3_client):
        mock_boto3_client.return_value = mock_boto3_client
        mock_boto3_client.side_effect = botocore.exceptions.ClientError(
            error_response={'foo': 'foo'}, operation_name='bar'
        )
        with raises(ValueError):
            AWSKubeCtlVersion(
                aws_access_key_id='access_key',
                aws_secret_access_key='secret_access',
                region_name='eu-west-1'
            )

    @patch('boto3.client')
    def test_raise_param_validation_exception(self, mock_boto3_client):
        mock_boto3_client.return_value = mock_boto3_client
        mock_boto3_client.get_parameters_by_path.side_effect = botocore.exceptions.ParamValidationError(report='foo')
        with raises(ValueError):
            AWSKubeCtlVersion(
                aws_access_key_id='access_key',
                aws_secret_access_key='secret_access',
                region_name='eu-west-1'
            )
