# 超级马里奥

[![Release](https://img.shields.io/github/v/release/Jayhe93-prog/easyinput-mario-canvas-game?label=release)](https://github.com/Jayhe93-prog/easyinput-mario-canvas-game/releases)
[![License](https://img.shields.io/badge/license-MIT-blue)](https://github.com/Jayhe93-prog/easyinput-mario-canvas-game/blob/main/LICENSE)
[![Zero dependencies](https://img.shields.io/badge/dependencies-0-brightgreen)](https://github.com/Jayhe93-prog/easyinput-mario-canvas-game/blob/main/super-mario.html)

一个零依赖的像素风横版闯关小游戏，整个游戏就是**一个 HTML 文件**。

- `super-mario.html` —— 游戏本体，双击用浏览器打开即可玩，Mac / Windows / 手机通用
- `Super-Mario-v1.0.0.exe` —— Windows 桌面版，双击即玩，免安装

两边玩法内容完全一致，但**进度互不相通**（各自独立存档）。

---

## 免责声明

本项目是个人学习性质的**非官方粉丝作品**，与 Nintendo 无关，未获得其授权或认可。

《超级马里奥》及相关角色名称是任天堂的商标。本项目仅用于学习与技术交流，
**禁止任何形式的商业使用**（不得销售、接入广告、上架应用商店）。

游戏内全部代码与美术素材均由本项目自行编写和绘制，未使用任天堂的任何资源文件。

本项目的源代码以 [MIT 许可](LICENSE) 开源。

---

## 快速开始

### Windows 桌面版

双击 `Super-Mario-v1.0.0.exe` 即可，不需要安装任何东西。

> 首次运行 Windows 可能弹出「已保护你的电脑 / 未知发布者」提示，
> 这是因为程序没有做代码签名，属于正常现象。
> 点「更多信息」→「仍要运行」即可，之后不再提示。

### 网页版（Mac 用户直接玩这个）

双击 `super-mario.html`，用任意现代浏览器打开（Chrome / Edge / Safari / Firefox 均可）。

也可以把它放到任意静态服务器上直接访问。

---

## 操作

| 按键 | 作用 |
| --- | --- |
| `←` `→` / `A` `D` | 左右移动 |
| `↑` / `W` / `空格` / `J` | 跳跃（**长按跳更高**，轻点是小跳） |
| `K` / `X` | 发射火球（吃到火焰花后才有） |
| `↓` / `S` | 蹲下；站在带箭头的水管上可钻进去 |
| `Enter` | 开始 / 重新开始 |
| `C` | 从已解锁的最后一关继续 |
| `R` | 重开当前关卡 |
| `P` | 暂停 |
| `M` | 打开 / 关闭声音 |
| `F11` | 全屏切换（仅桌面版），`Esc` 退出全屏 |

手机 / 平板上会自动出现屏幕虚拟按键（含 ▼ 钻水管、暂停、静音）。

---

## 游戏内容

三关递进，每关都有检查点和进度存档。

- **1-1 草原起程** —— 熟悉手感，小坑、砖块、金币
- **1-2 断桥高塔** —— 横向移动平台、断桥式深坑，炮台与飞行龟首次登场
- **1-3 终局堡垒** —— 最多的坑道与敌人，关底是 5 点血的 Boss

沿途要素：

- **金币**：每集满 150 枚自动 1UP
- **火焰花**：可发射火球，但**不会带进下一关**
- **无敌星**：短暂无敌并带拖尾
- **蘑菇**：变大，大个头可以顶碎砖块
- **弹簧 / 移动平台**：跳得更高、越过宽坑
- **金币房**：钻进带箭头的水管进入奖励关，收集完从右侧出口回到地面

---

## 存档

进度存在本地，关掉程序不会丢：

| 存储键 | 内容 |
| --- | --- |
| `mario_unlocked` | 已解锁到第几关 |
| `mario_level_bests` | 各关最高分 |
| `mario_best` | 总最高分 |
| `mario_binds` | 自定义键位 |

桌面版存在 `%APPDATA%\超级马里奥` 目录；网页版存在浏览器自己的 localStorage 里。
清理浏览器数据会清掉网页版的进度。

---

## 目录结构

```
.
├─ super-mario.html        游戏本体（单文件，零外部依赖）
├─ README.md
├─ LICENSE                 MIT 许可
├─ .gitignore
└─ desktop/                Electron 封装工程
   ├─ main.js              主进程：窗口、game:// 协议、F11 全屏、单实例
   ├─ package.json         构建配置
   ├─ make_icon.py         生成图标（纯标准库，无需 Pillow）
   └─ build/icon.ico       应用图标
```

Windows 便携版 `Super-Mario-v1.0.0.exe` 不打进仓库（70 MB，且可由源码重新构建），请到 [Releases](../../releases) 页面下载。

桌面版只是给 HTML 套了一层窗口外壳，游戏逻辑完全仍在 `super-mario.html` 里。
它用自定义协议 `game://app` 加载页面，这样存档有独立的 origin，不会和其他本地 HTML 页面混在一起。

---

## 重新打包

改了 `super-mario.html` 之后想重新生成 exe：

```bash
cd desktop
npm install
npm run build
```

产物在 `desktop/dist/`，把它复制到根目录即可。
构建直接引用根目录的 `super-mario.html`，不需要复制副本。

国内网络下载 Electron 较慢时，可以先设置镜像：

```bash
set ELECTRON_MIRROR=https://npmmirror.com/mirrors/electron/
set ELECTRON_BUILDER_BINARIES_MIRROR=https://npmmirror.com/mirrors/electron-builder-binaries/
```

> 构建配置里已固定 `signAndEditExecutable: false`。
> 原因是 electron-builder 的签名工具包内含 macOS 符号链接，在 Windows 普通权限下解压会失败；
> 个人游戏不需要代码签名，跳过即可。

---

## 自测

在网址后加 `?test=1` 打开，会自动跑 15 项内置检查（物理、关卡数据、Boss、炮台、飞行龟、存档等），
页面标题会变成 `ALLPASS` 或 `FAILn`，结果也显示在页面角落的面板里。

```
super-mario.html?test=1
```

---

## 已知说明

- exe 未做代码签名，首次运行会有 SmartScreen 提示（正常现象）
- exe 是便携版，不写注册表、不进开始菜单，删除文件即可卸载
- 桌面版和网页版存档独立，不互通
