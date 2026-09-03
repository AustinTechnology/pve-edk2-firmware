#!/usr/bin/env bash
set -euo pipefail

repo_root=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
image=${IMAGE:-austintechnology/pve-edk2-builder:trixie}

git -C "$repo_root" submodule update --init edk2
# Initialise every direct EDK II submodule, but deliberately do not recurse into
# optional OpenSSL test/provider submodules; the firmware build does not need them.
git -C "$repo_root/edk2" submodule update --init

docker build --tag "$image" --file "$repo_root/docker/Dockerfile.build" "$repo_root"
docker run --rm \
  --user "$(id -u):$(id -g)" \
  --mount "type=bind,src=$repo_root,dst=/src" \
  --workdir /src \
  "$image" \
  bash -lc 'dpkg-checkbuilddeps && make deb && version="$(dpkg-parsechangelog -SVersion)" && lintian ../pve-edk2-firmware*_"$version"_all.deb'
