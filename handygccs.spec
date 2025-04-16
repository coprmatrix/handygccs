Name:           HandyGCCS
%global _servicename handycon
Version:        2.0.0
Release:        3%{?dist}
Summary:        Handheld Game Console Controller Support (Handy Geeks) for Linux

License:        GPL-v3
URL:            https://github.com/ShadowBlip/%{name}
Source:         %{name}-%{version}.tar.xz
Patch0:         0001-fedora.patch

%define python_module() python3-%{1}

BuildArch:      noarch
Requires:       systemd
Requires:       udev
BuildRequires:  %{python_module devel}
BuildRequires:  %{python_module build}
BuildRequires:  %{python_module installer}
BuildRequires:  %{python_module setuptools}
BuildRequires:  %{python_module wheel}
BuildRequires:  python-rpm-macros
Provides:       handygccs

%description
Handheld Game Console Controller Support (Handy Geeks) for Linux

%prep
%setup -n %{name}-%{version}
%patch 0

%build
python3 -m build --wheel --no-isolation

%install
python3 -m installer dist/*.whl --destdir=%{buildroot}
cp -r usr/ %{buildroot}/

%pre
%systemd_pre %{_servicename}.service

%post
%systemd_post %{_servicename}.service
if [ -x /usr/bin/systemd-hwdb ]; then
    /usr/bin/systemd-hwdb update
fi
if [ -x /usr/bin/udevadm ]; then
    /usr/bin/udevadm control -R
fi

%preun
%systemd_preun %{_servicename}.service

%postun
%systemd_postun_with_restart %{_servicename}.service


%files
%{_bindir}/handycon
%{python3_sitelib}/%{_servicename}
%{python3_sitelib}/%{_servicename}-2.0.0.dist-info
%{_prefix}/lib/systemd/system/handycon.service
%{_prefix}/lib/udev/hwdb.d/59-handygccs-ayaneo.hwdb
%{_prefix}/lib/udev/rules.d/60-handycon.rules
%{_datadir}/handygccs/scripts/capture-system.py
%dir %{_prefix}/lib/udev/hwdb.d
%dir %{_datadir}/handygccs
%dir %{_datadir}/handygccs/scripts
