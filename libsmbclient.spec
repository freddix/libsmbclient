%define		rname	samba

Summary:	Samba library and clients
Name:		libsmbclient
Version:	3.6.8
Release:	2
License:	GPL v3
Group:		Networking/Daemons
Source0:	http://www.samba.org/samba/ftp/%{rname}-%{version}.tar.gz
# Source0-md5:	fbb245863eeef2fffe172df779a217be
URL:		http://www.samba.org/
BuildRequires:	acl-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	cups-devel
BuildRequires:	iconv
BuildRequires:	libmagic-devel
BuildRequires:	libtool
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
BuildRequires:	popt-devel
BuildRequires:	python-devel
BuildRequires:	readline-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	talloc-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Library that allows to use samba clients functions.

%package devel
Summary:	libsmbclient - samba client library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libsmbclient.

%prep
%setup -qn %{rname}-%{version}

%build
cd source3
%{__libtoolize}
%{__autoconf} -Im4 -I../m4 -I../lib/replace -Ilib/replace -I../source4
%configure \
	--disable-dnssd			\
	--disable-static		\
	--enable-avahi			\
	--enable-external-libtalloc=yes \
	--with-fhs			\
	--with-libtalloc=no		\
	--without-ads			\
	--without-krb5			\
	--without-ldap

%{__make} -j1 libsmbclient libsmbsharemodes

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir},%{_pkgconfigdir}}

cd source3
cp -a bin/lib*.so* $RPM_BUILD_ROOT%{_libdir}

install include/libsmbclient.h \
	include/smb_share_modes.h \
	$RPM_BUILD_ROOT%{_includedir}

install pkgconfig/{smbclient,smbsharemodes,wbclient}.pc $RPM_BUILD_ROOT%{_pkgconfigdir}
cd ..

install nsswitch/libwbclient/wbclient.h $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun	-p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsmbclient.so.*
%attr(755,root,root) %{_libdir}/libsmbsharemodes.so.*
%attr(755,root,root) %{_libdir}/libtdb.so.*
%attr(755,root,root) %{_libdir}/libwbclient.so.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsmbclient.so
%attr(755,root,root) %{_libdir}/libsmbsharemodes.so
%attr(755,root,root) %{_libdir}/libtdb.so
%attr(755,root,root) %{_libdir}/libwbclient.so
%{_includedir}/libsmbclient.h
%{_includedir}/wbclient.h
%{_includedir}/smb_share_modes.h
%{_pkgconfigdir}/*.pc

