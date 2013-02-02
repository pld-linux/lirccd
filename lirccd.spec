#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	LIRC Client Daemon
Summary(pl.UTF-8):	LIRCCD - demon kliencki LIRC
Name:		lirccd
Version:	0.9.1
Release:	1
License:	GPL v2+
Group:		Libraries
Source0:	http://www.dolda2000.com/~fredrik/lirccd/%{name}-%{version}.tar.gz
# Source0-md5:	1a5f65094b5738117dfde263b7f90ef2
Patch0:		%{name}-libc.patch
URL:		http://www.dolda2000.com/~fredrik/lirccd/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The LIRC Client Daemon connects to the LIRC daemon, parses messages
received, and executes C-like scripts from that data (for more
information, see the README file that comes with the distribution).

The LIRC Client Daemon provides several advantages compared to LIRC's
own client control scheme. First, it can do things itself, making
itself useful even without other clients. Second, it "synchronizes"
all clients, so to speak. Since all clients connect to lirccd and
receive commands from it, there is no chance that client processes
that were started at different times enter different states. Lirccd
also provides a more advanced, hierarchical state system instead of
the linear system used in the old config scheme.

%description -l pl.UTF-8
Demon kliencki LIRC (LIRCCD) łączy się z demonem LIRC, analizuje
otrzymane komunikaty i wywołuje na podstawie tych danych skrypty w
stylu C (więcej informacji - nich można znaleźć w pliku README).

Demon kliencki LIRC ma kilka zalet w porównaniu ze schematem
sterowania klienckiego LIRC. Po pierwsze, może sam wykonywać pewne
czynności, przez co jest przydatny nawet bez innych klientów. Po
drugie, "synchronizuje" wszystkich klientów. Ponieważ wszyscy
klienci łączą się z lirccd i odbierają polecenia od niego, nie ma
możliwości, że procesy klienckie uruchomione o różnym czasie wejdą
w różne stany. Lirccd zapewnia także bardziej rozbudowany system
stanów zamiast systemu liniowego w starym schemacie konfiguracji.

%package devel
Summary:	Header files for LIRC client library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki klienta LIRC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for LIRC client library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki klienta LIRC.

%package static
Summary:	Static LIRC client library
Summary(pl.UTF-8):	Statyczna biblioteka klienta LIRC
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static LIRC client library.

%description static -l pl.UTF-8
Statyczna biblioteka klienta LIRC.

%prep
%setup -q
%patch0 -p1

%build
%configure \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README TODO lirccrc*.example
%attr(755,root,root) %{_bindir}/lirccd
%attr(755,root,root) %{_libdir}/liblirc_client.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblirc_client.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblirc_client.so
%{_libdir}/liblirc_client.la
%{_includedir}/lirc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/liblirc_client.a
%endif
