%global _enable_debug_package 0
%global debug_package %{nil}
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}


Name:			fastdfs
Version:		5.09
Release:		1%{?dist}
Summary:		FastDFS server and client
License:		GPL
Group:			Arch/Tech
URL:			https://github.com/happyfish100/fastdfs

BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 

Source0:		%{name}-%{version}.tar.gz
Source1:		fastdfs-trackerd.service
Source2:		fastdfs-storaged.service
Source3:		fastdfs-trackerd.init
Source4:		fastdfs-storaged.init
Source5:		fastdfs-tracker.conf
Source6:		fastdfs-storage.conf
Source7:		fastdfs-client.conf
Source8:		http.conf

BuildRequires:		gcc
BuildRequires:		glibc-devel
BuildRequires:		libtool
BuildRequires:		make
BuildRequires:		perl,gawk
BuildRequires:		libfastcommon-devel >= 1.0.35

%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
BuildRequires:		systemd-units
Requires:		systemd
%endif

Requires:		libfastcommon >= 1.0.35

Requires(post):		chkconfig

%description
This package provides tracker & storage of fastdfs

%package		tracker
Summary:		fastdfs tracker
Requires:		fastdfs

%package		storage
Summary:		fastdfs storage
Requires:		fastdfs

%package		tool
Summary:		fastdfs tools
Requires:		fastdfs

%package		-n libfdfsclient
Summary:		The client dynamic library of fastdfs
Requires:		fastdfs

%package		-n libfdfsclient-devel
Summary:		The client header of fastdfs
Requires:		libfdfsclient

%description tracker
This package provides tracker of fastdfs

%description storage
This package provides storage of fastdfs

%description -n libfdfsclient
This package is client dynamic library of fastdfs

%description -n libfdfsclient-devel
This package is client header of fastdfs client

%description tool
This package is tools for fastdfs

%prep
%setup -q

%build
./make.sh

%install
rm -rf %{buildroot}
DESTDIR=$RPM_BUILD_ROOT ./make.sh install

%{__mkdir} -p $RPM_BUILD_ROOT%{_bindir}
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/fdfs
%{__mkdir} -p $RPM_BUILD_ROOT%{_datadir}/fastdfs/php-client
%{__mkdir} -p $RPM_BUILD_ROOT%{_sharedstatedir}/fastdfs/{client,storage,tracker}

%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%{__install} -p -m 755 %{SOURCE3} $RPM_BUILD_ROOT%{_initrddir}/fastdfs-trackerd
%{__install} -p -m 755 %{SOURCE4} $RPM_BUILD_ROOT%{_initrddir}/fastdfs-storaged

rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/init.d/fdfs_storaged 
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/init.d/fdfs_trackerd
rm -rf $RPM_BUILD_ROOT%{_bindir}/restart.sh
rm -rf $RPM_BUILD_ROOT%{_bindir}/stop.sh

rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/fdfs
cp -a conf $RPM_BUILD_ROOT%{_sysconfdir}/fdfs

#rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/fdfs/tracker.conf
#rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/fdfs/storage.conf

%{__install} -p -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/fdfs/tracker.conf
%{__install} -p -m 644 %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/fdfs/storage.conf
%{__install} -p -m 644 %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/fdfs/client.conf
%{__install} -p -m 644 %{SOURCE8} $RPM_BUILD_ROOT%{_sysconfdir}/fdfs/http.conf


mv $RPM_BUILD_ROOT%{_bindir}/fdfs_trackerd $RPM_BUILD_ROOT%{_bindir}/fastdfs-trackerd
mv $RPM_BUILD_ROOT%{_bindir}/fdfs_storaged $RPM_BUILD_ROOT%{_bindir}/fastdfs-storaged

%pre
# Add the "fdfs" user
getent group fdfs >/dev/null || groupadd -r fdfs
getent passwd fdfs >/dev/null || \
    useradd -r -g fdfs -s /sbin/nologin \
    -d /var/lib/fastdfs -c "fastdfs user"  fdfs
exit 0

%post tracker
chkconfig --add fastdfs-trackerd || true
%post storage
chkconfig --add fastdfs-storaged || true

%preun tracker
chkconfig --del fastdfs-trackerd || true
%preun storage
chkconfig --del fastdfs-storaged || true

%clean
rm -rf $RPM_BUILD_ROOT

pushd common;make -s clean ;popd
pushd tracker;make -s clean ;popd
pushd storage;make -s clean ;popd
pushd test;make -s clean ;popd
pushd client ;make -s clean ;popd

%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/fdfs
%dir %{_datadir}/fastdfs
%dir %attr(0755,fdfs,fdfs) %{_sharedstatedir}/fastdfs
%dir %attr(0755,fdfs,fdfs) %{_sharedstatedir}/fastdfs/client
%dir %attr(0755,fdfs,fdfs) %{_sharedstatedir}/fastdfs/storage
%dir %attr(0755,fdfs,fdfs) %{_sharedstatedir}/fastdfs/tracker

%files tracker
%defattr(-,root,root,-)
%{_bindir}/fastdfs-trackerd
%config(noreplace) %{_sysconfdir}/fdfs/tracker.conf
%{_initrddir}/fastdfs-trackerd

%files storage
%defattr(-,root,root,-)
%{_bindir}/fastdfs-storaged
%config(noreplace) %{_sysconfdir}/fdfs/storage.conf
%{_initrddir}/fastdfs-storaged

%files -n libfdfsclient
%{_libdir}/libfdfsclient*
%exclude /usr/lib/libfdfsclient.so
%config(noreplace) %{_sysconfdir}/fdfs/client.conf
%config(noreplace) %{_sysconfdir}/fdfs/http.conf
%config(noreplace) %{_sysconfdir}/fdfs/mime.types
%config(noreplace) %{_sysconfdir}/fdfs/storage_ids.conf
%config(noreplace) %{_sysconfdir}/fdfs/anti-steal.jpg

%files -n libfdfsclient-devel
%defattr(-,root,root,-)
%{_includedir}/fastdfs/*

%files tool
%{_bindir}/fdfs_monitor
%{_bindir}/fdfs_test
%{_bindir}/fdfs_test1
%{_bindir}/fdfs_crc32
%{_bindir}/fdfs_upload_file
%{_bindir}/fdfs_download_file
%{_bindir}/fdfs_delete_file
%{_bindir}/fdfs_file_info
%{_bindir}/fdfs_appender_test
%{_bindir}/fdfs_appender_test1
%{_bindir}/fdfs_append_file
%{_bindir}/fdfs_upload_appender

%changelog
* Sat Mar 18 2017  Purple Grape <purplegrape4@gmail.com>
- update to v5.09

* Fri Nov 06 2015  Purple Grape <purplegrape4@gmail.com>
- update to v5.0.7

* Thu Nov 05 2015  Purple Grape <purplegrape4@gmail.com>
- update to v5.0.5
- new init scripts
- run as user fdfs by default

* Mon Jun 23 2014  Zaixue Liao <liaozaixue@yongche.com>
- first RPM release (1.0)
