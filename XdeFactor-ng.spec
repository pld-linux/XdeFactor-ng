# TODO: march, files permissions - now passwords are stored 
#	in worldreadable files.
%define		_snap	20040308
%define		_rel	0.1
%define		_origname	XdeFactor-ng
Summary:	XdeFactor-ng - New Generation of program to make invoices
Summary(pl):	XdeFactor-ng - Nowa Generacja programu do fakturowania
Name:		xdefactor-ng
Version:	%{_snap}
Release:	%{_rel}
Epoch:		0
License:	GPL
Group:		X11/Applications
# temporary URL - will be removed after distfiles feeding
Source0:	http://test.mmt.pl/pld/xdefactor/XdeFactor-ng_%{version}.tar.gz
# Source0-md5:	a64f8693f8cdf912f0f13b8d187d9df4
Source1:	%{_origname}.conf
Source2:	%{_origname}-modules.conf
Patch0:		%{_origname}-includes.patch
Patch1:		%{_origname}-uid_gid_log.patch
Patch2:		%{_origname}-pic.patch
Patch3:		%{_origname}-ac_fix.patch
URL:		http://defactor-ng.gnu.pl/
BuildRequires:	autoconf >= 2.13
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	freetype-devel
BuildRequires:	gtk+2-devel
BuildRequires:	glib2-devel
BuildRequires:	pango-devel
BuildRequires:	postgresql-devel
Obsoletes:	XdeFactor-ng
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is nice program to makeing invoices, service clients, service
stores, service goods, service means of transport, service archive
invoices. It's based on GTK+2 library.

%description -l pl
Ca³kiem przyjemny program do fakturowania, obs³ugi klientów, obs³ugi
magazynów, zarz±dzania us³ugami/towarami, zarz±dzania ¶rodkami
transportu, zarz±dzania fakturami archiwalnymi. Jest on oparty o
bibliotekê GTK+2.

%prep
%setup -q -n %{_origname} 
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make} \
	CC="%{__cc}" 

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/defactor-ng/x/*
%{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*
%{_mandir}/man?/*
%{_datadir}/%{name}
