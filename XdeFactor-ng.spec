#
# TODO:
# do defactor-ng.spec with automagical script which
# configure our databases to work with XdeFactor-ng or phpDeFactor-ng
#
%define		_snap	20030212
%define		_modules login logout about clients goods invoices means_of_transport stores archive_invoices
Summary:	XdeFactor - New Generation of program to make invoices
Summary(pl):	XdeFactor - Nowa Generacja programu do fakturowania
Name:		XdeFactor-ng
Version:	%{_snap}
Release:	1
License:	GPL
Group:		Applications
BuildRequires:	glib2-devel
BuildRequires:	postgresql-devel
BuildRequires:	gtk+2-devel
BuildRequires:	pango-devel
BuildRequires:	pkgconfig
BuildRequires:	freetype-devel
Prereq: 	/sbin/ldconfig
Source0:	http://defactor-ng.gnu.pl/XdeFactor-ng_snapshots/%{name}_%{version}.tar.gz
Source1:	%{name}.conf
Source2:	%{name}-modules.conf
Patch0:		%{name}-includes.patch
Patch1:		%{name}-modules-includes.patch
Patch2:		%{name}-sharedir.patch
URL:		http://defactor-ng.gnu.pl/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is nice program to makeing invoices, service clients, service
stores, service goods, service means of transport, service archive
invoices. It's based on GTK+2 library.

%description -l pl
Ca³kiem przyjemny program do fakturowania, obs³ugi klientów, obs³ugi
magazynów, zarz±dzania us³ugami/towarami, zarz±dzania ¶rodkami transportu,
zarz±dzania fakturami archiwalnymi. Jest on oparty o bibliotekê GTK+2.

%package module-clients
Summary:	XdeFactor - Clients module
Summary(pl):	XdeFactor - Modu³ obs³ugi klientów
Group:          Applications
Requires:       %{name} = %{version}

%description module-clients
With this module you can manage your clients.

%description module-clients -l pl
Dziêki temu modu³owi bêdziesz móg³ zarz±dzaæ klientami.

%package module-goods
Summary:	XdeFactor - Goods module
Summary(pl):	XdeFactor - Modu³ zarz±dzania towarami/us³ugami
Group:		Applications
Requires:	%{name} = %{version}

%description module-goods
With this module you can manage your goods or services.

%description module-goods -l pl
Dziêki temu modu³owi bêdziesz móg³ zarz±dzaæ us³ugami/towarami.

%package module-invoices
Summary:	XdeFactor - Invoices module
Summary:	XdeFactor - modu³ fakturowania
Group:		Applications
Requires:	%{name} = %{version}

%description module-invoices
With this module you can prepare invoice.

%description module-invoices -l pl
Dziêki temu modu³owi bêdziesz móg³ wystawiaæ faktury VAT.

%package module-meansoftransport
Summary:	XdeFactor - Means Of Transport module
Summary(pl):	XdeFactor - modu³ ¶rodków transportów
Group:		Applications
Requires:	%{name} = %{version}

%description module-meansoftransport
This module manage means of transport.

%description module-meansoftransport
Modu³ odpowiedzialny jest za operacje na ¶rodkach transportu.

%package module-stores
Summary:	XdeFactor - Stores module
Summary(pl):	XdeFactor - modu³ magazynu
Group:		Applications
Requires:	%{name} = %{version}

%description module-stores
This module manage stores.

%description module-stores -l pl
Jest to modu³ do obs³ugi magazynu

%package module-archiveinvoices
Summary:	XdeFactor - Archive Invoices module
Summary(pl):	XdeFactor - modu³ operacji na archiwalnych fakturach
Group:		Applications
Requires:	%{name} = %{version}

%description module-archiveinvoices
This module allow to works on archived invoices.

%description module-archiveinvoices -l pl
Tem modu³ s³y¿y do operacji na archiwalnych fakturach.

%prep
%setup -q -n xdefactor-ng
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
cd src
%{__make} CC="gcc %{rpmcflags}"

cd modules

for i in %{_modules}; do
 cd $i
 %{__make} CC="gcc %{rpmcflags}"
 cd ..
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/defactor-ng/x/modules/,%{_bindir},%{_datadir}/%{name}/images,%{_libdir}}

install src/xdefactor-ng $RPM_BUILD_ROOT/%{_bindir}/
install conf/logo.jpg $RPM_BUILD_ROOT/%{_datadir}/%{name}/images/
#install conf/modules.conf.example $RPM_BUILD_ROOT/%{_datadir}/%{name}/
install conf/*.conf $RPM_BUILD_ROOT%{_sysconfdir}/defactor-ng/x/
install conf/host.name $RPM_BUILD_ROOT%{_sysconfdir}/defactor-ng/x/
cat %{SOURCE1} >> $RPM_BUILD_ROOT%{_sysconfdir}/defactor-ng/x/xdefactor-ng.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/defactor-ng/x/modules.conf


cd src/modules
	 
for i in %{_modules}; do
 cd $i
for j in *.so; do
  install $j $RPM_BUILD_ROOT%{_libdir}/
 done
 install *.conf $RPM_BUILD_ROOT%{_sysconfdir}/defactor-ng/x/modules/
 cd ..
done

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

# CLIENTS
%post module-clients
echo "/modules/Clients.conf" >> %{_sysconfdir}/defactor-ng/x/modules.conf
echo "libxdef_clients.so" >> %{_sysconfdir}/defactor-ng/x/modules.conf 
/sbin/ldconfig

%postun module-clients
umask 022
cat %{_sysconfdir}/defactor-ng/x/modules.conf | grep -v -i clients > %{_sysconfdir}/defactor-ng/x/modules.conf.tmp
mv %{_sysconfdir}/defactor-ng/x/modules.conf.tmp %{_sysconfdir}/defactor-ng/x/modules.conf
/sbin/ldconfig

# GOODS
%post module-goods
echo "/modules/Goods.conf" >> %{_sysconfdir}/defactor-ng/x/modules.conf
echo "libxdef_goods.so" >> %{_sysconfdir}/defactor-ng/x/modules.conf
/sbin/ldconfig

%postun module-goods
umask 022
cat %{_sysconfdir}/defactor-ng/x/modules.conf | grep -v -i goods > %{_sysconfdir}/defactor-ng/x/modules.conf.tmp
mv %{_sysconfdir}/defactor-ng/x/modules.conf.tmp %{_sysconfdir}/defactor-ng/x/modules.conf
/sbin/ldconfig

# INVOICES
%post module-invoices
echo "/modules/Invoices.conf" >> %{_sysconfdir}/defactor-ng/x/modules.conf
echo "libxdef_invoices.so"  >> %{_sysconfdir}/defactor-ng/x/modules.conf
/sbin/ldconfig

%postun module-invoices
umask 022
cat %{_sysconfdir}/defactor-ng/x/modules.conf | grep -v -i invoices > %{_sysconfdir}/defactor-ng/x/modules.conf.tmp
mv %{_sysconfdir}/defactor-ng/x/modules.conf.tmp %{_sysconfdir}/defactor-ng/x/modules.conf
/sbin/ldconfig

# MEANS OF TRANSPORT
%post module-meansoftransport
echo "/modules/MeansOfTransport.conf" >> %{_sysconfdir}/defactor-ng/x/modules.conf
echo "libxdef_meansoftransport.so"  >> %{_sysconfdir}/defactor-ng/x/modules.conf
/sbin/ldconfig

%postun module-meansoftransport
umask 022
cat %{_sysconfdir}/defactor-ng/x/modules.conf | grep -v -i meansoftransport > %{_sysconfdir}/defactor-ng/x/modules.conf.tmp
mv %{_sysconfdir}/defactor-ng/x/modules.conf.tmp %{_sysconfdir}/defactor-ng/x/modules.conf
/sbin/ldconfig

# STORES
%post module-stores
echo "/modules/Stores.conf" >> %{_sysconfdir}/defactor-ng/x/modules.conf
echo "libxdef_stores.so"  >> %{_sysconfdir}/defactor-ng/x/modules.conf
/sbin/ldconfig

%postun module-stores
umask 022
cat %{_sysconfdir}/defactor-ng/x/modules.conf | grep -v -i stores > %{_sysconfdir}/defactor-ng/x/modules.conf.tmp
mv %{_sysconfdir}/defactor-ng/x/modules.conf.tmp %{_sysconfdir}/defactor-ng/x/modules.conf
/sbin/ldconfig

# ARCHIVE INVOICES
%post module-archiveinvoices
echo "/modules/ArchiveInvoices.conf" >> %{_sysconfdir}/defactor-ng/x/modules.conf
echo "libxdef_archiveinvoices.so"  >> %{_sysconfdir}/defactor-ng/x/modules.conf
/sbin/ldconfig

%postun module-archiveinvoices
cat %{_sysconfdir}/defactor-ng/x/modules.conf | grep -v -i archiveinvoices > %{_sysconfdir}/defactor-ng/x/modules.conf.tmp
mv %{_sysconfdir}/defactor-ng/x/modules.conf.tmp %{_sysconfdir}/defactor-ng/x/modules.conf
/sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS README conf/modules.conf.example
%attr(755,root,root) %{_bindir}/xdefactor-ng
%{_datadir}/%{name}/images/logo.jpg
%{_sysconfdir}/defactor-ng/x/*.conf
%{_sysconfdir}/defactor-ng/x/host.name
%{_sysconfdir}/defactor-ng/x/modules/Login.conf
%{_sysconfdir}/defactor-ng/x/modules/Logout.conf
%{_sysconfdir}/defactor-ng/x/modules/About.conf
%{_libdir}/libxdef_login.so
%{_libdir}/libxdef_logout.so
%{_libdir}/libxdef_about.so

%files module-clients
%defattr(644,root,root,755)
%{_libdir}/libxdef_clients.so
%{_sysconfdir}/defactor-ng/x/modules/Clients.conf

%files module-goods
%defattr(644,root,root,755)
%{_libdir}/libxdef_goods.so
%{_sysconfdir}/defactor-ng/x/modules/Goods.conf

%files module-invoices
%defattr(644,root,root,755)
%{_libdir}/libxdef_invoices.so
%{_sysconfdir}/defactor-ng/x/modules/Invoices.conf

%files module-meansoftransport
%defattr(644,root,root,755)
%{_libdir}/libxdef_meansoftransport.so
%{_sysconfdir}/defactor-ng/x/modules/MeansOfTransport.conf

%files module-stores
%defattr(644,root,root,755)
%{_libdir}/libxdef_stores.so
%{_sysconfdir}/defactor-ng/x/modules/Stores.conf

%files module-archiveinvoices
%defattr(644,root,root,755)
%{_libdir}/libxdef_archiveinvoices.so
%{_sysconfdir}/defactor-ng/x/modules/ArchiveInvoices.conf
