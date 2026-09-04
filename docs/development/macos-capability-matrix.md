# OK-WW macOS Foreground MVP — Capability Matrix

Recorded: 2026-09-04

Scope baseline: after Stage 1 inventory, before runtime implementation

## Status vocabulary

Only these states are used for macOS runtime capabilities:

1. `not-implemented`
2. `unit-tested`
3. `hardware-validated`
4. `packaged-app-validated`

A capability advances only when its own evidence passes at the referenced commit. A later regression, relevant upstream sync, dependency change, capture/input architecture change, or packaged-identity change reopens the affected gate.

Stage 0/1 documentation and repository setup are complete, but they do not advance any runtime capability above `not-implemented`.

## Framework and installation

| ID | Capability | Owner | Current state | Next required evidence |
|---|---|---|---|---|
| CAP-01 | Normal arm64 macOS dependency resolution | `ok-script` | `not-implemented` | Stage 2 install succeeds without selecting Windows-only distributions. |
| CAP-02 | Deterministic PEP 517/editable framework build | `ok-script` | `not-implemented` | Stage 2 editable metadata/build succeeds without undeclared build imports or network-derived version state. |
| CAP-03 | `import ok` from installed environment | `ok-script` | `not-implemented` | Stage 2 clean-environment import test. |
| CAP-04 | `DeviceManager` and core executor import without Win32 | `ok-script` | `not-implemented` | Stage 2 import-isolation test and `sys.modules` assertion. |
| CAP-05 | Qt application/start modules import on Darwin | `ok-script` | `not-implemented` | Stage 2 headless/offscreen import test without Win32 global-hotkey modules. |
| CAP-06 | All registered OK-WW modules import on Darwin | both | `not-implemented` | Stage 2 framework gate plus Stage 6 removal of game-level OS imports. |
| CAP-07 | Windows provider behavior preserved after platform split | `ok-script` | `not-implemented` | Stage 2 Windows import/unit/CI regression results for changed paths. |

## Desktop target and permissions

| ID | Capability | Owner | Current state | Next required evidence |
|---|---|---|---|---|
| CAP-10 | Platform-neutral desktop target contract | `ok-script` | `not-implemented` | Stage 3 contract tests with fake targets and Windows adapter. |
| CAP-11 | Existing HWND behavior through Windows adapter | `ok-script` | `not-implemented` | Stage 3 Windows regression tests. |
| CAP-12 | Enumerate official Mac application/window candidates | `ok-script` + OK-WW hints | `not-implemented` | Stage 3 real-hardware discovery record. |
| CAP-13 | Stable PID/application/window binding and refresh | `ok-script` | `not-implemented` | Stage 3 unit tests and process/window-recreation hardware test. |
| CAP-14 | Observe frontmost state | `ok-script` | `not-implemented` | Stage 3 fake-adapter tests and Command-Tab hardware observation. |
| CAP-15 | Request activation and verify observed activation | `ok-script` | `not-implemented` | Stage 3 hardware validation; API return alone is insufficient. |
| CAP-16 | Screen-capture permission status/request service | `ok-script` | `not-implemented` | Stage 3/4 unit states and hardware permission test. |
| CAP-17 | Accessibility permission status/request service | `ok-script` | `not-implemented` | Stage 3/5 unit states and hardware permission test. |

## Capture and geometry

| ID | Capability | Owner | Current state | Next required evidence |
|---|---|---|---|---|
| CAP-20 | Persistent selected-window ScreenCaptureKit `SCStream` | `ok-script` | `not-implemented` | Stage 4 implementation and unit contracts. |
| CAP-21 | BGR `uint8` `(height, width, 3)` frame output | `ok-script` | `not-implemented` | Synthetic buffer/stride tests, then real-window frame evidence. |
| CAP-22 | Content-only frame without cursor/title/border/shadow | `ok-script` | `not-implemented` | Stage 4 real-hardware screenshots and inspection. |
| CAP-23 | Bounded latest-frame publication and ownership | `ok-script` | `not-implemented` | Stage 4 concurrency/ownership/queue tests. |
| CAP-24 | Capture/window recreation and bounded rebind | `ok-script` | `not-implemented` | Stage 4 failure/rebind unit tests and hardware result. |
| CAP-25 | Geometry generation and stale-frame rejection | `ok-script` | `not-implemented` | Stage 3/4 unit tests. |
| CAP-26 | Frame-pixel to global coordinate conversion | `ok-script` | `not-implemented` | Scale 1.0, 2.0, non-integer/observed scale and origin tests; hardware click mapping later. |
| CAP-27 | Stable 1920×1080 continuous capture | `ok-script` | `not-implemented` | At least 1000 frames, FPS/frame-age and leak/queue observations on the official client. |

## Foreground input and safety

| ID | Capability | Owner | Current state | Next required evidence |
|---|---|---|---|---|
| CAP-30 | Quartz key tap/down/up | `ok-script` | `not-implemented` | Stage 5 fake event-sink tests, then official-game hardware validation. |
| CAP-31 | Left/right/middle mouse down/up/click | `ok-script` | `not-implemented` | Stage 5 unit and hardware tests. |
| CAP-32 | Absolute movement/click coordinate mapping | `ok-script` | `not-implemented` | Geometry unit tests and official-game hardware validation. |
| CAP-33 | Relative/delta camera X/Y | `ok-script` | `not-implemented` | Stage 5 hardware validation; blocks combat/route claims. |
| CAP-34 | Held-key/button state tracking | `ok-script` | `not-implemented` | Stage 5 deterministic state tests. |
| CAP-35 | Idempotent best-effort `release_all()` | `ok-script` | `not-implemented` | Stage 5 tests including individual release failure and vanished target. |
| CAP-36 | Foreground guard immediately before events | `ok-script` | `not-implemented` | Stage 5 focus-race tests and hardware focus-loss test. |
| CAP-37 | No ordinary input after invalidation | `ok-script` | `not-implemented` | Stage 5 concurrent event-gate tests. |
| CAP-38 | Safe shutdown/target-loss/capture-loss/permission-loss release | `ok-script` | `not-implemented` | Stage 5 lifecycle tests, then hardware/package validation. |
| CAP-39 | Platform-neutral cursor service | `ok-script` | `not-implemented` | Stage 5 Windows/Mac service tests; consumed by OK-WW in Stage 6. |

## OK-WW integration and recognition

| ID | Capability | Owner | Current state | Next required evidence |
|---|---|---|---|---|
| CAP-40 | Verified Mac game matching configuration | OK-WW | `not-implemented` | Stage 3 observations followed by Stage 6 config integration. |
| CAP-41 | Mac-safe game hotkey mapping | OK-WW | `not-implemented` | Stage 6 official-client key validation. |
| CAP-42 | `CombatCheck` uses framework cursor/geometry services | OK-WW | `not-implemented` | Stage 6 tests after CAP-39. |
| CAP-43 | `MouseResetTask` explicit Mac behavior | OK-WW | `not-implemented` | Stage 6 explicit disablement or framework-service implementation and tests. |
| CAP-44 | Concrete PostMessage type checks removed from task behavior | OK-WW | `not-implemented` | Stage 6 activation-capability tests. |
| CAP-45 | Cross-platform screenshot-folder open/reveal | both | `not-implemented` | Framework service plus Stage 6 task tests. |
| CAP-46 | CPU OCR/inference loads on arm64 | OK-WW | `not-implemented` | Stage 6 model/runtime import and correctness tests with NPU disabled. |
| CAP-47 | Existing templates/OCR work on normalized Mac frames | OK-WW | `not-implemented` | Stage 6 offline visual suite and real-frame evidence. |
| CAP-48 | Simple non-combat task end-to-end | OK-WW | `not-implemented` | Stage 6 official-client hardware run. |
| CAP-49 | Representative combat flow end-to-end | OK-WW | `not-implemented` | CAP-33 hardware validation plus Stage 6 combat run. |
| CAP-50 | Route/map flow end-to-end | OK-WW | `not-implemented` | CAP-33 and navigation hardware validation. |

## CI, packaging, and release

| ID | Capability | Owner | Current state | Next required evidence |
|---|---|---|---|---|
| CAP-60 | Game-independent macOS Python 3.12 CI | both | `not-implemented` | Stage 7 green dependency/import/unit jobs. |
| CAP-61 | Windows CI remains green for affected paths | both | `not-implemented` | Stage 2 onward, recorded on every platform-layer change. |
| CAP-62 | Internal arm64 `.app` launches without shell | OK-WW | `not-implemented` | Stage 7 packaged build validation. |
| CAP-63 | Packaged Screen Recording permission | both | `not-implemented` | Stable bundle-ID `.app` permission grant/revoke validation. |
| CAP-64 | Packaged Accessibility permission and input | both | `not-implemented` | Stable bundle-ID `.app` permission and focus-safety validation. |
| CAP-65 | Packaged shutdown releases input/capture | both | `not-implemented` | Stage 7 packaged lifecycle validation. |
| CAP-66 | Developer ID, Hardened Runtime, notarization, staple | release | `not-implemented` | Public-release gate after MVP acceptance; credentials never enter the repository. |

## Claim boundary

As of this record:

- no Mac runtime capability may be described as supported;
- no menu, task, combat, route, background, packaged, or permission capability is implemented;
- Stage 0 and Stage 1 establish only a controlled workspace, normative constraints, inventory, decision process, and rollback process;
- combat and route claims remain blocked until CAP-33 is at least `hardware-validated`;
- public distribution remains blocked until the relevant core capabilities are `packaged-app-validated` and CAP-66 passes.
