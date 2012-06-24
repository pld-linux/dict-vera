%define		dictname vera
Summary:	Virtual Entity of Relevant Acronyms dictionary for dictd
Summary(pl):	S�ownik Virtual Entity of Relevant Acronyms dla dictd
Name:		dict-%{dictname}
Version:	1.9
Release:	1
License:	GPL
Group:		Applications/Dictionaries
Source0:	ftp://ftp.gnu.org/gnu/vera/%{dictname}-%{version}.tar.gz
# Source0-md5:	ed6120dd9739c71580a92868a34776b0
URL:		http://www.dict.org/
BuildRequires:	dictfmt
BuildRequires:	dictzip
Requires:	dictd
Requires:	%{_sysconfdir}/dictd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains V.E.R.A, version %{version}, formatted for use by
the dictionary server in the dictd package.

%description -l pl
Ten pakiet zawiera s�ownik V.E.R.A w wersji %{version}, sformatowany do
u�ytku z serwerem s�ownika dictd.

%prep
%setup -q -n %{dictname}-%{version}

%build
perl -ne 's/\@item (.*)\n/:$1:\n/; print unless /^@/' vera.? | \
	dictfmt -j -u http://home.snafu.de/ohei/ -s \
	"V.E.R.A. -- Virtual Entity of Relevant Acronyms (%{version})" %{dictname}
dictzip %{dictname}.dict

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/dictd,%{_sysconfdir}/dictd}

dictprefix=%{_datadir}/dictd/%{dictname}
echo "# Virtual Entity of Relevant Acronyms dictionary
database %{dictname} {
	data  \"$dictprefix.dict.dz\"
	index \"$dictprefix.index\"
}" > $RPM_BUILD_ROOT%{_sysconfdir}/dictd/%{dictname}.dictconf
mv %{dictname}.{dict.dz,index} $RPM_BUILD_ROOT%{_datadir}/dictd

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/dictd ]; then
	/etc/rc.d/init.d/dictd restart 1>&2
fi

%postun
if [ -f /var/lock/subsys/dictd ]; then
	/etc/rc.d/init.d/dictd restart 1>&2 || true
fi

%files
%defattr(644,root,root,755)
%doc README vera.texi
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/dictd/%{dictname}.dictconf
%{_datadir}/dictd/%{dictname}.*
