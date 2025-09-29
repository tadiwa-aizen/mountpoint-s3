%bcond_without check

Name:           mount-s3
Version:        1.20.0
Release:        1.amzn2023
Summary:        Mountpoint for Amazon S3

License:        Apache-2.0
URL:            https://github.com/awslabs/mountpoint-s3
Source0:        mountpoint-s3-%{version}.tar.gz
Source1:        LICENSE
Source2:        NOTICE
Source3:        THIRD_PARTY_LICENSES

# BuildRequires lists dependencies that must be installed on the build system before the package can be compiled.
BuildRequires:  clang
BuildRequires:  clang-devel
BuildRequires:  rust = 1.88.0
BuildRequires:  cargo = 1.88.0
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  pkgconfig
BuildRequires:  fuse-devel
BuildRequires:  glibc-devel
BuildRequires:  glibc-headers
BuildRequires:  glibc-static
BuildRequires:  libstdc++-devel
BuildRequires:  nasm
BuildRequires:  make
BuildRequires:  which
BuildRequires:  rust-packaging
BuildRequires:  rust-toolset

ExclusiveArch: x86_64 aarch64

# BUNDLED C/C++ LIBRARIES - Required virtual provides for security tracking
Provides: bundled(aws-c-auth) = 0.9.0
Provides: bundled(aws-c-cal) = 0.9.2
Provides: bundled(aws-c-common) = 0.2.1
Provides: bundled(aws-c-compression) = 0.3.1
Provides: bundled(aws-checksums) = 0.1.1
Provides: bundled(aws-c-http) = 0.10.3
Provides: bundled(aws-c-io) = 0.9.13
Provides: bundled(aws-c-s3) = 0.8.5
Provides: bundled(aws-c-sdkutils) = 0.2.4
Provides: bundled(aws-lc) = 1.53.1
Provides: bundled(s2n-tls) = 0.10.3

Requires:       ca-certificates
Requires:       fuse >= 2.9.0
Requires:       fuse-libs >= 2.9.0

%description
Mountpoint for Amazon S3 is a simple, high-throughput file client for
mounting an Amazon S3 bucket as a local file system. With Mountpoint for Amazon
S3, your applications can access objects stored in Amazon S3 through file
operations like open and read. Mountpoint for Amazon S3 automatically
translates these operations into S3 object API calls, giving your applications
access to the elastic storage and throughput of Amazon S3 through a file
interface.

%prep
%autosetup -n mountpoint-s3
%cargo_prep -v vendor

%build
# This suppresses optimization warnings
export CFLAGS="${CFLAGS:-%{optflags}} -O2 -Wno-error=cpp"
export CMAKE_C_FLAGS="$CFLAGS"

export RUSTFLAGS="${RUSTFLAGS} -C debuginfo=line-tables-only"
cargo build --release --frozen --offline
%cargo_vendor_manifest

%install
mkdir -p %{buildroot}/opt/aws/mountpoint-s3/bin
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_prefix}/sbin
cp target/release/mount-s3 %{buildroot}/opt/aws/mountpoint-s3/bin/mount-s3
cp NOTICE %{buildroot}/opt/aws/mountpoint-s3/
cp LICENSE %{buildroot}/opt/aws/mountpoint-s3/
cp THIRD_PARTY_LICENSES %{buildroot}/opt/aws/mountpoint-s3/
cp cargo-vendor.txt %{buildroot}/opt/aws/mountpoint-s3/
echo "%{version}" > %{buildroot}/opt/aws/mountpoint-s3/VERSION
ln -sf /opt/aws/mountpoint-s3/bin/mount-s3 %{buildroot}/%{_bindir}/mount-s3
ln -sf /opt/aws/mountpoint-s3/bin/mount-s3 %{buildroot}/%{_prefix}/sbin/mount.mount-s3

%if %{with check}
%check

# We reuse the same optimized flags as in the  %build section
export CFLAGS="%{optflags} -O2 -Wno-error=cpp"
export CMAKE_C_FLAGS="$CFLAGS"

# ulimit -n 4096 increases the maximum number of open file descriptors to 4096
# because Mountpoint-S3's tests open many files simultaneously and would fail with
# the default lower limit.
ulimit -n 4096
cargo test --release --frozen --offline -- \
    --skip mnt::test::mount_unmount \
    --skip unmount_no_send

%endif

%files
%dir /opt/aws/mountpoint-s3
%dir /opt/aws/mountpoint-s3/bin
/opt/aws/mountpoint-s3/bin/mount-s3
%doc /opt/aws/mountpoint-s3/NOTICE
%license /opt/aws/mountpoint-s3/LICENSE
%license /opt/aws/mountpoint-s3/cargo-vendor.txt
/opt/aws/mountpoint-s3/THIRD_PARTY_LICENSES
/opt/aws/mountpoint-s3/VERSION
%{_bindir}/mount-s3
%{_prefix}/sbin/mount.mount-s3

%changelog
* Wed Sep 24 2025 Tadiwa Magwenzi <tadiwaom@amazon.com> - 1.20.0
- Initial packaging for AL submission