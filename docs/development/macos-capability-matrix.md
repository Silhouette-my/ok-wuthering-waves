# OK-WW macOS 前台模式——能力与任务兼容矩阵

记录日期：2026-09-04

适用分支：`feature/macos-foreground-mvp`

状态：阶段 A/B 的本地与远端无游戏 gate 已通过；阶段 C 的窗口目标、fake discovery/rebind、前台观察和权限状态契约已通过本地单元测试。Stage C 远端 runner、真实《鸣潮》和 packaged `.app` 仍待验收。

## 1. 两个独立状态轴

### 1.1 provider capability evidence

仅使用：

1. `not-implemented`：没有可执行实现，或实现尚未满足最低单元契约；
2. `unit-tested`：无游戏环境中的确定性接口/状态/导入测试通过；
3. `hardware-validated`：在官方《鸣潮》Mac 客户端和真实硬件上通过；
4. `packaged-app-validated`：在稳定 bundle identifier 的内部 `.app` 身份下通过。

单元测试不能替代真实窗口、TCC 或游戏输入证据。相关架构、依赖、系统或 packaged identity 变化会重新打开 gate。

### 1.2 task support status

- `validated`：该任务在相应能力等级下真机端到端通过；
- `experimental`：可以在底层 capability 满足后进行真机验收，但不得对用户描述为稳定支持；
- `unsupported`：不可在当前 Mac MVP 执行。

任务状态不等于 provider evidence。当前没有任务达到 `validated`。

## 2. 精确设备能力

`ok-script` 的 `DeviceCapabilities` 包含：

```text
keyboard_tap
keyboard_hold
absolute_mouse
mouse_left
mouse_right
mouse_middle
mouse_button_hold
scroll
relative_mouse
foreground_only
```

所有字段默认 `False`。任务在 enable 前和真正执行前检查要求；未实现后端或空方法不会自动形成能力。

`relative_mouse` 专指自由镜头相对/delta 输入，不等于任务层把百分比坐标换算为绝对坐标的 `move_relative` helper。

## 3. 任务能力等级

| 等级 | 定义 | relative mouse 是否必需 |
|---|---|---|
| `MAC_BASIC` | 菜单、登录、领取、合成、背包、强化、固定页面 OCR/模板、绝对点击 | 否 |
| `MAC_LOCKED_GAMEPLAY` | 持续 W/A/S/D、中键锁敌/居中、左右键保持、键鼠组合和视觉方向选择 | 否 |
| `MAC_FULL_CAMERA` | 任意 relative X/Y、连续 delta、精确路线转向和自由镜头寻路 | 是 |

relative mouse 缺失只阻止 `MAC_FULL_CAMERA` 和明确声明该字段的任务，不阻止已通过的 basic/locked task。

## 4. 框架安装与导入

| ID | 能力 | Owner | 当前证据 | 已有证据 | 下一门槛 |
|---|---|---|---|---|---|
| CAP-01 | arm64 macOS 正常 dependency resolution，不选择 Windows-only distribution | `ok-script` | `unit-tested` | sibling editable install 和 `pip check` 在参考 Mac 环境成功；metadata marker tests 通过 | Windows/macOS CI 重跑及最终 immutable dependency |
| CAP-02 | 确定性 PEP 517/editable build | `ok-script` | `unit-tested` | 普通 build/editable 不再依赖未声明 import 或默认 PyPI 版本查询；package metadata tests 通过 | clean CI build 和最终 release version 流程 |
| CAP-03 | 从安装环境 `import ok` | `ok-script` | `unit-tested` | 从临时工作目录导入测试通过 | macOS CI |
| CAP-04 | `DeviceManager` / executor / shared capture/interaction 导入不加载 Win32 | `ok-script` | `unit-tested` | `tests/test_platform_imports.py` 与完整 framework suite 通过 | macOS CI |
| CAP-05 | Qt app/start/debug/notification optional modules 在 Darwin 可导入 | `ok-script` | `unit-tested` | headless/offscreen import contracts 通过 | native WindowServer UI smoke 与 packaged app |
| CAP-06 | 所有登记 OK-WW entry/task/scene/custom tab 在 Darwin 可导入 | both | `unit-tested` | `tests/test_macos_imports.py` 通过，无 forbidden module | macOS CI |
| CAP-07 | Windows provider 行为在平台拆分后保持 | `ok-script` | `unit-tested` | Windows branch workflow 已通过；Stage C 新增 HWND adapter 另有 fake contract tests | Stage C 提交后的 Windows runner 重跑 |
| CAP-08 | `DeviceCapabilities` 默认 fail-closed、matching 和 task preflight | `ok-script` | `unit-tested` | `tests/test_device_capabilities.py` 通过；enable/execute 前检查 | 在真实 Mac provider 接入后重跑 |
| CAP-09 | 所有登记 OK-WW task 有明确 Mac declaration | OK-WW | `unit-tested` | `tests/test_macos_capabilities.py` 检查 17/17 覆盖 | 真实 capability 与 task end-to-end |

## 5. Desktop target、窗口与权限

| ID | 能力 | 当前证据 | 下一门槛 |
|---|---|---|---|
| CAP-10 | 平台中立 `DesktopWindowTarget` contract | `unit-tested` | immutable snapshot、明确 coordinate-space、丢失清空与 generation contract tests | Stage D frame/geometry integration |
| CAP-11 | 现有 HWND 行为通过 Windows adapter | `unit-tested` | composition fake `HwndWindow` adapter tests；未改 Windows capture/input 主路径 | Stage C 提交后的 Windows unit/CI regression |
| CAP-12 | 枚举官方 Mac app/window candidates | `not-implemented` | 真实客户端 discovery record |
| CAP-13 | PID/bundle/window binding、manual selection 与 refresh/rebind | `unit-tested` | fake adapter 覆盖稳定 hint、歧义手选、PID/window replacement、bind 前二次枚举/liveness recheck、刷新期/异常 fail closed | 官方客户端 process/window recreation hardware test |
| CAP-14 | 观察系统 frontmost 状态 | `unit-tested` | fake adapter 覆盖实时 frontmost 观察；不使用枚举时的旧快照代替观察 | Command-Tab hardware observation |
| CAP-15 | request activation 后确认 observed activation | `unit-tested` | contract tests 证明 request accepted 不等于 observed frontmost | real-game hardware validation |
| CAP-16 | Screen Recording permission status/request/revoke | `unit-tested` | public API mapping 与 required/requested/granted/revoked/error 状态机 fake tests；并发请求串行化且 requested 后禁止重复请求 | source identity hardware + stable `.app` TCC |
| CAP-17 | Accessibility permission status/request/revoke | `unit-tested` | public API mapping 与 required/requested/granted/revoked/error 状态机 fake tests；并发请求串行化且 requested 后禁止重复请求 | source identity hardware + stable `.app` TCC |
| CAP-18 | 稳定 bundle identifier 的早期内部 `.app` identity checkpoint | `not-implemented` | 阶段 C 后从 `/Applications` 验证 permission persistence |

## 6. Capture 与 geometry

| ID | 能力 | 当前证据 | 下一门槛 |
|---|---|---|---|
| CAP-20 | selected-window persistent `SCStream` | `not-implemented` | 阶段 D implementation + lifecycle tests |
| CAP-21 | BGR `uint8` `(height,width,3)` frame | `not-implemented` | synthetic BGRA/stride tests，再做 hardware frame |
| CAP-22 | content-only frame，无 cursor/title/border/shadow | `not-implemented` | official-client screenshot inspection |
| CAP-23 | bounded latest-frame publication 与 ownership | `not-implemented` | concurrency/ownership/overwrite tests |
| CAP-24 | stream/window recreation 与 bounded rebind | `not-implemented` | failure/rebind tests + hardware |
| CAP-25 | immutable geometry generation 与 stale-frame rejection | `not-implemented` | generation unit tests |
| CAP-26 | frame pixel → global logical/CGEvent coordinate | `not-implemented` | scale 1.0/2.0/非整数、offset、crop、resize tests |
| CAP-27 | 1920×1080 1000+ continuous frames | `not-implemented` | official-client FPS/frame-age/leak/queue evidence |
| CAP-28 | 同时诊断 outer frame、actual frame、content、scale 和 posted coordinate | `not-implemented` | 阶段 D diagnostics |

## 7. Foreground input 与安全

| ID | 能力 | 当前证据 | 下一门槛 |
|---|---|---|---|
| CAP-30 | Quartz key tap | `not-implemented` | fake event sink + official game |
| CAP-31 | Quartz key down/up/hold | `not-implemented` | held-state unit + W/A/S/D hardware |
| CAP-32 | left/right/middle down/up/click | `not-implemented` | unit + game hardware |
| CAP-33 | absolute mouse coordinate mapping | `not-implemented` | geometry unit + game hardware |
| CAP-34 | scroll | `not-implemented` | unit + task hardware |
| CAP-35 | `HeldInputState` keys/buttons/owner/invalidation | `not-implemented` | deterministic state/concurrency tests |
| CAP-36 | idempotent best-effort `release_all()` | `not-implemented` | release failure、vanished target、repeat tests |
| CAP-37 | `ForegroundGuard` immediately before ordinary event/batch | `not-implemented` | focus-race tests + Command-Tab hardware |
| CAP-38 | invalidation 后无 ordinary event，只允许 matching release | `not-implemented` | concurrent gate tests + hardware leak test |
| CAP-39 | task/capture/permission/device/app shutdown release ordering | `not-implemented` | lifecycle tests + packaged app |
| CAP-40 | platform-neutral CursorService seam | `unit-tested` | unavailable/Windows seam tests 已通过；Mac Quartz implementation 未完成 | 阶段 E Mac implementation + hardware |
| CAP-41 | relative/delta mouse X/Y | `not-implemented` | 阶段 F 第三优先级 hardware；只阻止 full-camera claims |
| CAP-42 | W/A/S/D + left/skill/middle/right-hold combinations | `not-implemented` | 阶段 F official-game matrix；通过后可开放 locked tasks |

## 8. OK-WW integration 与 recognition

| ID | 能力 | 当前证据 | 下一门槛 |
|---|---|---|---|
| CAP-50 | 真实 Mac game matching config | `not-implemented` | 阶段 C 实测 bundle/app/window hints |
| CAP-51 | Mac logical key set / game hotkeys | `not-implemented` | Quartz map unit + official-client key validation |
| CAP-52 | `CombatCheck` 不直接调用 Win32，使用 framework cursor seam | `unit-tested` | import/unit tests 通过；Mac CursorService 未实现 | 阶段 E/F hardware |
| CAP-53 | `MouseResetTask` Mac P0 显式 unsupported | `unit-tested` | capability declaration/preflight test | UI 文案和 packaged behavior |
| CAP-54 | task 不依赖具体 `PostMessageInteraction` 类型 | `unit-tested` | existing task regression/import tests | Windows CI |
| CAP-55 | cross-platform screenshot-folder open/reveal | `not-implemented` | platform service + task tests |
| CAP-56 | CPU OCR/inference arm64，NPU disabled/ignored | `not-implemented` | model load/correctness/performance tests |
| CAP-57 | existing template/OCR on normalized Mac frame | `not-implemented` | offline real-frame suite |
| CAP-58 | UI 显示 task status / missing capabilities，并阻止新 enable | `unit-tested` | framework `TaskCard` status-code badge tests 通过；Windows compatible task 不显示额外 badge | 阶段 G 补 level/本地化说明并做真实 provider UI 验收 |

## 9. Task compatibility

下表是当前代码审计后的**候选验收范围**，不是用户支持声明。

| Task | Level | Required capability 摘要 | 当前状态 | 下一证据 |
|---|---|---|---|---|
| `MergeEchoTask` | `MAC_BASIC` | key tap、absolute mouse、left、foreground-only | `experimental` | normalized frame + end-to-end |
| `EnhanceEchoTask` | `MAC_BASIC` | key tap、absolute mouse、left、foreground-only | `experimental` | end-to-end |
| `ChangeEchoTask` | `MAC_BASIC` | key tap、absolute mouse、left、foreground-only | `experimental` | end-to-end |
| `AutoLoginTask` | `MAC_BASIC` | absolute mouse、left、foreground-only | `experimental` | login/notice hardware |
| `AutoPickTask` | `MAC_BASIC` | key tap、scroll、foreground-only | `experimental` | F-key/候选滚动 trigger hardware |
| `AutoDialogTask` | `MAC_BASIC` | absolute mouse、left、foreground-only | `experimental` | dialog hardware |
| `FastTravelTask` | `MAC_BASIC` | absolute mouse、left、foreground-only | `experimental` | fast-travel hardware |
| `AutoCombatTask` | `MAC_LOCKED_GAMEPLAY` | key tap/hold、absolute、left/middle、button hold、foreground-only | `experimental` | locked input matrix + representative combat |
| `FarmEchoTask` | `MAC_LOCKED_GAMEPLAY` | locked baseline + right + scroll | `experimental` | movement/combat/pickup end-to-end |
| `NightmareNestTask` | `MAC_LOCKED_GAMEPLAY` | locked baseline + scroll | `experimental` | end-to-end |
| `TacetTask` | `MAC_LOCKED_GAMEPLAY` | locked baseline + scroll | `experimental` | end-to-end |
| `ForgeryTask` | `MAC_LOCKED_GAMEPLAY` | locked baseline + scroll | `experimental` | end-to-end |
| `SimulationTask` | `MAC_LOCKED_GAMEPLAY` | locked baseline + scroll | `experimental` | end-to-end |
| `DailyTask` | `MAC_LOCKED_GAMEPLAY` | 编排子任务，按最宽依赖 | `experimental` | constituent tasks + end-to-end |
| `MultiAccountDailyTask` | `MAC_LOCKED_GAMEPLAY` | 编排 DailyTask，按最宽依赖 | `experimental` | account flow + end-to-end |
| `GardenTask` | `MAC_LOCKED_GAMEPLAY` | key tap/hold、absolute、left、foreground-only | `experimental` | end-to-end |
| `MouseResetTask` | — | Windows workaround | `unsupported` | 只有真机证明确有必要才重新设计 |

当前没有登记任务要求 `MAC_FULL_CAMERA` 或 `relative_mouse=True`。未来任务如调用自由镜头 delta，必须显式升级 requirement，并在 CAP-41 硬件通过前被拒绝。

## 10. 端到端与发布声明

| ID | 能力 | 当前证据 | 下一门槛 |
|---|---|---|---|
| CAP-60 | 一个 `MAC_BASIC` task end-to-end | `not-implemented` | 阶段 G real game |
| CAP-61 | Auto Pick 或其他 key-tap trigger end-to-end | `not-implemented` | CAP-30/37 后 hardware |
| CAP-62 | 一个 `MAC_LOCKED_GAMEPLAY` representative flow | `not-implemented` | CAP-31/32/36/37/42 hardware |
| CAP-63 | `MAC_FULL_CAMERA` route flow | `not-implemented` | CAP-41 hardware + route end-to-end |
| CAP-64 | 当前全部 task 兼容矩阵与 UI 一致 | `not-implemented` | 阶段 G automated + hardware evidence |

CAP-41 未通过时不阻止 CAP-60，也不阻止已经通过的 CAP-62；但 CAP-63 与 full-camera/complete-route claims 保持关闭。

## 11. CI、packaging 与公开发布

| ID | 能力 | 当前证据 | 下一门槛 |
|---|---|---|---|
| CAP-70 | macOS Python 3.12 no-game branch CI | `unit-tested` | OK-WW guardrail run `33860501014` 的 `macos-latest` job 通过；Stage C 尚待重跑 | Stage C 提交后的远端绿色 |
| CAP-71 | Windows branch regression CI | `unit-tested` | OK-WW legacy run `33860501048` 与 guardrail run `33860501014` 的 Windows jobs 通过；Stage C 尚待重跑 | Stage C 提交后的两仓库 Windows runner 绿色 |
| CAP-72 | stable bundle-ID arm64 internal `.app` launch | `not-implemented` | 阶段 C/H internal package |
| CAP-73 | packaged Screen Recording permission/persistence/revoke | `not-implemented` | `/Applications` identity validation |
| CAP-74 | packaged Accessibility/input/focus safety | `not-implemented` | stable identity hardware |
| CAP-75 | packaged shutdown releases input/capture | `not-implemented` | lifecycle hardware |
| CAP-76 | Developer ID + Hardened Runtime + timestamp + notarization + staple | `not-implemented` | public-release gate；凭据不入库 |

## 12. 当前声明边界

截至本记录：

- 可声明“平台安全安装/导入、capability/task declaration，以及 Stage C target/permission contract 已在无游戏环境通过单元测试”；
- macOS `SCShareableContent` 与 Quartz metadata adapter 已有 fake API mapping tests，但本机没有官方客户端，CAP-12/CAP-50 仍不得提升；
- 不可声明已经发现或捕获官方游戏窗口；
- 不可声明 persistent `SCStream`、Quartz input 或 packaged app 已实现；权限仅完成状态/请求 contract，真实授权、撤销和稳定应用身份仍未验收；
- 不可声明中键、持续按键、locked gameplay 或 relative mouse 在游戏中有效；
- 所有候选任务仍为 `experimental`，`MouseResetTask` 为 `unsupported`；
- 不支持后台；
- Windows 行为仍需远端 Windows runner 证明；
- README、UI、PR 和 release note 必须采用上述较低状态。
