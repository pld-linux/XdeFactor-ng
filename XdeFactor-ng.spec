#
# TODO:
# summary, desc, more BRs ?, maybe some build fix ?, 
# config files
#
%define		_snap	20030212
%define		_modules login logout about clients goods invoices
#means_of_transport stores archive_invoices
Summary:	XdeFactor - New Generation
Summary(pl):	XdeFactor - Nowa Generacja
Name:		XdeFactor-ng
Version:	%{_snap}
Release:	0.2
License:	GPL
Group:		Applications
BuildRequires:	glib2-devel
BuildRequires:	postgresql-devel
Requires:	%{name}-module-login = %{version}
Requires:       %{name}-module-logout = %{version}
Requires:	%{name}-module-about = %{version}
Prereq: 	/sbin/ldconfig
Source0:	http://defactor-ng.gnu.pl/XdeFactor-ng_snapshots/%{name}_%{version}.tar.gz
Patch0:		%{name}-includes.patch
Patch1:		%{name}-modules-includes.patch
URL:		http://defactor-ng.gnu.pl/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description

%description -l pl

%package module-login
Summary:	XdeFactor - Login Module
Summary(pl):	XdeFacotr - Modu³ logowania
Group:		Applications
Requires:	%{name} = %{version}

%description module-login
Login authentication module.

%description module-login -l pl
Modu³ logowania.

%package module-logout
Summary:	XdeFactor - Logout Module
Summary(pl):	XdeFactor - Modu³ wylogowania
Group:          Applications
Requires:	%{name} = %{version}

%description module-logout
Logout module.

%description module-logout -l pl
Modu³ wylogowania.

%package module-about
Summary:	XdeFactor - About Module
Summary(pl):	XdeFactor - Modu³ "O programie"
Group:          Applications
Requires:       %{name} = %{version}

%description module-about
About module.

%description module-about -l pl
Modu³ "O programie".

%package module-clients
Summary:	XdeFactor - Clients Module
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

%prep
%setup -q -n xdefactor-ng
%patch0 -p1
%patch1 -p1

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
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/defactor-ng/x/modules/,%{_bindir},%{_libdir}/xdefactor-ng/,%{_datadir}/%{name}}

install src/xdefactor-ng $RPM_BUILD_ROOT/%{_bindir}/
install conf/logo.jpg $RPM_BUILD_ROOT/%{_datadir}/%{name}/
install conf/modules.conf.example $RPM_BUILD_ROOT/%{_datadir}/%{name}/
install conf/*.conf $RPM_BUILD_ROOT%{_sysconfdir}/defactor-ng/x/
install conf/host.name $RPM_BUILD_ROOT%{_sysconfdir}/defactor-ng/x/

cd src/modules
	 
for i in %{_modules}; do
 cd $i
for j in *.so; do
  install $j $RPM_BUILD_ROOT%{_libdir}/xdefactor-ng/
 done
 install *.conf $RPM_BUILD_ROOT%{_sysconfdir}/defactor-ng/x/modules/
 cd ..
done

%post   
echo %{_libdir}/xdefactor-ng>> %{_sysconfdir}/ld.so.conf
/sbin/ldconfig

%postun
cat %{_sysconfdir}/ld.so.conf | grep -v xdefactor-ng > /tmp/ld.so.conf.tmp
mv /tmp/ld.so.conf.tmp %{_sysconfdir}/ld.so.conf
/sbin/ldconfig

# LOGIN
%post module-login
echo "/modules/Login.conf" >> %{_sysconfdir}/defactor-ng/x/modules.conf
echo "libxdef_login.so" >> %{_sysconfdir}/defactor-ng/x/modules.conf
chmod 644 %{_sysconfdir}/defactor-ng/x/modules.conf
/sbin/ldconfig

%postun module-login
cat %{_sysconfdir}/defactor-ng/x/modules.conf | grep -v -i login > /tmp/xdf-modules.conf.tmp
mv /tmp/xdf-modules.conf.tmp %{_sysconfdir}/defactor-ng/x/modules.conf
chmod 644 %{_sysconfdir}/defactor-ng/x/modules.conf
/sbin/ldconfig

# LOGOUT
%post module-logout
echo "/modules/Logout.conf" >> %{_sysconfdir}/defactor-ng/x/modules.conf
echo "libxdef_logout.so" >> %{_sysconfdir}/defactor-ng/x/modules.conf
chmod 644 %{_sysconfdir}/defactor-ng/x/modules.conf
/sbin/ldconfig

%postun module-logout
cat %{_sysconfdir}/defactor-ng/x/modules.conf | grep -v -i logout > /tmp/xdf-modules.conf.tmp
mv /tmp/xdf-modules.conf.tmp %{_sysconfdir}/defactor-ng/x/modules.conf
chmod 644 %{_sysconfdir}/defactor-ng/x/modules.conf
/sbin/ldconfig

# ABOUT
%post module-about
echo "/modules/About.conf" >> %{_sysconfdir}/defactor-ng/x/modules.conf
echo "libxdef_about.so" >> %{_sysconfdir}/defactor-ng/x/modules.conf
/sbin/ldconfig

%postun module-about
cat %{_sysconfdir}/defactor-ng/x/modules.conf | grep -v -i about > /tmp/xdf-modules.conf.tmp
mv /tmp/xdf-modules.conf.tmp %{_sysconfdir}/defactor-ng/x/modules.conf
chmod 644 %{_sysconfdir}/defactor-ng/x/modules.conf
/sbin/ldconfig

# CLIENTS
%post module-clients
echo "/modules/Clients.conf" >> %{_sysconfdir}/defactor-ng/x/modules.conf
echo "libxdef_clients.so" >> %{_sysconfdir}/defactor-ng/x/modules.conf 

%postun module-clients
cat %{_sysconfdir}/defactor-ng/x/modules.conf | grep -v -i clients > /tmp/xdf-modules.conf.tmp
mv /tmp/xdf-modules.conf.tmp %{_sysconfdir}/defactor-ng/x/modules.conf
chmod 644 %{_sysconfdir}/defactor-ng/x/modules.conf
/sbin/ldconfig

# GOODS
%post module-goods
echo "/modules/Goods.conf" >> %{_sysconfdir}/defactor-ng/x/modules.conf
echo "libxdef_goods.so" >> %{_sysconfdir}/defactor-ng/x/modules.conf

%postun module-goods
cat %{_sysconfdir}/defactor-ng/x/modules.conf | grep -v -i goods > /tmp/xdf-modules.conf.tmp
mv /tmp/xdf-modules.conf.tmp %{_sysconfdir}/defactor-ng/x/modules.conf
chmod 644 %{_sysconfdir}/defactor-ng/x/modules.conf
/sbin/ldconfig

# INVOICES
%post module-invoices
echo "/modules/Invoices.conf" >> %{_sysconfdir}/defactor-ng/x/modules.conf
echo "libxdef_invoices.so"  >> %{_sysconfdir}/defactor-ng/x/modules.conf

%postun module-invoices
cat %{_sysconfdir}/defactor-ng/x/modules.conf | grep -v -i invoices > /tmp/xdf-modules.conf.tmp
mv /tmp/xdf-modules.conf.tmp %{_sysconfdir}/defactor-ng/x/modules.conf
chmod 644 %{_sysconfdir}/defactor-ng/x/modules.conf
/sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/xdefactor-ng
%{_datadir}/%{name}/
%{_sysconfdir}/defactor-ng/x/*.conf
%{_sysconfdir}/defactor-ng/x/host.name

%files module-login
%defattr(644,root,root,755)
%{_libdir}/xdefactor-ng/libxdef_login.so
%{_sysconfdir}/defactor-ng/x/modules/Login.conf

%files module-logout
%defattr(644,root,root,755)
%{_libdir}/xdefactor-ng/libxdef_logout.so
%{_sysconfdir}/defactor-ng/x/modules/Logout.conf

%files module-about
%defattr(644,root,root,755)
%{_libdir}/xdefactor-ng/libxdef_about.so
%{_sysconfdir}/defactor-ng/x/modules/About.conf

%files module-clients
%defattr(644,root,root,755)
%{_libdir}/xdefactor-ng/libxdef_clients.so
%{_sysconfdir}/defactor-ng/x/modules/Clients.conf

%files module-goods
%defattr(644,root,root,755)
%{_libdir}/xdefactor-ng/libxdef_goods.so
%{_sysconfdir}/defactor-ng/x/modules/Goods.conf

%files module-invoices
%defattr(644,root,root,755)
%{_libdir}/xdefactor-ng/libxdef_invoices.so
%{_sysconfdir}/defactor-ng/x/modules/Invoices.conf
