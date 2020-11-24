from getframeworkk8sapiversion.gce import GceKubeCtlVersion

class TestGceKubeCtlVersion(object):
    def test_get_latest_kubectl_version(self):
        self.gce_kubectl = GceKubeCtlVersion()
        self.gce_kubectl.get_latest_k8s_version()
