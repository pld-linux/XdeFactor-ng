#
# TODO:
# summary, desc, more BRs ?, maybe some build fix ?, 
# conditional build - maybe subpackages with sperate modules ?
# 
%define		_snap	20030212
Summary:	XdeFactor - New Generation
Summary(pl):	XdeFactor - Nowa Generacja
Name:		XdeFactor-ng
Version:	%{_snap}
Release:	0.1
License:	GPL
Group:		Bzium
BuildRequires:	glib2-devel
BuildRequires:	postgresql-devel
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

MODULES="login logout about clients goods invoices means_of_transport stores \
	 archive_invoices"

cd modules

for i in $MODULES; do
 cd $i
 %{__make} CC="gcc %{rpmcflags}"
 cd ..
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{{%_sysconfdir}/defactor-ng/x/modules/,%{_bindir},%{_libdir}/xdefactor-ng/}

install src/xdefactor-ng %{_bindir}
install conf/* %{_sysconfdir}/defactor-ng/x/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog README
%attr(755,root,root) %{_bindir}/*
%{_datadir}/
%{_sysconfdir}/defactor-ng/x/
