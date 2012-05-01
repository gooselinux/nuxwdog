Name:           nuxwdog
Version:        1.0.1
Release:        1%{?dist}
Summary:        Watchdog server to start and stop processes, and prompt for passwords
# The entire source code is LGPLv2 except for the perl module, which is GPL+ or Artistic
License:        LGPLv2 and (GPL+ or Artistic)
Group:          System Environment/Libraries
URL:            http://www.redhat.com/certificate_system
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  ant
BuildRequires:  java-devel >= 1:1.6.0
BuildRequires:  jpackage-utils
BuildRequires:  nspr-devel
BuildRequires:  nss-devel
BuildRequires:  pkgconfig
BuildRequires:  libselinux-devel
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  keyutils-libs-devel

Requires:       nss
Requires:       keyutils-libs
Obsoletes:      nuxwdog-client
Obsoletes:      nuxwdog-client-perl

Source0:        https://fedorahosted.org/released/nuxwdog/%{name}-%{version}.tar.gz

# Note: there is an rpmlint warning about Nuxwdogclient.so being a private-shared-object-provide
# This would ordinarily be fixed by calling the macro perl_default_filter, but 
# this disables rpms file coloring and makes the package fail multilib tests.

%if 0%{?rhel}
ExcludeArch: ppc ppc64 s390 s390x
%endif

%description
The nuxwdog package supplies the nuxwdog watchdog daemon, 
used to start,stop, prompt for passwords and monitor processes.
It also contains C/C++ and Perl client code to allow clients to
interact with the nuxwdog watchdog daemon.

%package devel
Group:        Development/Libraries
Summary:      Development files for the Nuxwdog Watchdog
Requires:     %{name} = %{version}-%{release}
Obsoletes:    nuxwdog-client-devel

%description devel
The nuxwdog-devel package contains the header files needed to build clients
that call WatchdogClient functions, so that clients can interact with the
nuxwdog watchdog server.

%package client-java
Group:        System Environment/Libraries
Summary:      Nuxwdog Watchdog client JNI Package
Requires:     java >= 1:1.6.0
Requires:     jpackage-utils
Requires:     %{name} = %{version}-%{release}

%description client-java
The nuxwdog-client-java package contains a JNI interface to the nuxwdog 
client code, so that Java clients can interact with the nuxwdog watchdog 
server.


%prep
%setup -q -n %{name}-%{version}

%build
ant \
    -Dproduct.ui.flavor.prefix="" \
    -Dproduct.prefix="" \
    -Dproduct="nuxwdog" \
    -Dversion="%{version}"
%configure  --disable-static  \
%ifarch ppc64 s390x sparc64 x86_64
    --enable-64bit \
%endif
    --libdir=%{_libdir}
make

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="install -p"

find %{buildroot} -name '*.la' -exec rm -f {} ';'

mkdir -p  %{buildroot}%{_docdir}
mv %{buildroot}%{_usr}/doc %{buildroot}%{_docdir}/%{name}-%{version}

find %{buildroot}/%{perl_vendorarch} -name .packlist |xargs rm -f {}
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find %{buildroot} -name "perllocal.pod" |xargs rm -f {}
%{_fixperms} %{buildroot}/%{perl_vendorarch}/*

mkdir -p %{buildroot}/%{_libdir}/nuxwdog-jni
mv %{buildroot}/%{_libdir}/libnuxwdog-jni.so  %{buildroot}/%{_libdir}/nuxwdog-jni
mv %{buildroot}%{_usr}/jars/nuxwdog.jar %{buildroot}/%{_libdir}/nuxwdog-jni/nuxwdog-%{version}.jar
mkdir -p %{buildroot}%{_jnidir}
cd %{buildroot}/%{_jnidir}
ln -s %{_libdir}/nuxwdog-jni/nuxwdog-%{version}.jar nuxwdog.jar
rm -rf %{buildroot}%{_usr}/jars
rm -rf %{buildroot}%{_usr}/doc

%post -p /sbin/ldconfig 

%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root,-)
%doc LICENSE
%{_bindir}/*
%{_libdir}/libnuxwdog.so.*
%{_mandir}/man3/Nuxwdogclient.3pm*
%{_mandir}/man1/nuxwdog.1*
%{perl_vendorarch}/*
%exclude %dir %{perl_vendorarch}/auto/

%files devel
%defattr(-,root,root,-)
%doc 
%{_includedir}/nuxwdog/
%{_libdir}/libnuxwdog.so

%files client-java
%defattr(-,root,root,-)
%doc
%{_libdir}/nuxwdog-jni/
%{_jnidir}/*

%changelog
* Fri Jan 28 2011 Ade Lee <alee@redhat.com> 1.0.1-1
- Resolves: #643546 - [RFE] Add nuxwdog to RHEL.
- fix file coloring, aliasing problem

* Tue Jan 4 2011 Ade Lee <alee@redhat.com> 1.0.0-16
- Resolves: #643546 - [RFE] Add nuxwdog to RHEL.
- fix build problem

* Tue Jan 4 2011 Ade Lee <alee@redhat.com> 1.0.0-15
- Resolves: #643546 - [RFE] Add nuxwdog to RHEL.
- add needed build requires, requires

* Thu Dec 23 2010 Ade Lee <alee@redhat.com> 1.0.0-14
- Resolves: #643546 - [RFE] Add nuxwdog to RHEL.
- Remove old encryption scheme
- Store passwords in kernel keyring

* Wed Dec 16 2010 Ade Lee <alee@redhat.com> 1.0.0-13
- Resolves: #643546 - [RFE] Add nuxwdog to RHEL.

* Wed Dec 15 2010 Ade Lee <alee@redhat.com> 1.0.0-12
- Resolves: #643546 - [RFE] Add nuxwdog to RHEL. 

* Wed Dec 15 2010 Ade Lee <alee@redhat.com> 1.0.0-11
- Exclude arches for which there is no java

* Wed Dec 8 2010 Ade Lee <alee@redhat.com> 1.0.0-10
- Fixed copyright notices
- Removed versioning for requires
- Fixed library reference in perl build

* Tue Dec 7 2010 Ade Lee <alee@redhat.com> 1.0.0-9
- Fixed macros and copyrights
- Copyrights fixed for perl modules

* Fri Dec 3 2010 Ade Lee <alee@redhat.com> 1.0.0-8
- Spec file modified as per fedora review
- Copyrights fixed for perl modules

* Wed Dec 1 2010 Ade Lee <alee@redhat.com> 1.0.0-7
- Added missing build dependency on MakeMaker
- Removed extra config flags

* Tue Nov 30 2010 Ade Lee <alee@redhat.com> 1.0.0-6
- Restructure rpms
- Fix rpmlint issues

* Fri Sep 10 2010 Ade Lee <alee@redhat.com> 1.0.0-5
- Bumped version to match brew builds
- Bugzilla Bug 630115 - added printMessage() method
 
* Thu Feb 11 2010 Ade Lee <alee@redhat.com> 1.0.0-2
- Initial version in separated repo.

* Tue Dec 1 2009 Ade Lee <alee@redhat.com> 1.0.0-1
- Initial open source version based upon Red Hat
  Certificate System (RHCS) 6.1 uxwdog code.

