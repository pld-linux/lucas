
Summary:	Framework for configuring servers/services through LDAP
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
BuildRequires:	openldap-devel
BuildRequires:	rpmbuild(macros) >= 1.202
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Lucas is a framework to monitor LDAP databases for changes and
reacting to them. Currently it only consists of "lum" (LDAP Update
Monitor), a deamon, working as a slave LDAP server, that triggers
scripts/programs, as soon as the master tries to replicate changes.

%package -n lum
Summary:	LDAP Update Monitor
Group:		Applications/System
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/useradd

%description -n lum
LDAP Update Monitor is a deamon, working as a slave LDAP server, that
triggers scripts/programs, as soon as the master tries to replicate
changes.

%description -n lum -l pl
LDAP Update Monitor jest demonem pracuj�cym jako serwer LDAP w trybie
"slave" i wykonuj�cym skrypty programy jak tylko "master" pr�buje
zreplikowa� zmiany.

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/{%{_sbindir},%{_mandir}/man8}
install -d $RPM_BUILD_ROOT/%{_sysconfdir}/{rc.d/init.d,sysconfig,%{name}}

install src/lum/lum $RPM_BUILD_ROOT/%{_sbindir}
install doc/*.8 $RPM_BUILD_ROOT/%{_mandir}/man8
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/lum
install data/dist/suse/lum.sysconfig $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/lum
install data/lum.cfg $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}

%pre -n lum
%useradd -P lum -u 152 -s /bin/false -c "LDAP Update Monitor" -g nobody lum

%post -n lum
/sbin/chkconfig --add lum
if [ -f /var/lock/subsys/lum ]; then
	/etc/rc.d/init.d/lum restart >&2
else
	echo "Run \"/etc/rc.d/init.d/lum start\" to start lum service." >&2
fi

%preun -n lum
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/lum ]; then
		/etc/rc.d/init.d/lum stop
	fi
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

%clean
rm -rf $RPM_BUILD_ROOT
