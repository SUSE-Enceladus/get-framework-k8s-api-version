# Copyright 2020 SUSE LLC
#
# This file is part of get-kubectl-version
#
# get-kubectl-version is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# get-kubectl-version is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# get-kubectl-version. If not, see <http://www.gnu.org/licenses/>.

def get_k8s_version(log, credentials):
    if credentials.get('az_parser'):
        from getframeworkk8sapiversion import azure

        azure_instance = azure.AzureKubeCtlVersion(
            client_id=credentials.get('client_id'),
            client_secret=credentials.get('client_secret'),
            tenant_id=credentials.get('tenant_id'),
            subscription_id=credentials.get('subscription_id'),
            location=credentials.get('location')
        )
        try:
            return azure_instance.get_latest_k8s_version()
        except Exception as err:
            log.error(err)
            return
    if credentials.get('ec2_parser'):
        from getframeworkk8sapiversion import aws

        try:
            return aws.AWSKubeCtlVersion(
                credentials.get('aws_access_key_id'),
                credentials.get('aws_secret_access_key'),
                credentials.get('region_name'),
            ).get_latest_k8s_version()
        except Exception as err:
            log.error(err)
            print(err)
            return
    else:
        from getframeworkk8sapiversion import gce

        try:
            return gce.GceKubeCtlVersion().get_latest_kubectl_version()
        except Exception:
            return None
