# Codex Windows Update Issue Log - 2026-07-11

## Scope

Primary task: fix Codex GUI/Desktop update on Windows.

Secondary issues to handle later:
- Valorant/WeGame client connection error when FLClash is not running.
- System-wide proxy state is currently tied to FLClash at `127.0.0.1:7890`.

## Current Codex State

- Codex CLI was updated successfully from `0.128.0` to `0.144.1`.
- Codex GUI/Desktop package is still `OpenAI.Codex_26.616.3767.0_x64__2p2nqsd0c76g0`.
- Official minimum for GPT-5.6 in Codex desktop mode is `26.707.30751`.
- Official Windows install command is `winget install Codex -s msstore`, but local text search for `Codex` resolves to an unrelated QR app.
- Exact Microsoft Store product id for the OpenAI desktop app is `9PLM9XGG6VKS`.

## Observed GUI Update Failure

Codex Desktop logs repeatedly show:

```text
[windows-store-updater] Checking Windows Store for package updates buildVersion=26.616.3767.0 manifestBuildVersion=26.707.3748.0 packageIdentity=OpenAI.Codex
[windows-store-updater] Failed to check for Windows Store updates errorMessage=参数错误。
```

Interpretation:
- The GUI updater can see a newer manifest version.
- The failure happens when it asks the Windows Store/MSIX update path to check or install updates.

## Network And Proxy Findings

- FLClash listens on `127.0.0.1:7890`.
- Windows system proxy points to `127.0.0.1:7890`.
- WinHTTP proxy points to `127.0.0.1:7890`.
- User environment variables `HTTP_PROXY`, `HTTPS_PROXY`, and `ALL_PROXY` point to `http://127.0.0.1:7890`.
- When FLClash is not running, programs that honor these proxy settings may try to connect to a dead local proxy and report connection errors.

## Changes Already Applied

- Started `ClipSVC`.
- Refreshed `msstore` source.
- Re-registered:
  - `Microsoft.WindowsStore`
  - `Microsoft.DesktopAppInstaller`
  - `Microsoft.StorePurchaseApp`
- Added loopback exemption for:
  - `microsoft.windowsstore_8wekyb3d8bbwe`
  - `microsoft.storepurchaseapp_8wekyb3d8bbwe`

## Current Hypothesis

The Codex GUI update failure is likely caused by the interaction between:
- MSIX/Microsoft Store update APIs,
- system-wide proxy pointing to `127.0.0.1:7890`,
- FLClash loopback/proxy behavior,
- and Store package identity/update resolution.

## Next Actions

1. Try forcing Microsoft Store to reinstall/update product `9PLM9XGG6VKS`.
2. If Store CLI still says no update, reset Microsoft Store cache and reopen the exact product page.
3. Restart Codex Desktop and verify whether the updater still logs `参数错误`.
4. Only after Codex update is resolved, handle the Valorant/WeGame proxy dependency separately.

## Resolution (2026-07-11 14:45 CST)

- Codex Desktop update completed successfully: `OpenAI.Codex_26.707.3748.0_x64__2p2nqsd0c76g0`, package status `Ok`.
- Enabled `respect_system_proxy = true` in `C:\Users\Administrator\.codex\config.toml`.
- Removed user-level `HTTP_PROXY`, `HTTPS_PROXY`, `ALL_PROXY`, and `NO_PROXY` from `HKCU\Environment`.
- Reset WinHTTP to direct access with `netsh winhttp reset proxy`.
- Kept FL Clash `systemProxy = true` and TUN disabled. FL Clash now remains the only owner of the WinINET proxy switch.
- Verified Codex with a clean child-process environment: one request completed successfully and returned `PROXY_OK` using only the Windows system proxy.
- Verified direct Microsoft Store connectivity and confirmed Store/App Installer/Purchase App packages are healthy.
- Live Valorant/WeGame processes were not interrupted for an off-proxy test. The persistent dead-proxy layers that caused the off-proxy failure have been removed.

Backups and rollback notes: `adhoc_jobs/codex_network_repair_20260711/`.
