"use strict";

/**
 * 像素闯关 · Electron 主进程
 *
 * 游戏本身仍是根目录下的单个 mario.html（无外部依赖），这里只做一层窗口外壳：
 * - 用自定义协议 game:// 提供页面，让 localStorage 拥有稳定的 origin（存档不会和别的本地页面混在一起）
 * - 去掉菜单栏，F11 全屏、Esc 退出全屏，禁掉窗口拖放与外部跳转
 */

const { app, BrowserWindow, Menu, protocol, net, shell } = require("electron");
const path = require("node:path");
const { pathToFileURL } = require("node:url");

const ENTRY = "super-mario.html";
// 打包后 super-mario.html 由 extraResources 放到 resources 目录；开发时在项目上一级
const RES_ROOT = app.isPackaged
  ? process.resourcesPath
  : path.join(__dirname, "..");

protocol.registerSchemesAsPrivileged([
  {
    scheme: "game",
    privileges: { standard: true, secure: true, supportFetchAPI: true },
  },
]);

/** 把 game://app/xxx 映射到资源目录内的文件，阻止越权读取 */
function registerGameProtocol() {
  protocol.handle("game", (req) => {
    let rel = decodeURIComponent(new URL(req.url).pathname);
    if (!rel || rel === "/") rel = "/" + ENTRY;
    const target = path.normalize(path.join(RES_ROOT, rel));
    const root = path.normalize(RES_ROOT + path.sep);
    if (!target.startsWith(root)) {
      return new Response("403 Forbidden", { status: 403 });
    }
    return net.fetch(pathToFileURL(target).toString());
  });
}

let win = null;

function createWindow() {
  win = new BrowserWindow({
    width: 1100,
    height: 700,
    minWidth: 760,
    minHeight: 480,
    backgroundColor: "#10141f",
    title: "超级马里奥",
    show: false,
    autoHideMenuBar: true,
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
      backgroundThrottling: false,
      spellcheck: false,
    },
  });

  win.loadURL("game://app/" + ENTRY);

  win.once("ready-to-show", () => {
    win.show();
    win.focus();
  });

  // 游戏只用到键盘：F11 切全屏，Esc 退出全屏
  win.webContents.on("before-input-event", (e, input) => {
    if (input.type !== "keyDown") return;
    if (input.key === "F11") {
      win.setFullScreen(!win.isFullScreen());
      e.preventDefault();
    } else if (input.key === "Escape" && win.isFullScreen()) {
      win.setFullScreen(false);
      e.preventDefault();
    }
  });

  // 页面内的跳转一律留在 game:// 协议里，外部链接交给系统浏览器
  win.webContents.on("will-navigate", (e, url) => {
    if (!url.startsWith("game://")) e.preventDefault();
  });
  win.webContents.setWindowOpenHandler(({ url }) => {
    if (/^https?:\/\//.test(url)) shell.openExternal(url);
    return { action: "deny" };
  });

  win.on("closed", () => {
    win = null;
  });
}

// 单实例：再次双击 exe 时聚焦已有窗口，而不是开第二个
if (!app.requestSingleInstanceLock()) {
  app.quit();
} else {
  app.on("second-instance", () => {
    if (win) {
      if (win.isMinimized()) win.restore();
      win.focus();
    }
  });

  app.whenReady().then(() => {
    Menu.setApplicationMenu(null);
    registerGameProtocol();
    createWindow();

    app.on("activate", () => {
      if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
  });

  app.on("window-all-closed", () => {
    if (process.platform !== "darwin") app.quit();
  });
}
