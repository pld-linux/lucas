Summary:	Framework for configuring servers/services through LDAP
Summary(pl.UTF-8):	Szkielet do konfigurowania serwerów/usług poprzez LDAP
Name:		lucas
Version:	1.0
Release:	0.1
License:	GPL v2
Group:		Applications/System
Source0:	http://www.home.unix-ag.org/patrick/software/lucas/%{name}-%{version}.tgz
# Source0-md5:	0be2b71038609e6ca13348c34d0e4cf3
Source1:	lum.init
URL:		http://www.home.unix-ag.org/patrick/
BuildRequires:	groff
BuildRequires:	openldap-devel >= 2.4.6
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Lucas is a framework to monitor LDAP databases for changes and
reacting to them. Currently it only consists of "lum" (LDAP Update
Monitor), a daemon, working as a slave LDAP server, that triggers
scripts/programs, as soon as the master tries to replicate changes.

%description -l pl.UTF-8
Lucas to szkielet do monitorowania baz danych LDAP pod kątem zmian i
reagowania na nie. Aktualnie składa się tylko z "lum" (LDAP Update
Monitor) - demona działającego jako podległy (slave) serwer LDAP,
wyzwalający skrypty/programy zaraz po tym, jak główny serwer (master)
próbuje zreplikować zmiany.

%package -n lum
Summary:	LDAP Update Monitor
Summary(pl.UTF-8):	LDAP Update Monitor - monitor uaktualnień LDAP
Group:		Applications/System
Requires:	rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/useradd

%description -n lum
LDAP Update Monitor is a daemon, working as a slave LDAP server, that
triggers scripts/programs, as soon as the master tries to replicate
changes.

%description -n lum -l pl.UTF-8
LDAP Update Monitor jest demonem pracującym jako serwer LDAP w trybie
"slave" i wykonującym skrypty programy jak tylko "master" próbuje
zreplikować zmiany.

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8}
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig,%{name}}

install src/lum/lum $RPM_BUILD_ROOT%{_sbindir}
install doc/*.8 $RPM_BUILD_ROOT%{_mandir}/man8
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/lum
install data/dist/suse/lum.sysconfig $RPM_BUILD_ROOT/etc/sysconfig/lum
install data/lum.cfg $RPM_BUILD_ROOT%{_sysconfdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre -n lum
%useradd -P lum -u 152 -s /bin/false -c "LDAP Update Monitor" -g nobody lum

%post -n lum
/sbin/chkconfig --add lum
%service lum restart

%preun -n lum
if [ "$1" = "0" ]; then
	%service lum stop
	/sbin/chkconfig --del lum
fi

%postun -n lum
if [ "$1" = "0" ]; then
	%userremove lum
fi

%files -n lum
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/lum
%attr(754,root,root) /etc/rc.d/init.d/lum
# we don't want lie README
%doc doc/AUTHORS doc/HISTORY
%{_mandir}/man8/lum.8*
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/lum
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/lum.cfg
