%define release_name Parsidora
%define dist_version 13

Summary:	Parsidora release files
Name:		parsidora-release
Version:	13
Release:	2
License:	GPLv2
Group:		System Environment/Base
Source:		%{name}-%{version}.tar.bz2
Obsoletes:	redhat-release
Provides:	redhat-release = %{version}-%{release}
Provides:	system-release = %{version}-%{release}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
Conflicts:	fedora-release
Conflicts:	generic-release

%description
Parsidora release files such as yum configs and various /etc/ files that
define the release.

%package rawhide
Summary:        Rawhide repo definitions
Requires:	parsidora-release = %{version}-%{release}
Conflicts:	fedora-release-rawhide
Conflicts:      generic-release-rawhide

%description rawhide
This package provides the rawhide repo definitions.

%package notes
Summary:	Release Notes
License:	Open Publication
Group:		System Environment/Base
Provides:	system-release-notes = %{version}-%{release}
Conflicts:	fedora-release-notes
Conflicts:	generic-release-notes

%description notes
Parsidora release notes package.

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc
echo "Parsidora release %{version} (%{release_name})" > $RPM_BUILD_ROOT/etc/fedora-release
echo "cpe://o:parsidora:parsidora:%{version}" > $RPM_BUILD_ROOT/etc/system-release-cpe
cp -p $RPM_BUILD_ROOT/etc/fedora-release $RPM_BUILD_ROOT/etc/issue
echo "Kernel \r on an \m (\l)" >> $RPM_BUILD_ROOT/etc/issue
cp -p $RPM_BUILD_ROOT/etc/issue $RPM_BUILD_ROOT/etc/issue.net
echo >> $RPM_BUILD_ROOT/etc/issue
ln -s fedora-release $RPM_BUILD_ROOT/etc/redhat-release
ln -s fedora-release $RPM_BUILD_ROOT/etc/system-release

install -d -m 755 $RPM_BUILD_ROOT/etc/pki/rpm-gpg

install -m 644 RPM-GPG-KEY* $RPM_BUILD_ROOT/etc/pki/rpm-gpg/

# Install all the keys, link the primary keys to primary arch files
# and to compat parsidora location
pushd $RPM_BUILD_ROOT/etc/pki/rpm-gpg/
for arch in i386 x86_64 ppc ppc64
  do
  ln -s RPM-GPG-KEY-fedora-%{dist_version}-primary RPM-GPG-KEY-fedora-$arch
done
ln -s RPM-GPG-KEY-fedora-%{dist_version}-primary RPM-GPG-KEY-fedora
popd

install -d -m 755 $RPM_BUILD_ROOT/etc/yum.repos.d
for file in fedora*repo ; do
  install -m 644 $file $RPM_BUILD_ROOT/etc/yum.repos.d
done

install -m 644 parsidora-dvd.repo $RPM_BUILD_ROOT/etc/yum.repos.d

# Set up the dist tag macros
install -d -m 755 $RPM_BUILD_ROOT/etc/rpm
cat >> $RPM_BUILD_ROOT/etc/rpm/macros.dist << EOF
# dist macros.

%%fedora		%{dist_version}
%%dist		.fc%{dist_version}
%%fc%{dist_version}		1
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc GPL 
%config %attr(0644,root,root) /etc/fedora-release
/etc/redhat-release
/etc/system-release
%config %attr(0644,root,root) /etc/system-release-cpe
%dir /etc/yum.repos.d
%config(noreplace) /etc/yum.repos.d/fedora.repo
%config(noreplace) /etc/yum.repos.d/fedora-updates*.repo
%config(noreplace) /etc/yum.repos.d/parsidora-dvd.repo
%config(noreplace) %attr(0644,root,root) /etc/issue
%config(noreplace) %attr(0644,root,root) /etc/issue.net
%config %attr(0644,root,root) /etc/rpm/macros.dist
%dir /etc/pki/rpm-gpg
/etc/pki/rpm-gpg/*

%files notes
%defattr(-,root,root,-)
%doc README.Parsidora-Release-Notes

%files rawhide
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/fedora-rawhide.repo

%changelog
* Fri Jul 02 2010 Hedayat Vatankhah <hedayat@fedorapeople.org> 13.0-2
- Added parsidora-dvd.repo to the package!

* Sat May 15 2010 Hedayat Vatankhah <hedayat@grad.com> 13.0-1
- Updated for Fedora 13 based release

* Tue Jan 26 2010 Hedayat Vatankhah <hedayat@grad.com> 12.0-1
- Initial package for parsidora-release and parsidora-release-notes, forked
  from generic packages

