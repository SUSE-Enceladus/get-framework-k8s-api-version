# Copyright 2020 SUSE LLC
#
# This file is part of getkubectlversion
#
# getkubectlversion is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# getkubectlversion is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# getkubectlversion. If not, see <http://www.gnu.org/licenses/>.

import botocore
import boto3


class AWSKubeCtlVersion(object):
    def __init__(
        self, aws_access_key_id, aws_secret_access_key, region_name
    ):
        try:
            self.ssm = boto3.client(
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=region_name,
                service_name='ssm'
            )
            self.parameters = self.ssm.get_parameters_by_path(
                Path='/aws/service/eks/optimized-ami',
                Recursive=True,
                ParameterFilters=[]
            )
        except botocore.exceptions.ParamValidationError as error:
            raise ValueError(error)
        except botocore.exceptions.ClientError as error:
            raise ValueError(error)

    def get_latest_k8s_version(self):
        next_token = True
        kube_versions = []
        while next_token:
            names = [param['Name'] for param in self.parameters.get('Parameters')]
            for name in names:
                version = name.split('/')[5]
                if version not in kube_versions:
                    kube_versions.append(version)

            self.parameters = self.ssm.get_parameters_by_path(
                Path='/aws/service/eks/optimized-ami',
                Recursive=True,
                ParameterFilters=[],
                NextToken=self.parameters.get('NextToken')
            )
            next_token = bool(self.parameters.get('NextToken'))
        list.sort(kube_versions)
        return kube_versions[-1]
