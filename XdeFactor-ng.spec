#
# TODO:
# - do defactor-ng_sql.spec with automagical script which
#   configure our databases to work with XdeFactor-ng or phpDeFactor-ng
# - add user ksiegowy (accounter) to whole distribution ?
# - wants to use /var/log/xdefactor-ng.log - teach him not to
#
%define		_snap	27022004
%define		_dbsnap	2004_04_08
%define		_modules login logout about clients goods invoices means_of_transport stores archive_invoices
Summary:	XdeFactor - New Generation of program to make invoices
Summary(pl):	XdeFactor - nowa generacja programu do fakturowania
Name:		XdeFactor-ng
Version:	%{_snap}
Release:	3
Epoch:		1
License:	GPL
Group:		Applications
#Source0:	http://defactor-ng.gnu.pl/XdeFactor-ng_snapshots/%{name}_%{version}.tar.gz
# S XXXource0-md5:	94f7f1abfafbff21183a7d3ee40f9d95
Source0:	http://www.xdefactor.netsync.pl/snapshots/%{name}-%{version}.tar.gz
# Source0-md5:	3f2d7b129b19cbeb79d5fa197b175f4b
Source1:	%{name}.conf
Source2:	%{name}-modules.conf
Source10:	http://duch.mimuw.edu.pl/~hunter/deFactor-ng_sql_%{_dbsnap}.tar.gz
# Source10-md5:	da1bc049b3bbb33d06c364f3b6fefb11
#http://defactor-ng.gnu.pl/deFactor-ng_sql_snapshots/deFactor-ng_sql_%{_dbsnap}.tar.gz
Patch0:		%{name}-includes.patch
Patch1:		%{name}-modules-includes.patch
Patch2:		%{name}-sharedir.patch
Patch3:		%{name}-pic.patch
URL:		http://defactor-ng.gnu.pl/
BuildRequires:	autoconf >= 2.13
BuildRequires:	automake
BuildRequires:	glib2-devel >= 2.0.0
BuildRequires:	gtk+2-devel >= 2.0.0
BuildRequires:	pkgconfig
BuildRequires:	postgresql-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is nice program to makeing invoices, service clients, service
stores, service goods, service means of transport, service archive
invoices. It's based on GTK+2 library.

You will need access to PostgreSQL database. Sample structures are
given in the %{name}-database package.

%description -l pl
Jest to ca³kiem przyjemny program do fakturowania, obs³ugi klientów,
obs³ugi magazynów, zarz±dzania us³ugami/towarami, zarz±dzania ¶rodkami
transportu, zarz±dzania fakturami archiwalnymi. Jest on oparty o
bibliotekê GTK+2.

Potrzebny jest dostêp do bazy danych PostgreSQL. Przyk³adowa
struktura bazy znajduje siê w paczce %{name}-database.

%package database
Summary:	Database specs for XdeFactor
Summary(pl):	Definicja bazy dla XdeFactora
Group:		Applications
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description database
Database definition for XdeFactor.

%description database -l pl
Definicja bazy dla XdeFactora.

%prep
%setup -q -n %{name} -a 10
%patch0 -p0
#%patch1 -p1
#%patch2 -p1
%patch3 -p1

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-user=nobody \
	--with-group=nogroup

%{__make} \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/defactor-ng/x/modules,%{_bindir},%{_datadir}/%{name}/images,%{_libdir}}

install src/xdefactor-ng $RPM_BUILD_ROOT%{_bindir}
install conf/logo.jpg $RPM_BUILD_ROOT%{_datadir}/%{name}/images
#install conf/modules.conf.example $RPM_BUILD_ROOT%{_datadir}/%{name}
install conf/*.conf $RPM_BUILD_ROOT%{_sysconfdir}/defactor-ng/x
#install conf/host.name $RPM_BUILD_ROOT%{_sysconfdir}/defactor-ng/x
cat %{SOURCE1} >> $RPM_BUILD_ROOT%{_sysconfdir}/defactor-ng/x/xdefactor-ng.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/defactor-ng/x/modules.conf

for i in			\
	views.sql		\
	triggers.sql		\
	struct.sql		\
	triggers.sql		\
	user_perms.sql		\
	perms.sql.dist		\
	install.sh.dist		\
	init.sql.dist		\
	init.sh.dist		\
	environment		\
	data.sql		\
	config_db		\
	README			\
	Makefile;

do 
	install deFactor-ng_sql/$i  $RPM_BUILD_ROOT%{_datadir}/%{name}
done

cd src/modules

for i in %{_modules}; do
	cd $i
	for j in *.so; do
		install $j $RPM_BUILD_ROOT%{_libdir}
	done
	install *.conf $RPM_BUILD_ROOT%{_sysconfdir}/defactor-ng/x/modules
	cd ..
done

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README conf/modules.conf.example
%attr(755,root,root) %{_bindir}/xdefactor-ng
%attr(755,root,root) %{_libdir}/libxdef_*.so
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/images
%{_datadir}/%{name}/images/logo.jpg
%dir %{_sysconfdir}/defactor-ng
%dir %{_sysconfdir}/defactor-ng/x
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/defactor-ng/x/*.conf
#%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/defactor-ng/x/host.name
%dir %{_sysconfdir}/defactor-ng/x/modules
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/defactor-ng/x/modules/*.conf

%files database
%defattr(644,root,root,755)
%{_datadir}/%{name}/*
%exclude %{_datadir}/%{name}/images
