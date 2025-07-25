%global rustflags '-Clink-arg=-Wl,-z,relro,-z,now'
Name:           rust-ripgrep
Version:        14.1.1
Release:        2
Summary:        A search tool that combines ag with grep
License:        MIT AND Unlicense
Group:          Productivity/Text/Utilities
URL:            https://github.com/BurntSushi/ripgrep
Source0:        ripgrep-%{version}.tar.gz
Source1:        vendor.tar.gz
BuildRequires:  cargo-rpm-macros >= 24
BuildRequires:  pkgconf

%description
ripgrep is a line oriented search tool that combines the usability of
The Silver Searcher (similar to ack) with the raw speed of GNU grep.
ripgrep works by recursively searching your current directory
for a regex pattern.

%prep 
%autosetup -n ripgrep-%{version} -p1 -a1 
%setup -n ripgrep-%{version} -a1
tar xvfz %{SOURCE1}
mkdir -p .cargo 
cat >> .cargo/config.toml << EOF
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"

EOF

%build
cargo build --features 'pcre2' --release

%install
install -D -d -m 0755 %{buildroot}%{_bindir}
install -m 0755 %{_builddir}/ripgrep-%{version}/target/release/rg %{buildroot}%{_bindir}/rg

# remove residual crate file
rm -f %{buildroot}%{_prefix}/.crates*

TARGETBIN=target/release/rg
$TARGETBIN --generate man > rg.1
$TARGETBIN --generate complete-bash > rg.bash
$TARGETBIN --generate complete-fish > rg.fish
$TARGETBIN --generate complete-zsh > rg.zsh
install -Dm 644 rg.1 %{buildroot}%{_mandir}/man1/rg.1
install -Dm 644 rg.bash %{buildroot}%{_datadir}/bash-completion/completions/rg
install -Dm 644 rg.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/rg.fish
install -Dm 644 rg.zsh %{buildroot}%{_datadir}/zsh/site-functions/_rg

%files
%license LICENSE-MIT UNLICENSE
%doc CHANGELOG.md README.md
%{_mandir}/man1/rg.1*
%{_bindir}/rg

%{_datadir}/bash-completion

%{_datadir}/fish

%{_datadir}/zsh

%changelog
