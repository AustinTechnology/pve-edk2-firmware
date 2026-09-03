#!/usr/bin/env bash
set -euo pipefail

repo_root=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
image=${IMAGE:-austintechnology/pve-edk2-builder:trixie}

git -C "$repo_root" submodule update --init edk2
git -C "$repo_root/edk2" submodule update --init \
  BaseTools/Source/C/BrotliCompress/brotli \
  CryptoPkg/Library/OpensslLib/openssl \
  MdeModulePkg/Library/BrotliCustomDecompressLib/brotli \
  MdePkg/Library/MipiSysTLib/mipisyst

docker build --tag "$image" --file "$repo_root/docker/Dockerfile.build" "$repo_root"
docker run --rm \
  --mount "type=bind,src=$repo_root,dst=/src" \
  --workdir /src \
  "$image" \
  bash -lc 'dpkg-checkbuilddeps && make deb'
