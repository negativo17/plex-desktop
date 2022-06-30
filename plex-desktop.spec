%global         debug_package %{nil}
%global         __strip /bin/true
# Build id links are sometimes in conflict with other RPMs.
%define         _build_id_links none

# Remove bundled libraries from requirements/provides
%global         __requires_exclude ^(libav.*\\.so.*|libicu.*\\.so.*|libsw.*\\.so.*|libQt.*\\.so\\..*|libPlexMediaServer\\.so.*)$
%global         __provides_exclude ^lib.*\\.so.*$

%global         desktop_id tv.plex.PlexDesktop
%global         plex_hash 6c3d964f
%global         plex_version %{version}-%{plex_hash}

Name:           plex-desktop
Summary:        Plex client for Linux
Version:        1.47.1.3086
Release:        1%{?dist}
License:        https://www.plex.tv/media-server-downloads/#remodal-terms
URL:            https://www.plex.tv/media-server-downloads/#plex-app
ExclusiveArch:  x86_64

Source0:        https://artifacts.plex.tv/plex-desktop-stable/%{plex_version}/linux/Plex-%{plex_version}-linux-x86_64.tar.bz2
NoSource:       0
Source1:        https://raw.githubusercontent.com/flathub/%{desktop_id}/master/%{desktop_id}.desktop
Source2:        https://github.com/flathub/%{desktop_id}/raw/master/%{desktop_id}.png
Source3:        https://raw.githubusercontent.com/flathub/%{desktop_id}/master/%{desktop_id}.metainfo.xml
Patch0:         %{name}-script.patch

BuildRequires:  chrpath
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib

%description
Plex for Linux is your client for playback on the Linux desktop. It features the
point and click interface you see in your browser but uses a more powerful
playback engine as well as some other advance features.

%prep
%setup -q -c
%patch0 -p0

chrpath -d bin/Plex
chrpath -d bin/Plex\ Transcoder

for lib in lib/libav* lib/libicu* lib/libsw* lib/libQt* lib/libPlexMediaServer.so; do
    chrpath -d $lib
done

find . -name "*.js" -exec chmod 644 {} \;
find . -name "*.qml" -exec chmod 644 {} \;
find . -name "*.qmltypes" -exec chmod 644 {} \;
find . -name "qmldir" -exec chmod 644 {} \;

%install
# Libraries
mkdir -p %{buildroot}%{_libdir}/%{name}/lib
install -p -m 0755 lib/libav* lib/libicu* lib/libsw* lib/libQt* lib/libPlexMediaServer.so \
    %{buildroot}%{_libdir}/%{name}/lib/
cp -a plugins resources qml translations %{buildroot}%{_libdir}/%{name}/

# Main binaries
install -p -m 0755 Plex.sh %{buildroot}%{_libdir}/%{name}/
mkdir -p %{buildroot}%{_libdir}/%{name}/bin
install -p -m 0755 bin/* %{buildroot}%{_libdir}/%{name}/bin/
mkdir -p %{buildroot}%{_bindir}
ln -sf %{_libdir}/%{name}/Plex.sh %{buildroot}%{_bindir}/Plex

# Desktop stuff
install -p -m 0644 -D %{SOURCE1} %{buildroot}%{_datadir}/applications/%{desktop_id}.desktop
install -p -m 0644 -D %{SOURCE2} %{buildroot}%{_datadir}/icons/%{desktop_id}.png
install -p -m 0644 -D %{SOURCE3} %{buildroot}%{_metainfodir}/%{desktop_id}.metainfo.xml

%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{desktop_id}.metainfo.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/%{desktop_id}.desktop

%files
%{_bindir}/Plex
%{_datadir}/applications/%{desktop_id}.desktop
%{_datadir}/icons/%{desktop_id}.png
%{_libdir}/%{name}
%{_metainfodir}/%{desktop_id}.metainfo.xml

%changelog
* Fri Jul 01 2022 Simone Caronni <negativo17@gmail.com> - 1.47.1.3086-1
- First build.
