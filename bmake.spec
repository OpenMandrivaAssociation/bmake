Summary:       The NetBSD make(1) tool
Name:          bmake
Version:	20260824
Release:	1
License:	BSD with advertising
Group:		Development/Other
URL:		ftp://ftp.NetBSD.org/pub/NetBSD/misc/sjg/
Source0:	ftp://ftp.NetBSD.org/pub/NetBSD/misc/sjg/bmake-%{version}.tar.gz
Requires:	mk-files
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	slibtool
BuildRequires:	make
BuildRequires:	mk-files
BuildRequires:	util-linux

%description
bmake, the NetBSD make tool, is a program designed to simplify the
maintenance of other programs.  The input of bmake is a list of specifications
indicating the files upon which the targets (programs and other files) depend.
bmake then detects which targets are out of date based on their dependencies
and triggers the necessary commands to bring them up to date when that happens.

bmake is similar to GNU make, even though the syntax for the advanced features
supported in Makefiles is very different.

%prep
%setup -q -n bmake

%build
%configure --with-default-sys-path=%{_datadir}/mk
sh ./make-bootstrap.sh

# Bootstrap plus a few typical make graphs (vars, suffixes, parallel-ish
# phony targets). The binary is small but the parser/graph is C.
%pgo
./bmake -r -f /dev/null -V .MAKE.LEVEL >/dev/null 2>&1 || true
cat > bmake-pgo.mk << 'EOF'
.PHONY: all a b c
all: a b c
a b c:
	@true
EOF
./bmake -f bmake-pgo.mk all
./bmake -f bmake-pgo.mk -n all
rm -f bmake-pgo.mk

%install
install -m 755 -d %{buildroot}%{_bindir}
install -m 755 -c bmake %{buildroot}%{_bindir}/bmake
install -m 755 -d %{buildroot}%{_mandir}/man1
install -m 644 -c make.1 %{buildroot}%{_mandir}/man1/bmake.1

%files
%doc ChangeLog README
%{_bindir}/*
%{_mandir}/man1/*
