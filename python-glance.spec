%define bzr_rev 86
%define module	glance
%define	rel		3
%if %mdkversion < 201100
%define release %mkrel %{rel}
%else
%define	release	%{rel}
%endif

Name:           python-%module
Version:        2011.1.%{bzr_rev}
Release:        %{release}
Summary:        Discover, Register and Retrieve virtual machine images
License:        Apache Software Licene
Group:          Development/Python
Url:            http://glance.openstack.org/
Source:         http://hudson.openstack.org/job/glance-tarball/lastSuccessfulBuild/artifact/dist/glance-2011.2~bzr%{bzr_rev}.tar.gz
Source1:        glance.init
Source2:        glance.sysconfig
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  python-setuptools
Buildrequires:	python-sphinx
BuildRequires:  python-devel
Requires:       python-cheetah python-gflags python-daemon python-routes
Requires:       python-eventlet python-webob python-sqlalchemy python-mysql
%if %mdkversion < 201100
Requires:		python-argparse
%endif
Provides:	openstack-glance

%description
The Glance project provides services for discovering, registering,
and retrieving virtual machine images. Glance has a RESTful API
that allows querying of VM image metadata as well as retrieval
of the actual image.

%prep
%setup -q -n %{module}-2011.2

%build
CFLAGS="%{optflags}" python setup.py build

%install
mkdir -p %{buildroot}%{_initrddir}/
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
%{__python} setup.py install --root $RPM_BUILD_ROOT --install-purelib=%{python_sitearch}
install -D -m 0755 %{SOURCE1} %{buildroot}%{_initrddir}/openstack-glance
install -D -m 0644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/sysconfig/sysconfig.openstack-glance

%post
%_post_service openstack-glance

%preun
%_preun_service openstack-glance


%files 
%defattr(-,root,root)
%doc ChangeLog README
%{_bindir}/%{module}*
%{python_sitearch}/*
%{_initrddir}/openstack-glance
%{_sysconfdir}/sysconfig/sysconfig.openstack-glance

