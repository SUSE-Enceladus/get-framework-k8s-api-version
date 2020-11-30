#
# spec file for package python3-getkubectlversion
#
# Copyright (c) 2020 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


%define upstream_name get-framework-k8s-api-version
%define is_aws "%(if [ -e /sys/hypervisor/uuid ]; then grep -r ^ec2 /sys/hypervisor/uuid; else echo 0; fi)"


Name:           python3-get-framework-k8s-api-version
Version:        0.0.2
Release:        0
Summary:        latest version of k8s API server
License:        GPL-3.0+
Url:            https://github.com/SUSE-Enceladus/get-framework-k8s-api-version
Source0:        %{upstream_name}-%{version}.tar.bz2
Requires:       python3
Requires:       python3-requests
%if %{is_aws}
Requires:       python3-boto3
%endif
BuildRequires:  python3-setuptools
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch


%description
Command line tools for setting authorization credentials based on metadata
present in a public cloud VM instance.

%prep
%setup -q -n %{upstream_name}-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
mkdir -p %{buildroot}%{_sbindir}
mv %{buildroot}%{_bindir}/get-kubectl-version %{buildroot}%{_sbindir}/get-framework-k8s-api-version


%files
%defattr(-,root,root,-)
%doc README.md
%license LICENSE
%dir %{python3_sitelib}/get-framework-k8s-api-version
%{python3_sitelib}/*
%{_sbindir}/get-framework-k8s-api-version

%changelog
