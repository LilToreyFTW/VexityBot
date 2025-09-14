// TSMPoke - Advanced Pokemon GO Desktop Bot with Thunderbolt Integration
// Imports
const constants = require('./modules/const.js');
let User = require('./modules/User.js'),
    Ipc = require('./modules/Ipc.js'),
    Logger = require('./modules/Logger.js'),
    Materialize = require('./modules/Materialize.js'),
    GoogleMap = require('./modules/GoogleMap.js'),
    ProfileMenu = require('./modules/ProfileMenu.js'),
    ThunderboltIntegration = require('./modules/ThunderboltIntegration.js');

// Global vars
let user,
    googleMap,
    omap,
    forts = [],
    info_windows = [], // windows that appear when you click on fort
    ipc,
    logger,
    profileMenu,
    thunderboltIntegration;

// TSMPoke Main Initialization
$(document).ready(function() {
  // Init User 
  user = new User(userInfo.users[0]);

  // Init map
  googleMap = new GoogleMap(userInfo, user);

  // Init logger
  logger = new Logger();

  // Init Ipc
  ipc = new Ipc();
  ipc.enableLogging(logger);

  // Init Thunderbolt Integration
  thunderboltIntegration = new ThunderboltIntegration();

  // Thunderbolt Bot Control Listeners
  $('#start-bot').click(async function() {
    try {
      const mode = $('#bot-mode').val();
      await thunderboltIntegration.startBot(mode);
      logger.log('TSMPoke Thunderbolt bot started successfully!');
    } catch (error) {
      logger.log(`Failed to start bot: ${error.message}`);
    }
  });

  $('#stop-bot').click(async function() {
    try {
      await thunderboltIntegration.stopBot();
      logger.log('TSMPoke Thunderbolt bot stopped successfully!');
    } catch (error) {
      logger.log(`Failed to stop bot: ${error.message}`);
    }
  });

  $('#pause-bot').click(async function() {
    try {
      await thunderboltIntegration.pauseBot();
      logger.log('TSMPoke Thunderbolt bot paused/resumed successfully!');
    } catch (error) {
      logger.log(`Failed to pause/resume bot: ${error.message}`);
    }
  });

  // Bot mode change listener
  $('#bot-mode').change(async function() {
    const mode = $(this).val();
    try {
      await thunderboltIntegration.changeMode(mode);
      logger.log(`Changed bot mode to: ${mode}`);
    } catch (error) {
      logger.log(`Failed to change mode: ${error.message}`);
    }
  });

  // Logout listener
  $('#logout').click(function() {
    ipc.send('logout');
  });

  profileMenu = new ProfileMenu(user);

  // Materialize init
  Materialize.init();

  // Initialize Thunderbolt bot status updates
  initializeThunderboltStatus();

});

// Callback for google maps
function mapCallback() {
  googleMap.init();
}

// TSMPoke Thunderbolt Bot Status Management
function initializeThunderboltStatus() {
  // Register Thunderbolt integration callbacks
  thunderboltIntegration.onStatusUpdate(updateBotStatus);
  thunderboltIntegration.onStatsUpdate(updateBotStats);

  // Request initial status
  thunderboltIntegration.getStatus().then(updateBotStatus).catch(console.error);
  thunderboltIntegration.getStats().then(updateBotStats).catch(console.error);
}

function updateBotStatus(status) {
  const statusElement = $('#bot-indicator p');
  const statusText = status.running ? 
    `⚡ Running (${status.mode}) - ${status.current_activity}` : 
    '⏹️ Stopped';
  
  statusElement.text(statusText);
  
  // Update control buttons
  $('#start-bot').prop('disabled', status.running);
  $('#stop-bot').prop('disabled', !status.running);
  $('#pause-bot').text(status.paused ? 'Resume Bot' : 'Pause Bot');
}

function updateBotStats(stats) {
  const statsElement = $('#bot-stats p');
  const statsText = `
    🎯 Pokemon Caught: ${stats.pokemon_caught || 0}
    🎡 Pokestops Spun: ${stats.pokestops_spun || 0}
    ⚔️ Gyms Battled: ${stats.gyms_battled || 0}
    🏰 Raids Completed: ${stats.raids_completed || 0}
    ⭐ XP Gained: ${stats.xp_gained || 0}
    ✨ Shiny Caught: ${stats.shiny_caught || 0}
    💎 Perfect IV: ${stats.perfect_iv_caught || 0}
  `;
  
  statsElement.html(statsText.replace(/\n/g, '<br>'));
}