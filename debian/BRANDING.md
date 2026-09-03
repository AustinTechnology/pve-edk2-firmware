# Austin Technology OVMF branding

This derivative changes only `debian/Logo.bmp`, which the upstream Proxmox build copies to `MdeModulePkg/Logo/Logo.bmp` before compiling every firmware variant.

## Included assets

| File | Purpose | SHA-256 |
| --- | --- | --- |
| `branding-source.svg` | Original Austin Technology vector artwork supplied for this build | `9572a039233336f39abc5a19e524db116ca9efbc5482070eeeff37a2dd1c800f` |
| `Logo.bmp` | Firmware input: uncompressed 512×160, 24-bit BMP, dark navy background and safe margins | `cc6d477d5888c177f87181c2d68ed269818d5b09e27994c295e74c7eccd240c0` |

## Scope

The resulting `pve-edk2-firmware-ovmf` package brands the normal OVMF, Secure Boot OVMF, SEV, TDX, and MicroVM images built from this source revision. It does not change guest EFI variable stores or Secure Boot keys.

SeaBIOS is a separate firmware implementation and is intentionally out of scope.

## Update policy

Rebase this derivative onto each Proxmox EDK2 firmware release. Confirm that upstream still copies `debian/Logo.bmp` in `debian/rules`, rebuild the package, then repeat the lab boot and Secure Boot/BitLocker gates before promotion.
