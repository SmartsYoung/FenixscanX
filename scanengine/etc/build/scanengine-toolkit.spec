Name:           scanengine-toolkit
Version:        v0.0.1
Release:        0
Url:            https://gitee.com/meta-oss/FenixscanX
Summary:        ScanEngine is a tool to scan code and detect licenses, copyrights and more.
License:        GPL-2.0
Source:         https://gitee.com/meta-oss/FenixscanX/archive/%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  python-devel
BuildRequires:  zlib
BuildRequires:  bzip2
BuildRequires:  liblzma5
BuildRequires:  libarchive13
BuildRequires:  git

%description
ScanEngine is a tool to scan code and detect copyrights and more.

%prep
%setup -q -n %{name}-%{version}

%build
#cd %{buildroot}
ls -al
pwd
./configure
cd `pwd` && bin/py.test -n 2 -vvs src tests/commoncode

#py.test -n 2 -vvs src tests/commoncode tests/extractcode tests/textcode tests/typecode tests/cluecode tests/scanengine tests/licensedcode/test_detect.py tests/licensedcode/test_index.py tests/licensedcode/test_legal.py tests/licensedcode/test_models.py

#%install
#python setup.py install --prefix=%{_prefix} --root=%{buildroot}

#%check
#source configure && py.test -n 2 -vs src tests/commoncode
