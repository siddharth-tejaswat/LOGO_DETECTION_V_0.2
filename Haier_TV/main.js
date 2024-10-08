import path from "path";
import { app, BrowserWindow, net } from "electron";
import isDev from "electron-is-dev";

function createWindow() {
  // Create the browser window.
  const win = new BrowserWindow({
    width: 1280,
    height: 720,
    autoHideMenuBar: true,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false, // Ensure context isolation is disabled for nodeIntegration
    },
  });

  // Load the app (use localhost for dev, built files for prod)
  win.loadURL(
    isDev
      ? "http://localhost:5173"
      : `file://${path.join(__dirname, "index.html")}`
  );

  // Suppress Autofill related console errors
  win.webContents.on("console-message", (event, level, message) => {
    if (message.includes("Autofill")) {
      event.preventDefault(); // Suppress Autofill related errors
    }
  });

   //Open DevTools if in development
   //if (isDev) {
    // win.webContents.openDevTools({ mode: "detach" });
  // }
}

// Called when Electron has finished initializing and is ready to create browser windows.
app.whenReady().then(createWindow);

// Quit when all windows are closed (except on macOS)
app.on("window-all-closed", () => {
  // Send request to backend when window is closed
  const request = net.request({
    method: "GET",
    protocol: "http:",
    hostname: "10.10.14.63",
    port: 5001,
    path: "/close",
  });

  request.on("finish", () => {
    if (process.platform !== "darwin") {
      app.quit();
    }
  });

  request.setHeader("Content-Type", "application/json");
  request.end();
});

// On macOS, recreate the window when the app is re-activated
app.on("activate", () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});
