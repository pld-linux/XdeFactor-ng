#
# TODO:
# - do defactor-ng_sql.spec with automagical script which
#   configure our databases to work with XdeFactor-ng or phpDeFactor-ng
# - add user ksiegowy (accounter) to whole distribution ?
#
%define		_snap	20030212
%define		_modules login logout about clients goods invoices means_of_transport stores archive_invoices
Summary:	XdeFactor - New Generation of program to make invoices
Summary(pl):	XdeFactor - Nowa Generacja programu do fakturowania
Name:		XdeFactor-ng
Version:	%{_snap}
Release:	2
License:	GPL
Group:		Applications
Source0:	http://defactor-ng.gnu.pl/XdeFactor-ng_snapshots/%{name}_%{version}.tar.gz
# Source0-md5:	94f7f1abfafbff21183a7d3ee40f9d95
Source1:	%{name}.conf
Source2:	%{name}-modules.conf
Patch0:		%{name}-includes.patch
Patch1:		%{name}-modules-includes.patch
Patch2:		%{name}-sharedir.patch
URL:		http://defactor-ng.gnu.pl/
BuildRequires:	freetype-devel
BuildRequires:	glib2-devel
BuildRequires:	gtk+2-devel
BuildRequires:	pango-devel
BuildRequires:	pkgconfig
BuildRequires:	postgresql-devel
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
%setup -q -n xdefactor-ng
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
cd src
%{__make} CC="%{__cc} %{rpmcflags}"

cd modules

for i in %{_modules}; do
 cd $i
 %{__make} CC="%{__cc} %{rpmcflags}"
 cd ..
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/defactor-ng/x/modules/,%{_bindir},%{_datadir}/%{name}/images,%{_libdir}}

install src/xdefactor-ng $RPM_BUILD_ROOT%{_bindir}
install conf/logo.jpg $RPM_BUILD_ROOT%{_datadir}/%{name}/images
#install conf/modules.conf.example $RPM_BUILD_ROOT%{_datadir}/%{name}
install conf/*.conf $RPM_BUILD_ROOT%{_sysconfdir}/defactor-ng/x
install conf/host.name $RPM_BUILD_ROOT%{_sysconfdir}/defactor-ng/x
cat %{SOURCE1} >> $RPM_BUILD_ROOT%{_sysconfdir}/defactor-ng/x/xdefactor-ng.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/defactor-ng/x/modules.conf

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
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/defactor-ng/x/host.name
%dir %{_sysconfdir}/defactor-ng/x/modules
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/defactor-ng/x/modules/*.conf
