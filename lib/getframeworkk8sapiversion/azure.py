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

from packaging import version
from azure.identity import ClientSecretCredential
from azure.mgmt.containerservice import ContainerServiceClient
from msrestazure.azure_exceptions import CloudError
from azure.core.exceptions import (
    ResourceNotFoundError,
    ClientAuthenticationError
)


class AzureKubeCtlVersion(object):
    def __init__(
        self, client_id, client_secret, tenant_id, subscription_id, location
    ):
        self.location = location
        self.credential = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret
        )
        self.container_client = ContainerServiceClient(
            subscription_id=subscription_id,
            credential=self.credential
        )

    def get_orchestrators(self):
        try:
            return self.container_client.container_services.list_orchestrators(
                location=self.location
            ).orchestrators
        except CloudError as err:
            message = "Error trying to list orchestrators: {}".format(err)
            print(message)
            raise Exception(message) from err
        except ClientAuthenticationError as err:
            print(err)
            raise err
        except ResourceNotFoundError as err:
            message = "Resource not found: {}".format(err)
            print(message)
            raise Exception(message) from err

    def get_latest_k8s_version(self):
        orchestrators = self.get_orchestrators()
        return str(max([version.parse(x.orchestrator_version) for x in
                        orchestrators if x.orchestrator_type == 'Kubernetes']))
