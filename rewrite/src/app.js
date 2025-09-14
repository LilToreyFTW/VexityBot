const electron = require('electron');
const dialog = require('electron').dialog;
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;
const ipcMain = electron.ipcMain;
const Menu = electron.Menu;
const path = require('path');
const os = require('os');
const fs = require('fs');
const autoUpdater = electron.autoUpdater;

// TSMPoke - Advanced Pokemon GO Desktop Bot with Thunderbolt Integration
var platform = os.platform() + '_' + os.arch();
global.appRoot = path.resolve(__dirname);
app.setVersion(require('./package.json').version);
app.setName('TSMPoke');

var mainWindow = null;
var procStarted = false;
var subpy = null;
var mainAddr;

// TSMPoke Menu Template
var template = [{
  label: "TSMPoke",
  submenu: [{
    label: "About TSMPoke",
    selector: "orderFrontStandardAboutPanel:"
  }, {
    type: "separator"
  }, {
    label: "Thunderbolt Settings",
    click: function() {
      // Open Thunderbolt configuration
      mainWindow.webContents.send('openThunderboltSettings');
    }
  }, {
    type: "separator"
  }, {
    label: "Quit",
    accelerator: "Command+Q",
    click: function() {
      app.quit();
    }
  }]
}, {
  label: "Edit",
  submenu: [{
    label: "Undo",
    accelerator: "CmdOrCtrl+Z",
    selector: "undo:"
  }, {
    label: "Redo",
    accelerator: "Shift+CmdOrCtrl+Z",
    selector: "redo:"
  }, {
    type: "separator"
  }, {
    label: "Cut",
    accelerator: "CmdOrCtrl+X",
    selector: "cut:"
  }, {
    label: "Copy",
    accelerator: "CmdOrCtrl+C",
    selector: "copy:"
  }, {
    label: "Paste",
    accelerator: "CmdOrCtrl+V",
    selector: "paste:"
  }, {
    label: "Select All",
    accelerator: "CmdOrCtrl+A",
    selector: "selectAll:"
  }]
}, {
  label: "Tools",
  submenu: [{
    label: "Refresh",
    accelerator: "CmdOrCtrl+R",
    click(item, focusedWindow) {
      if (focusedWindow) focusedWindow.reload();
    }
  }, {
    label: "Thunderbolt Bot Control",
    submenu: [{
      label: "Start Bot",
      click: function() {
        mainWindow.webContents.send('startThunderboltBot');
      }
    }, {
      label: "Stop Bot",
      click: function() {
        mainWindow.webContents.send('stopThunderboltBot');
      }
    }, {
      label: "Pause Bot",
      click: function() {
        mainWindow.webContents.send('pauseThunderboltBot');
      }
    }]
  }, {
    label: 'Toggle Developer Tools',
    accelerator: process.platform === 'darwin' ? 'Alt+Command+I' : 'Ctrl+Shift+I',
    click(item, focusedWindow) {
      if (focusedWindow)
        focusedWindow.webContents.toggleDevTools();
    }
  }]
}];

// Launch app
app.on('ready', function() {
  Menu.setApplicationMenu(Menu.buildFromTemplate(template));
  setupMainWindow();
});

// Handle app closing
app.on('window-all-closed', function() {
  if (subpy && subpy.pid) {
    // Kill TSMPoke Thunderbolt bot
    killProcess(subpy.pid);
  }
  app.quit();
});

// TSMPoke IPC listeners
// Handle logout
ipcMain.on('logout', function(event, auth, code, location, opts) {
  if (procStarted) {
    logData('Stopping TSMPoke Thunderbolt bot...');
    if (subpy && subpy.pid) {
      killProcess(subpy.pid);
    }
  }
  procStarted = false;
});

// Start TSMPoke Thunderbolt bot
ipcMain.on('startPython', function(event, auth, code, location, opts) {
  if (!procStarted) {
    logData('Starting TSMPoke Thunderbolt bot...');
    startThunderboltBot(auth, code, location, opts);
  }
  procStarted = true;
});

// Thunderbolt bot control listeners
ipcMain.on('startThunderboltBot', function(event) {
  logData('Starting Thunderbolt bot...');
  // Implementation for starting Thunderbolt bot
});

ipcMain.on('stopThunderboltBot', function(event) {
  logData('Stopping Thunderbolt bot...');
  if (subpy && subpy.pid) {
    killProcess(subpy.pid);
  }
  procStarted = false;
});

ipcMain.on('pauseThunderboltBot', function(event) {
  logData('Pausing Thunderbolt bot...');
  // Implementation for pausing Thunderbolt bot
});

// Creates TSMPoke main window and load Login page
function setupMainWindow() {

  if (!mainWindow) {
    mainWindow = new BrowserWindow({
      width: 1280,
      height: 720,
      minWidth: 700,
      minHeight: 500,
      title: 'TSMPoke - Advanced Pokemon GO Desktop Bot',
      icon: path.join(appRoot, 'assets/image/icons/tsmpoke.ico')
    });
  }
  mainWindow.loadURL('file://' + appRoot + '/pages/login.html');

  mainWindow.on('closed', function() {
    mainWindow = null;
    if (subpy && subpy.pid) {
      killProcess(subpy.pid);
    }
  });
}

// Sends log to web page
function logData(str) {
  console.log(str);
  if (mainWindow) {
    mainWindow.webContents.send('appLog', {
      'msg': `${str}`
    });
  }
}

function killProcess(pid) {
  try {
    process.kill(-pid, 'SIGINT');
    process.kill(-pid, 'SIGTERM');
  } catch (e) {
    try {
      process.kill(pid, 'SIGTERM');
    } catch (e) {}
  }
}


// Starts TSMPoke Thunderbolt bot
function startThunderboltBot(auth, code, location, opts) {

  // Load TSMPoke home page
  mainWindow.loadURL('file://' + appRoot + '/pages/home.html');

  var cmdLine = [
    './tsmpoke_cli.py',
  ];

  logData('TSMPoke bot path: ' + path.join(appRoot, 'tsmpoke'));
  logData('python ' + cmdLine.join(' '));

  var pythonCmd = 'python';
  if (os.platform() == 'win32') {
    pythonCmd = path.join(appRoot, 'pywin', 'python.exe');
  }

  // Rename config.json if needed
  try {
    //test to see if settings exist
    var setting_path = path.join(appRoot, 'tsmpoke/configs/config.json');
    fs.openSync(setting_path, 'r+');
  } catch (err) {
    fs.renameSync(path.join(appRoot, 'tsmpoke/configs/config.json.example'), setting_path);
  }

  // Rename userdata.js if needed
  try {
    //test to see if settings exist
    var user_path = path.join(appRoot, 'tsmpoke/web/config/userdata.js');
    fs.openSync(user_path, 'r+');
  } catch (err) {
    fs.renameSync(path.join(appRoot, 'tsmpoke/web/config/userdata.js.example'), user_path);
  }

  // Load user config
  var data = fs.readFileSync(path.join(appRoot, 'tsmpoke/configs/config.json'));
  var settings = JSON.parse(data);

  // Load settings
  settings.auth_service = auth;
  if (auth == 'google') {
    settings.password = opts.google_password;
    settings.username = opts.google_username;
  } else {
    settings.password = opts.ptc_password;
    settings.username = opts.ptc_username;
  }
  settings.gmapkey = opts.google_maps_api;
  if (opts.walk_speed != '') {
    settings.walk = parseInt(opts.walk_speed);
  }
  settings.location = location;

  var titleWorker = false;
  for(var i = 0 ; i < settings.tasks.length; i ++){
    if(settings.tasks[i].type == "UpdateTitleStats") {
      titleWorker = true;
    }
  }
  if(!titleWorker) {
  settings.tasks.unshift({
            "type": "UpdateTitleStats",
            "config": {
                "min_interval": 1,
                "stats": [
                    "login",
                    "uptime",
                    "km_walked",
                    "level_stats",
                    "xp_earned",
                    "xp_per_hour"
                ],
                "terminal_log": true,
                "terminal_title": false
            }
        });
  }

  let userdata_code = [
      'var userInfo = {',
      'users : ["' + settings.username + '"],',
      'userZoom : true,',
      'userFollow : true,',
      'imageExt : ".png",',
      'gMapsAPIKey : "' + settings.gmapkey + '"',
      '};'
  ];

  // Write userdata for map                
  fs.writeFileSync(path.join(appRoot, 'tsmpoke/web/config/userdata.js'), userdata_code.join('\n'), 'utf-8');

  //temporary fix for location/catchable bug in TSMPoke
  try {
    //test to see if settings exist
    var location_path = path.join(appRoot, 'tsmpoke/web/location-' + settings.username + '.json');
    fs.openSync(location_path, 'r+');
  } catch (err) {
    fs.writeFileSync(location_path, "{}");
  }
  try {
    //test to see if settings exist
    var location_path = path.join(appRoot, 'tsmpoke/web/catchable-' + settings.username + '.json');
    fs.openSync(location_path, 'r+');
  } catch (err) {
    fs.writeFileSync(location_path, "{}");
  }

  // Save user config
  fs.writeFileSync(path.join(appRoot, 'tsmpoke/configs/config.json'), JSON.stringify(settings, null, 4), 'utf-8');

  // Create TSMPoke Thunderbolt bot process
  subpy = require('child_process').spawn(pythonCmd, cmdLine, {
    cwd: path.join(appRoot, 'tsmpoke'),
    detached: true
  });

  // Send TSMPoke Thunderbolt bot log to web page
  subpy.stdout.on('data', (data) => {
    console.log(`TSMPoke: ${data}`);
    mainWindow.send('pythonLog', {
      'msg': `${data}`
    });
  });
  subpy.stderr.on('data', (data) => {
    console.log(`TSMPoke: ${data}`);
    mainWindow.send('pythonLog', {
      'msg': `${data}`
    });
    if (data.indexOf("ERROR") > -1) {
      dialog.showMessageBox({
        type: "error",
        title: "TSMPoke Error",
        message: "Error in TSMPoke Thunderbolt bot",
        detail: "" + data,
        buttons: ["I understand the error message"]
      });
    }
  });

  subpy.on('exit', () => {
    console.log(`TSMPoke Thunderbolt bot exited`);
    procStarted = false;
    setupMainWindow();
  });

}