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

import requests
from packaging import version


class AzureKubeCtlVersion(object):
    def __init__(
        self, client_id, client_secret, tenant_id, subscription_id, location
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.subscription_id = subscription_id
        self.location = location

    def get_access_token(self):
        url = 'https://login.microsoftonline.com/{}/oauth2/token'.format(
            self.tenant_id
        )
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
            "resource": "https://management.azure.com"
        }
        response = requests.post(url, data=data)
        return response.json()['access_token']

    def get_orchestrators(self):
        self.access_token = self.get_access_token()
        url_kubeversions = "https://management.azure.com/subscriptions/" \
            "{subscription}/providers/Microsoft.ContainerService/locations/" \
            "{location}/orchestrators?api-version=2019-08-01".format(
                subscription=self.subscription_id,
                location=self.location
            )
        bearer_token = {"Authorization": 'Bearer {}'.format(self.access_token)}
        response = requests.get(url_kubeversions, headers=bearer_token)
        return response.json()['properties']['orchestrators']

    def get_latest_k8s_version(self):
        try:
            self.orchestrators = self.get_orchestrators()
            k8s_version = '0'
            for elem in self.orchestrators:
                fetched_ver = elem['orchestratorVersion']
                needs_update = (
                    elem['orchestratorType'] == 'Kubernetes'
                    and version.parse(fetched_ver) > version.parse(k8s_version)
                )
                if needs_update:
                    k8s_version = fetched_ver

            return k8s_version
        except requests.exceptions.RequestException as err:
            raise err
        except KeyError as err:
            raise err
