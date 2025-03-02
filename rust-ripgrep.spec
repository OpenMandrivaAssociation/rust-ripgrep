# Rust packages always list license files and docs
# inside the crate as well as the containing directory
%undefine _duplicate_files_terminate_build
%bcond_without check

%global crate ripgrep

Name:           rust-ripgrep
Version:        14.1.1
Release:        1
Summary:        Line-oriented search tool that recursively searches the current directory for a regex pattern while respecting gitignore rules
Group:          Development/Rust

License:        BSD-3-Clause AND MIT AND Unicode-DFS-2016 AND (Apache-2.0 OR BSL-1.0) AND (MIT OR Apache-2.0) AND (Unlicense OR MIT)
# LICENSE.dependencies contains a full license breakdown
URL:            https://crates.io/crates/ripgrep
Source0:        %{crates_source}
Source1:        %{crate}-%{version}-vendor.tar.xz
Patch:          ripgrep-fix-metadata.diff

ExclusiveArch:  %{rust_arches}

BuildRequires:  cargo-rpm-macros >= 24

%global _description %{expand:
Ripgrep is a line-oriented search tool that recursively searches the
current directory for a regex pattern while respecting gitignore rules.
ripgrep has first class support on Windows, macOS and Linux.}

%description %{_description}

%files
%license COPYING
%license LICENSE-MIT
%license UNLICENSE
%license LICENSE.dependencies
%doc CHANGELOG.md
%doc FAQ.md
%doc GUIDE.md
%doc README.md
%doc RELEASE-CHECKLIST.md
%{_bindir}/rg
%{_mandir}/man1/rg.1*
%{_datadir}/bash-completion/completions/rg.bash
%{_datadir}/fish/completions/rg.fish
%{_datadir}/zsh/site-functions/_rg

%prep
%autosetup -n %{crate}-%{version} -p1
tar xf %{SOURCE1}
%cargo_prep -v vendor

%build
%cargo_build
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies

%cargo_vendor_manifest

%install
%cargo_install
pwd
target/release/rg --generate man > rg.1
target/release/rg --generate complete-bash > rg.bash
target/release/rg --generate complete-fish > rg.fish
target/release/rg --generate complete-zsh > _rg

install -Dpm 0644 rg.1 -t %{buildroot}/%{_mandir}/man1/
install -Dpm 0644 rg.bash -t %{buildroot}/%{_datadir}/bash-completion/completions/
install -Dpm 0644 rg.fish -t %{buildroot}/%{_datadir}/fish/completions/
install -Dpm 0644 _rg -t %{buildroot}/%{_datadir}/zsh/site-functions/

%if %{with check}
%check
%cargo_test
%endif
