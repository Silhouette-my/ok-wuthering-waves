# OK-WW macOS 前台模式移植——工程约束

状态：**macOS 前台模式 MVP 的规范性约束**

目标：Apple Silicon、macOS 13+、Python 3.12 arm64、官方《鸣潮》Mac 客户端

本文档规定 OK-WW 首个原生 macOS 版本的硬性工程边界。文中的“必须”“不得”“仅允许”“发布阻断项”均为强制要求，不得通过兼容垫片、隐藏回退、空实现或宽泛异常处理绕过。

## 0. 规范层级与变更控制

- 本文件是 macOS 前台 MVP 的规范性产品与工程合同。
- `docs/development/macos-foreground-port-plan.md` 只描述实施顺序和证据，不得削弱本文件。
- 仓库 `AGENTS.md`、嵌套说明和适用 skills 同时生效；更具体规则可以收紧实现，但不得放宽“仅前台、仅公开 API、失败关闭、Windows 不回归”四项核心边界。
- 发现规则冲突时，必须在修改运行时代码前解决。安全、仓库职责和兼容性优先于实现便利。
- 有意偏离必须在 `docs/development/decisions/` 提交 ADR，至少记录原因、备选方案、安全/权限影响、Windows 影响、测试与硬件验收、迁移及回滚。
- 代码注释、临时 issue、聊天记录或 PR 讨论不能代替 ADR。

## 1. 开发与集成模型

### 1.1 长期集成分支

- `ok-script` 与 `ok-wuthering-waves` 均使用 `feature/macos-foreground-mvp` 或明确对应的长期集成分支。
- 分支从记录的 `upstream/master` SHA 创建。
- `origin` 指向 contributor fork；`upstream` 指向 `ok-oldking` canonical repository。
- 开发提交按逻辑拆分、可审查、可回滚、可二分，尽量保持可构建。
- 不得为每个阶段创建准备合并的基础设施 PR、占位 PR 或未完成能力 PR。
- 不得把不完整 Mac 支持合入默认分支来“解锁后续工作”。
- 定期同步 upstream，及早暴露冲突。
- 开发分支只推送到 contributor fork；不得直接推送或强制更新 canonical 默认分支。

### 1.2 跨仓库依赖

开发期使用 sibling editable install：

```bash
./.venv/bin/python -m pip install -e "../ok-script[ocr,qt]"
./.venv/bin/python -m pip install -e ".[dev]"
```

不得用 submodule、subtree、复制包或 vendoring 连接两个仓库。

最终 OK-WW 变更不得依赖：

- 可变分支 URL；
- 临时或未发布本地 wheel；
- 未提交补丁或文件；
- 开发者私有目录结构；
- 未记录的环境级 monkey patch。

最终交付是两个相互关联的完整 MVP PR：

1. `ok-script` PR：可复用的平台能力；
2. `ok-wuthering-waves` PR：游戏集成，并使用维护者接受的不可变框架版本或提交。

### 1.3 阶段 0 启动门槛

阶段 0 只负责工作区、仓库身份、分支、参考环境、规范、忽略规则和基线证据。不得开始窗口发现、ScreenCaptureKit、Quartz 或任务适配运行时代码。

运行时代码开始前必须完成并记录：

- 两个可写 contributor fork；
- 两个独立 sibling checkout；
- 已验证的 `origin`/`upstream`；
- 两个集成分支和起始 upstream SHA；
- Apple Silicon、受支持 macOS、Xcode/Clang、Git、Python 3.12 arm64；
- OK-WW 本地 `.venv`；
- 两个实际分支中的约束文件；
- 初始 install/import/test 命令与结果；
- `.gitignore` 对本地环境、构建物、凭据、TCC 材料和私密验收材料的覆盖；
- bootstrap 提交已推送到 contributor fork，但未开阶段性 PR；
- 提交后两个工作树干净。

初始命令可以因现有 Windows-only 依赖图而失败，但必须原样记录并关联后续阶段。不得用 `--no-deps`、临时 wheel、分支 URL 或全局 Python 环境掩盖失败。

### 1.4 仓库与证据卫生

不得提交：

- 本地绝对路径；
- token、私钥、Developer ID、公证凭据或敏感签名日志；
- TCC 数据库或权限绕过材料；
- 个人账户截图、未脱敏日志和私密硬件验收数据；
- `.venv`、`.app`、`.dmg`、`.pkg`、构建缓存或生成目录。

采用外部分支或历史 PR 代码时必须记录来源、作者归属和许可证兼容性，不得整段照搬未经审查的实验实现。

## 2. 产品定义与支持基线

首个 Mac 版本是官方《鸣潮》Mac 客户端的**原生前台自动化客户端**。

支持流程：

1. 用户启动官方游戏；
2. OK-WW 发现或让用户选择游戏应用和窗口；
3. 使用 ScreenCaptureKit 捕获选定窗口；
4. 任务开始和每次输入前确认游戏是系统最前台应用；
5. 使用 Quartz 发送键盘和鼠标；
6. 焦点、目标、权限、截图或任务状态失效时立即阻断输入并释放保持状态。

必须支持的基线：

- Apple Silicon arm64；
- macOS 13.0 或更高；
- Python 3.12 arm64 参考环境；
- 现有 PySide6/Qt GUI 技术栈；
- 官方《鸣潮》Mac 客户端；
- 窗口化或无边框窗口化优先；
- 现有 16:9 坐标模型；
- 首个硬件验收分辨率 1920×1080；
- 初始 CPU 推理。

明确不支持：

- Intel Mac 和正式 macOS 12 承诺；
- 最小化、后台或其他 Mission Control Space 控制；
- BetterDisplay、虚拟显示器或私有 `CGVirtualDisplay`；
- `CGEvent.postToPid` 后台机制；
- 游戏注入、dylib 注入、swizzling、Metal hook 或反作弊绕过；
- Android 模拟器、云游戏或远程串流替代原生客户端；
- 任意宽高比；
- Mac App Store 首发分发。

## 3. API 政策

仅允许公开 Apple API：

- ScreenCaptureKit；
- AppKit；
- Core Graphics / Quartz；
- 必要时的 ApplicationServices Accessibility API；
- Foundation / CoreFoundation。

禁止：

- 私有 WindowServer SPI；
- 私有 `CGVirtualDisplay*`；
- 注入、进程内 hook、method swizzling；
- 直接修改游戏进程代码、数据或运行状态；
- 任何用于无焦点、隐藏或后台控制的未公开接口；
- 自动修改 TCC 或以 root 绕过权限。

## 4. 仓库职责边界

### 4.1 `ok-script` 负责

- 平台路由；
- 平台中立桌面窗口目标；
- Windows 兼容适配；
- macOS 应用/窗口发现；
- ScreenCaptureKit 持久截图；
- Quartz 前台输入；
- 前台守卫；
- 光标服务；
- 屏幕捕获和辅助功能权限服务；
- 坐标转换与几何代次；
- 持续输入状态和关闭生命周期；
- 平台依赖与延迟导入。

### 4.2 `ok-wuthering-waves` 负责

- 经真实安装验证的游戏 app/window 匹配提示；
- 游戏热键选择；
- 任务兼容性和能力声明；
- 必要且有证据的 `assets/macos` 覆盖；
- 移除两处直接 `win32api` 使用并消费框架 CursorService；
- Mac CPU 推理配置；
- OK-WW 用户文档、权限指导和故障排查。

### 4.3 禁止本仓库自建 OS 兼容层

- 不得新增 `src.compat.win32api` 一类保持 Win32 外形、在 Darwin 内改调 Quartz 的垫片。
- task、combat、scene 不得直接导入 Win32、AppKit、Quartz、ScreenCaptureKit。
- 不得复制 `ok-script` 后端到 OK-WW。
- Windows 专属非核心功能可在 Mac P0 显式禁用，但状态必须可观察、可测试；不得空实现、吞异常或伪造成功。

## 5. 依赖与平台导入

`pyproject.toml` 是依赖事实来源。

- `pywin32`、`pydirectinput`、`pycaw`、适用的 `comtypes` 以及仅 Windows 可用的 `mouse` 必须使用环境标记或 Windows extra。
- macOS 只声明最小 PyObjC wrapper，例如 Cocoa、Quartz、ScreenCaptureKit、ApplicationServices。
- 生成锁文件必须由生成工具重建；不得手改版本集合。
- 单一锁无法跨平台复现时，允许独立 macOS arm64 锁。
- Windows 生成的 `requirements.txt` 不是 Mac 安装清单。

共享模块顶层不得无条件导入：

- `win32api`、`win32con`、`win32gui`、`win32process`、`winreg`；
- `ctypes.windll` 或 `ctypes.WinDLL` 实现；
- AppKit、Quartz、ScreenCaptureKit 或 PyObjC 平台实现。

必须先选择平台/provider，再延迟导入实现。不得散布宽泛 `try/except ImportError` 掩盖错误边界。

macOS 冒烟测试必须能导入 `ok`、DeviceManager、executor、共享设备抽象和全部 OK-WW task，而不加载 Win32-only 模块。

## 6. 桌面窗口目标

不得把 `HwndWindow` 扩充成仍以 HWND 字段为中心的伪跨平台对象。

平台中立 target 至少表达：

- 当前运行实例中的进程标识；
- 可选 bundle/application 标识；
- 平台窗口标识；
- 标题/显示名；
- 窗口、内容区和截图几何；
- 存活和前台状态；
- 激活请求；
- 窗口或进程重建后的刷新/重绑。

Windows 以最小改动适配现有 HWND；macOS 可绑定 `NSRunningApplication`、`SCWindow`、`CGWindowID`。任务不得判断底层标识类型。

不得在观察真实安装客户端前把猜测 bundle ID 写成唯一条件，也不得只靠标题匹配。多候选时允许显式选择，并持久化稳定提示而不是旧 PID/window ID。

## 7. ScreenCaptureKit 截图契约

### 7.1 生产路径

- 连续自动化必须使用持久化 `SCStream`。
- 首选 `SCContentFilter(desktopIndependentWindow:)`。
- `SCScreenshotManager`、主显示器截图和全桌面裁切仅供显式诊断或测试夹具，不得进入 task executor，也不得成为自动回退。
- `showsCursor = false`。
- 回调只做必要的帧接收、转换/所有权处理和最新帧发布，不运行 OCR、模板、task 或 Qt 控件更新。

### 7.2 输出

每个成功帧必须：

- `numpy.ndarray`；
- `dtype == uint8`；
- `shape == (height, width, 3)`；
- BGR；
- 仅游戏内容区；
- 不含光标、标题栏、阴影、边框或其他桌面内容。

### 7.3 队列与所有权

- 只保留最新完整帧；
- 缓冲有固定上限；
- 可丢弃旧帧，禁止无界队列；
- 消费期间底层缓冲不得异步覆盖；
- 每个帧绑定一个不可变几何/截图代次。

### 7.4 重绑与失败

必须检测、恢复或进入明确终止状态：

- 游戏退出；
- 窗口重建或切换全屏；
- 尺寸变化；
- 显示器/缩放变化；
- 权限撤销；
- `SCStream` 失败。

重试需退避和终止条件。重绑开始后立即使旧帧和旧坐标失效，新代次建立前不得继续输入。

## 8. 坐标模型

任务和识别统一使用**截图帧内部物理像素坐标**。平台后端负责转换到 AppKit 逻辑点、Core Graphics 全局坐标或 Qt 坐标。

- task 不得混用 ScreenCaptureKit 像素、AppKit 点、CG 全局坐标、Qt logical coordinate 和游戏内部渲染分辨率。
- 一次输入只能使用当前有效几何代次。
- 测试覆盖 scale 1.0、2.0、观察到的非整数缩放、原点偏移、resize 和代次替换。
- 不得假设 Retina 恒为 2.0。

## 9. Quartz 前台输入契约

生产后端使用 Core Graphics Quartz，至少支持：

- `send_key`、`send_key_down`、`send_key_up`；
- 左/右/中键 down、up、click；
- 绝对移动；
- task 需要时的滚轮；
- 可控制游戏镜头的相对/delta 移动；
- `release_all()`。

每个普通事件或短原子批次前必须：

1. 验证目标仍存在；
2. 验证绑定进程仍有效；
3. 验证目标是系统最前台应用；
4. 通过后才发送。

激活 API 返回成功不代表获得焦点。必须观察到 frontmost 状态，并在后续每次输入前继续检查。

目标不在前台时：

1. 不发送待发送普通事件；
2. 阻断后续输入；
3. 调用 `release_all()`；
4. task 进入焦点丢失暂停/停止；
5. 显示明确原因；
6. 只有用户显式操作才能恢复。

不得使用 `CGEvent.postToPid` 或向当前任意前台 app 发送普通输入作为回退。

## 10. 持续输入、并发与关闭

- 显式跟踪程序保持的键和鼠标按钮。
- `release_all()` 幂等，目标消失后仍安全。
- 单个 release 失败时继续释放其余状态，最后清空内部集合。
- task 长按操作使用 `try/finally`。
- `send_key_down`、`send_key_up`、`release_all` 不得为空实现或只记录日志。
- 普通输入、焦点失效、stop 和 release 必须经过同一个线程安全边界。
- 目标失效时先关闭新输入闸门，再释放保持状态。
- 失效后的 release 路径只允许发送对应 key-up/button-up，不得生成新的 down、click、movement、scroll 或 text。
- 原子批次不得跨越 sleep、frame wait、activate、permission prompt 或其他可能改变焦点的操作。
- 以下路径必须 release：焦点丢失、任务取消、executor stop、致命截图失败、权限撤销、设备切换、游戏退出、应用退出。
- 关闭顺序：阻断新输入 → release → 停止 stream/worker → 销毁 Qt/Python 对象。

## 11. 相对鼠标硬件门槛

未经官方 Mac 游戏实测，不得把 relative/delta 鼠标标记为支持。

至少验证：

- X/Y 镜头转动；
- 连续 delta 不会非预期把光标推离区域；
- 镜头可与 W/A/S/D 长按和攻击同时工作；
- 中键行为正确；
- 停止后光标和输入状态合理；
- 无持续旋转、卡键或卡按钮。

失败时只能声明菜单/基础任务可用，不能声明完整战斗、跑图或路线任务。

## 12. 权限

必须显式处理：

- Screen Recording / screen capture；
- Accessibility synthetic control。

使用系统支持的 preflight/request API。缺失权限时：

- 显示明确状态和设置路径；
- 阻止对应截图或输入能力；
- 不在紧密循环重复请求；
- 不修改 TCC，不请求 root 绕过。

Terminal/Python 权限只是开发证据。最终验收必须使用稳定 bundle identifier 的打包 `.app`。

## 13. 视觉、分辨率和推理

- 保持现有 16:9 task 坐标模型。
- 首个硬件验收为 1920×1080。
- 后续目标：1280×720、1600×900、2560×1440。
- 不承诺任意比例。
- 先标准化内容区、分辨率、BGR，再原样运行现有 template/OCR/color/detection。
- 只有同分辨率下可重复 Mac 差异且通用调整会损害 Windows 时，才增加 `assets/macos` 覆盖并回退通用资源。
- 不得预复制完整 assets tree。
- 初始使用 CPU 推理；`use_npu` 在 macOS 关闭或安全忽略。
- 必须验证 OCR/model wheel 和 native library 的 arm64 兼容性；正确性优先于优化。

## 14. UI、进程、线程和性能

Mac P0 可显式禁用：Win32 GDI overlay、Windows tray、Windows thumbnail、volume/HDR/Night Light、Windows launcher/updater。装饰性功能不得阻塞核心自动化。

- 继续复用可跨平台的 Qt GUI，不无必要重写。
- Windows named mutex、admin/elevation、Explorer helper 不得在 Darwin 执行；Mac MVP 不要求 root。
- ScreenCaptureKit callback 不直接修改 Qt。
- Python/Qt 销毁前关闭 stream/worker。
- `close()` 可重复安全调用。
- 参考 1920×1080 下 SCStream 目标配置 30 FPS；框架消费最新帧，不堆积队列。
- 稳态低于 20 FPS 时分析原因。
- 调试记录 FPS、frame age、drop/rebind 状态。

## 15. 测试与 CI

平台层每次变更都必须保持 Windows 行为。

自动化测试至少覆盖：

- Windows 和 Darwin provider selection；
- Darwin import 不加载 Win32；
- Windows import 不要求 PyObjC；
- desktop target 生命周期/rebind；
- BGRA/BGR、stride/padding、帧所有权和 bounded publication；
- geometry 和 Retina 转换；
- held state、幂等 release、单点失败继续释放；
- focus race 和失效后无普通输入；
- permission state；
- repeated close/shutdown order；
- OK-WW app、executor、全部 task 导入。

CI 不得要求安装游戏。新增 macOS Python 3.12 job 负责依赖安装、导入和无游戏测试；现有 Windows CI 保持通过。

真实游戏属于人工硬件验收，不是 GitHub Actions 前置条件。

## 16. 打包与分发

源码/dev bring-up 优先，不被当前 Windows PyAppify installer 阻塞。

源码稳定后优先评估 `pyside6-deploy` / Nuitka，生成自包含 `.app`。最终 PR 前必须用稳定 bundle identifier 的内部包验证：

- arm64 native library；
- Qt platform plugin；
- OpenCV、OCR/inference、PyObjC；
- assets/i18n；
- Screen Recording 与 Accessibility；
- shutdown release/stream close。

公开直接分发必须使用 Developer ID Application、Hardened Runtime、安全时间戳、Apple notarization、staple，并在干净环境验证。不得把 unsigned/ad-hoc 包当作正常公开产物，也不得提交发布凭据。

## 17. Windows 回归边界

`ok-script` 必须保持：

- WGC/BitBlt 选择；
- 当前 Windows 输入；
- HWND 选择；
- 现有 task API 与配置键；
- ADB/browser 行为。

优先用最小适配包装现有 Windows 实现，不为视觉对称大规模重写已工作代码。

## 18. 真实硬件验收矩阵

### 应用/窗口

- [ ] 找到进程和正确窗口；
- [ ] 显示 PID、bundle ID、window ID、标题、内容几何；
- [ ] 激活后观察到 frontmost；
- [ ] Command-Tab 状态变化；
- [ ] 检测退出；
- [ ] 处理或明确报告窗口重建和尺寸变化。

### 截图

- [ ] 1920×1080 连续 BGR `uint8`；
- [ ] 不含光标、标题栏、边框；
- [ ] 颜色正确；
- [ ] 连续场景切换稳定；
- [ ] 至少 1000 帧无 stall/明显泄漏/队列增长；
- [ ] resize/rebind 状态正确；
- [ ] FPS/frame age 可观测。

### 键盘

- [ ] W/A/S/D tap、hold、release；
- [ ] E/Q/R/F/T；
- [ ] Space、Shift、Tab；
- [ ] 实际使用时的 F2、B、1/2/3。

### 鼠标

- [ ] 左/右/中键；
- [ ] hold/release；
- [ ] 绝对坐标；
- [ ] relative X/Y；
- [ ] movement + attack + camera；
- [ ] stop 后状态合理。

### 安全

- [ ] hold W 时 Command-Tab；
- [ ] hold modifier/button 时切换应用；
- [ ] 点击其他应用；
- [ ] 撤销 Screen Recording；
- [ ] 撤销 Accessibility；
- [ ] 持续输入时退出游戏；
- [ ] 持续输入时关闭 OK-WW；
- [ ] 上述场景无字符、点击或普通输入泄漏到错误应用。

## 19. 能力状态与声明

只使用：

1. `not-implemented`；
2. `unit-tested`；
3. `hardware-validated`；
4. `packaged-app-validated`。

README、UI、PR 和 release note 不得宣称高于证据的状态。每条证据记录 commit SHA、命令或人工步骤、Mac/系统/游戏版本、分辨率、窗口模式和结果。回归会重新打开对应 gate。

## 20. 最终完成定义

最终 MVP PR 前必须满足：

- arm64 macOS 安装和导入不加载 Win32；
- 能发现/选择官方游戏；
- ScreenCaptureKit 提供标准帧；
- 核心 template/OCR 在真实 Mac 图像通过；
- Quartz keyboard/mouse 控制真实游戏；
- relative camera 硬件通过；
- focus loss 阻止新输入并 release；
- 至少一个简单非战斗 task 端到端通过；
- 声称战斗支持前至少一个代表战斗流程通过；
- Windows tests 通过；
- packaged `.app` 权限行为通过；
- 文档、限制、故障排查和回滚完整。

公开发布前再完成签名、公证和 Gatekeeper 验证。

## 21. 禁止的捷径

不得：

- 全桌面截图后猜坐标裁切作为生产后端；
- `pyautogui`/`pynput` 代替平台架构；
- 其他应用前台时发送普通输入；
- 猜测并硬编码唯一 bundle ID 或恒定标题；
- 假设 Retina 恒为 2.0；
- 静默忽略权限、down/up/release 或 capture 失败；
- relative camera 失败后仍声称战斗/路线支持；
- task 直接导入 OS API；
- OK-WW 私建兼容 shim 或复制后端；
- 使用私有 API、BetterDisplay、虚拟显示、注入或 hook；
- 使用 `CGEvent.postToPid` 或任意前台输入回退；
- 让旧帧/旧几何在重绑期间继续驱动输入。
