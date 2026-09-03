# Austin Technology Proxmox EDK2 firmware

A maintained fork of Proxmox's `pve-edk2-firmware` source that embeds the Austin Technology wordmark in the UEFI boot/setup logo.

## Release model

- The derivative uses the exact upstream version with an `+austinN` suffix.
- It replaces the upstream `pve-edk2-firmware-ovmf` package; it is not a parallel firmware package or a file override.
- Publish the resulting `.deb` through a signed internal APT repository and pin that repository on every PVE node.
- Every migration-capable host must have the identical package version before a branded VM is cold-booted anywhere in the cluster.

## Build

```bash
scripts/build-deb-container.sh
```

The container uses Debian Trixie build dependencies and produces Debian packages in the repository parent directory, as defined by the upstream Makefile.

## Lab gates before promotion

1. Confirm the lab host runs a compatible PVE 9/Trixie `pve-edk2-firmware-ovmf` base release.
2. Install the derivative package and verify the exact installed version with `dpkg-query`.
3. Cold-boot an ordinary OVMF guest and confirm the Austin Technology logo appears.
4. Cold-boot a Secure Boot guest.
5. Test a Windows vTPM/BitLocker guest and record whether recovery is requested.
6. Test any deployed SEV or TDX guest class.
7. Confirm the `.deb` checksum and installed firmware-file checksums are identical across all target nodes before cluster promotion.

## Safety

The change affects OVMF/UEFI only. SeaBIOS VMs need their own splash policy. Firmware changes can affect PCR measurements and prompt BitLocker or other TPM-sealed workflows for recovery; do not roll this package cluster-wide before the lab gates pass.
