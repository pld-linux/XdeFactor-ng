#
# TODO:
# summary, desc, more BRs ?, maybe some build fix ?, 
# conditional build - maybe subpackages with sperate modules ?
# 
%define		_snap	20030212
%define		_modules login logout about clients goods invoices means_of_transport stores archive_invoices
Summary:	XdeFactor - New Generation
Summary(pl):	XdeFactor - Nowa Generacja
Name:		XdeFactor-ng
Version:	%{_snap}
Release:	0.1
License:	GPL
Group:		Bzium
BuildRequires:	glib2-devel
BuildRequires:	postgresql-devel
Prereq: 	/sbin/ldconfig
Source0:	http://defactor-ng.gnu.pl/XdeFactor-ng_snapshots/%{name}_%{version}.tar.gz
Patch0:		%{name}-includes.patch
Patch1:		%{name}-modules-includes.patch
URL:		http://defactor-ng.gnu.pl/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description

%description -l pl

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
  echo "$j" >> $RPM_BUILD_ROOT%{_sysconfdir}/defactor-ng/x/modules.conf
 done
 install *.conf $RPM_BUILD_ROOT%{_sysconfdir}/defactor-ng/x/modules/
 cd ..
done

# i think it should be in XdeFactor-subpackages in post and postun scripts :)

%post   
echo %{_libdir}/xdefactor-ng>> %{_sysconfdir}/ld.so.conf
/sbin/ldconfig

%postun
cat %{_sysconfdir}/ld.so.conf | grep -v xdefactor-ng > /tmp/ld.so.conf.tmp
mv /tmp/ld.so.conf.tmp %{_sysconfdir}/ld.so.conf

%clean
#rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/xdefactor-ng
%{_datadir}/%{name}/
%{_sysconfdir}/defactor-ng/x/
%{_libdir}/xdefactor-ng/
