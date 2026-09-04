# OK-WW Native macOS Foreground Port — Integration Plan

Status: implementation plan

Scope: **foreground-only native Mac client**

Target: Apple Silicon, macOS 13+, Python 3.12 arm64

Normative contract: `MACOS_ENGINEERING_CONSTRAINTS.md`

This plan defines sequencing and evidence. It cannot weaken the normative constraints. Deliberate deviations require an ADR before implementation proceeds.

## 1. Goal

On a supported Apple Silicon Mac, a user can launch the official Wuthering Waves client and OK-WW, grant normal macOS permissions, select the game window, run a task while the game remains frontmost, and have automation stop safely when focus or another required state is lost.

Target architecture:

```text
Official Wuthering Waves Mac client
        │
        ├── app/window target: AppKit + ScreenCaptureKit metadata
        ├── capture: persistent ScreenCaptureKit SCStream
        └── input: Quartz/Core Graphics foreground events
                         │
                         ▼
                    ok-script
             reusable platform contracts
                         │
                         ▼
             existing OK-WW task, OCR,
             template and combat logic
```

The first release does not support background/minimized control, BetterDisplay, virtual displays, private APIs, process injection, Metal hooks, Android emulation, or input while another application is frontmost.

## 2. Repository ownership

### `ok-script`

Owns reusable capabilities:

- platform-neutral desktop target and Windows adapter;
- macOS application/window discovery;
- ScreenCaptureKit capture;
- Quartz foreground input;
- focus guard and held-state release;
- cursor and permission services;
- geometry and coordinate conversion;
- platform provider routing, dependencies, imports, lifecycle, and tests.

### `ok-wuthering-waves`

Owns game integration:

- verified application/window matching hints;
- game hotkey defaults;
- CPU inference configuration;
- removal of direct Win32 cursor calls in `CombatCheck` and `MouseResetTask`;
- task compatibility decisions;
- evidence-driven Mac asset overrides;
- OK-WW user documentation, permissions, limitations, and troubleshooting.

Do not create an OK-WW-local capture/input backend or `win32api`-shaped compatibility shim.

## 3. Workspace and branch workflow

Use sibling repositories:

```text
workspace/
├── okww-macos-foreground-plan/
├── ok-script/
└── ok-wuthering-waves/
```

For each source repository:

- `origin` → contributor fork;
- `upstream` → `ok-oldking` canonical repository;
- integration branch → `feature/macos-foreground-mvp` from a recorded `upstream/master` SHA;
- push development commits only to the contributor fork;
- keep commits small and bisectable;
- do not open incremental MVP PRs.

Development dependency connection:

```bash
python3.12 -m venv .venv
./.venv/bin/python -m pip install -U pip
./.venv/bin/python -m pip install -e "../ok-script[ocr,qt]"
./.venv/bin/python -m pip install -e ".[dev]"
```

The initial install is expected to expose the current unconditional Windows dependencies. Record the failure; do not hide it with `--no-deps`, temporary wheels, a mutable branch URL, or global Python state.

## 4. Stage sequence

## Stage 0 — Workspace bootstrap and baseline evidence

Deliverables:

- writable contributor forks for both repositories;
- sibling local checkouts;
- verified `origin` and `upstream` remotes;
- matching integration branches and starting upstream SHAs;
- Apple Silicon/macOS/Xcode/Clang/Git/Python 3.12 baseline;
- OK-WW local `.venv`;
- repository constraints and agent instructions on actual branches;
- hardened `.gitignore` rules;
- dependency install/import/test baseline;
- committed and pushed bootstrap changes with no PR.

Evidence file:

```text
docs/development/acceptance/macos-stage0-bootstrap.md
```

Non-goals: no window discovery, capture, input, task, visual, or packaging implementation.

Gate:

- forks/remotes/branches/SHAs are recorded;
- constraints exist in both checkouts;
- reference environment and `.venv` exist;
- expected baseline failures are recorded and assigned to later stages;
- bootstrap commits are pushed to contributor forks;
- both worktrees are clean.

## Stage 1 — Guardrail confirmation and implementation inventory

Work:

- confirm contributor scope and forbidden mechanisms without inferring prior upstream-maintainer acceptance;
- inventory unconditional Win32 dependencies and imports in `ok-script`;
- inventory OK-WW direct OS calls, concrete backend checks, and Windows-only optional features;
- define the initial capability-state matrix, keeping every runtime capability at `not-implemented` until evidence advances it;
- create ADR directories, policy, and template in both repositories;
- record the coordinated upstream sync procedure and rollback expectations;
- map packaging, import, target, capture, input, task, CI, and packaging blockers to Stages 2–7.

Evidence:

```text
# ok-script
docs/development/macos-stage1-platform-inventory.md
docs/development/macos-integration-sync-and-rollback.md
docs/development/decisions/

# ok-wuthering-waves
docs/development/macos-stage1-game-inventory.md
docs/development/macos-capability-matrix.md
docs/development/macos-integration-sync-and-rollback.md
docs/development/decisions/
docs/development/acceptance/macos-stage1-inventory.md
```

Gate:

- no unresolved internal rule conflict;
- inventory maps each blocker to a file and stage;
- Windows-only implementations are distinguished from shared import blockers and are not scheduled for unnecessary rewrites;
- rollback and ADR processes are available before runtime changes;
- runtime implementation can proceed without changing product scope.

## Stage 2 — `ok-script` platform-safe dependencies and imports

Goals:

- install/import shared framework code on macOS;
- preserve Windows behavior;
- no production Mac capture or input yet.

Work:

- add environment markers for Windows-only packages;
- declare minimal macOS PyObjC wrappers;
- split common/Windows/macOS/ADB/browser key maps;
- make capture and interaction exports lazy/platform-selected;
- guard process/window/overlay/notification utilities;
- refactor DeviceManager provider imports;
- add Darwin and Windows import smoke tests.

Gate:

```bash
./.venv/bin/python -c "import ok"
./.venv/bin/python -c "from ok.device.DeviceManager import DeviceManager"
```

Both succeed on macOS without Win32 modules, task discovery imports, and Windows tests remain green.

## Stage 3 — Desktop target abstraction and Mac discovery

Implement:

- platform-neutral desktop target contract;
- Windows adapter around existing `HwndWindow` behavior;
- macOS app/window enumeration and selection data;
- PID/bundle/window identity;
- observed frontmost state and activation;
- process/window refresh and rebind diagnostics.

Selection strategy:

1. enumerate shareable content;
2. join windows to owning applications/PIDs;
3. apply verified game hints and plausible geometry;
4. allow explicit selection for ambiguity;
5. persist stable hints, not stale PID/window IDs.

Gate on the real game:

- correct process/window is visible;
- PID, bundle ID, window ID, title, and geometry are reported;
- activation is observed rather than assumed;
- Command-Tab state changes are detected;
- process exit and window replacement are detected.

## Stage 4 — Persistent ScreenCaptureKit backend

Implement:

```text
SCShareableContent
  → selected SCWindow
  → SCContentFilter(desktopIndependentWindow:)
  → SCStreamConfiguration
  → persistent SCStream
  → bounded latest-frame publication
  → owned BGR numpy.ndarray
```

Rules:

- cursor disabled;
- content area only;
- no per-frame screenshot requests;
- no OCR/task/Qt work in callback;
- BGRA/stride/padding handled deterministically;
- frame and geometry generations tracked;
- old frame invalidated on resize/rebind;
- permission and stream failures become actionable states with bounded backoff.

Tests:

- shape/dtype/channel order;
- row stride and padding;
- memory ownership after publication;
- bounded queue/latest frame;
- generation invalidation;
- scale/origin conversion.

Hardware gate:

- normalized 1920×1080 BGR frames;
- no cursor/title bar/border;
- correct color;
- at least 1000 consecutive frames without stall or queue growth;
- FPS/frame age observable;
- resize/rebind has a clear result.

## Stage 5 — Quartz foreground input and fail-closed state

Implement:

- Mac virtual key map;
- key tap/down/up;
- left/right/middle mouse down/up/click;
- absolute movement;
- scroll where required;
- relative/delta movement;
- foreground guard;
- held-state tracking;
- idempotent `release_all()`;
- explicit focus-loss pause/stop signal;
- shutdown ordering.

Safety ordering:

```text
verify target exists
→ verify bound process
→ verify frontmost
→ publish short event/batch
```

On invalidation:

```text
block new ordinary input
→ emit only matching up events for held state
→ clear internal state
→ pause/stop with an explicit reason
```

Hardware gate:

- W tap and hold/release;
- E/Q/R/F, Space, Shift, Tab;
- left/middle/right button behavior;
- absolute click mapping;
- camera delta X/Y;
- W + attack + camera;
- Command-Tab while holding keys/buttons produces no ordinary input in the new app;
- stop/exit releases state.

Relative camera failure blocks combat/route support claims.

## Stage 6 — OK-WW integration

Change:

- add a verified `macos` device configuration;
- disable/ignore NPU on Darwin and use a proven arm64 CPU inference path;
- replace `CombatCheck` cursor calls with framework CursorService;
- replace or explicitly disable Windows-only `MouseResetTask` behavior through framework capabilities;
- declare task compatibility where needed;
- add user-visible permission/focus states and translations;
- validate existing recognition on normalized Mac frames.

Bring-up order:

1. screenshot and feature diagnostics;
2. simple menu click flow;
3. Auto Pick or another simple trigger flow;
4. fixed-domain/basic combat;
5. map/route flows;
6. broad task matrix.

Visual validation groups:

- login/entry;
- overworld HUD and team state;
- skill/liberation/echo readiness;
- F interaction;
- guidebook/map/teleport;
- stamina/claim/confirmation;
- backpack/echo enhancement;
- domain start/result;
- combat target/lock state.

Prefer geometry/normalization/threshold fixes. Add `assets/macos` only for reproducible platform-specific differences that cannot be fixed without harming Windows.

## Stage 7 — CI and packaged application

CI:

- Python 3.12 macOS job;
- dependency install;
- import smoke;
- all task imports;
- provider, geometry, capture-contract, held-state, focus and shutdown tests;
- no game requirement;
- existing Windows CI remains green.

After source mode is stable:

- build an internal `.app` through the supported PySide deployment path, preferring `pyside6-deploy`/Nuitka;
- use a stable bundle identifier;
- verify arm64 libraries, Qt plugins, OpenCV/inference/PyObjC, assets and i18n;
- validate Screen Recording and Accessibility under the packaged identity;
- verify application shutdown releases input and capture resources.

Public release additionally requires Developer ID Application signing, Hardened Runtime, secure timestamp, notarization, stapling and Gatekeeper validation in a clean environment.

## Stage 8 — Acceptance freeze and final MVP PRs

Freeze feature scope and run the complete automated and manual matrix.

Required evidence:

- Windows and macOS automated results;
- real-hardware window/capture/keyboard/mouse/camera/focus-loss results;
- Mac model, architecture, macOS version, game version, resolution and window mode;
- packaged-app permission behavior;
- supported and unsupported task list;
- known limitations and rollback notes;
- immutable cross-repository dependency relationship.

Only then open one cohesive MVP PR in each affected repository and link them as one delivery unit.

## 5. File-level map

### `ok-script`

Likely areas:

```text
pyproject.toml
ok/device/DeviceManager.py
ok/device/capture_methods/
ok/device/interaction_methods/
ok/device/window_targets/
ok/device/services/
ok/util/process.py
ok/util/window.py
ok/ui/overlay/
ok/notification/
tests/
```

Illustrative new shape:

```text
ok/device/
├── capture_methods/
│   ├── base.py
│   ├── windows/
│   └── macos/screencapturekit.py
├── interaction_methods/
│   ├── base.py
│   ├── windows/
│   └── macos/
│       ├── keys.py
│       └── quartz_foreground.py
├── window_targets/
│   ├── base.py
│   ├── windows.py
│   └── macos.py
└── services/
    ├── cursor.py
    └── permissions.py
```

Use a smaller refactor when it preserves compatibility better; ownership matters more than directory aesthetics.

### `ok-wuthering-waves`

```text
config.py
src/combat/CombatCheck.py
src/task/MouseResetTask.py
assets/macos/                 # only when evidence requires
.github/workflows/test.yml
docs/
i18n/
```

## 6. Test architecture

### Unit tests

Provider selection:

- Windows chooses Windows providers;
- Darwin chooses Mac providers;
- Darwin does not load Win32;
- Windows does not require PyObjC.

Geometry:

- frame pixel to screen point;
- scale 1.0, 2.0 and observed non-integer scale;
- origin offsets;
- resize and generation replacement;
- stale generation rejection.

Held input:

- down adds state;
- up removes state;
- repeated down behavior is intentional;
- `release_all()` is best-effort and idempotent;
- one release error does not prevent the rest;
- state is cleared after release attempts.

Focus/concurrency:

- correct PID permits ordinary input;
- other PID or missing target rejects it;
- invalidation closes the input gate;
- no ordinary event follows invalidation;
- release path emits only recorded up events;
- task receives an explicit pause/stop reason.

Capture:

- synthetic BGRA buffers;
- dimensions, stride, padding, BGR conversion and alpha removal;
- publication ownership;
- latest-frame/bounded-buffer behavior;
- fatal/rebind states.

### Integration tests without game

- deterministic adapters around Apple API boundaries;
- optional shareable-content diagnostics outside required CI;
- headless/offscreen Qt where supported;
- application and all task modules import;
- no permission prompt in deterministic unit tests.

### Real hardware

Record separately; GitHub Actions does not install the game. Validate at least one supported M1-class or later machine, and more than one supported macOS major version where practical.

## 7. Failure-state design

Use explicit states such as:

```text
MAC_SCREEN_CAPTURE_PERMISSION_REQUIRED
MAC_ACCESSIBILITY_PERMISSION_REQUIRED
MAC_GAME_NOT_FOUND
MAC_GAME_WINDOW_NOT_FOUND
MAC_GAME_NOT_FOREGROUND
MAC_CAPTURE_STREAM_STOPPED
MAC_CAPTURE_REBIND_FAILED
MAC_UNSUPPORTED_GEOMETRY
MAC_INPUT_POST_FAILED
MAC_CAMERA_INPUT_UNSUPPORTED
```

A terminal state must not become an endless task loop.

## 8. Capability and evidence protocol

Track each capability as:

1. `not-implemented`
2. `unit-tested`
3. `hardware-validated`
4. `packaged-app-validated`

Each result records commit SHA, exact command or manual procedure, host/macOS/game details where applicable, resolution/window mode, and outcome. A regression reopens the gate. README, UI, PR and release claims use the lowest demonstrated state.

## 9. Major risks

### Relative camera input

Highest functional risk. Validate before task integration; isolate the API so the Quartz technique can change without task changes. Failure limits the product to menu/basic tasks.

### Wider Win32 import graph

Use full application/task import smoke tests and repository searches for `win32`, `windll`, `WinDLL`, `winreg`, Windows overlays and notifications.

### Retina coordinate mismatch

Use one frame-pixel model, immutable geometry snapshots, conversion tests, and diagnostics showing source and posted coordinates.

### Permission identity mismatch

Package with a stable bundle ID before declaring the hardware matrix complete. Terminal/Python permission is not final evidence.

### Window identity changes

Match application/process plus window properties, support rebind, and avoid title-only or stale-ID matching.

### CPU inference performance

Establish correctness first, profile actual task frequency/ROI, then optimize based on measurements.

## 10. Definition of success

A successful first native Mac port means:

> On Apple Silicon running macOS 13+, the user launches the official Wuthering Waves Mac client and OK-WW, grants supported permissions, selects the game, runs an OK-WW task through ScreenCaptureKit and Quartz while the game remains frontmost, and sees automation stop safely if the user leaves the game or another required state fails.

It does not mean the game can run minimized or while the user actively operates another application.
