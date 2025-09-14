// TSMPoke Thunderbolt Integration Module
// This module handles the integration between TSMPoke desktop app and Thunderbolt bot

const { ipcRenderer } = require('electron');

class ThunderboltIntegration {
    constructor() {
        this.botInstance = null;
        this.isConnected = false;
        this.statusCallbacks = [];
        this.statsCallbacks = [];
        
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // Listen for Thunderbolt bot status updates
        ipcRenderer.on('thunderboltStatus', (event, status) => {
            this.handleStatusUpdate(status);
        });

        // Listen for Thunderbolt bot statistics updates
        ipcRenderer.on('thunderboltStats', (event, stats) => {
            this.handleStatsUpdate(stats);
        });

        // Listen for Thunderbolt bot errors
        ipcRenderer.on('thunderboltError', (event, error) => {
            this.handleError(error);
        });
    }

    // Start Thunderbolt bot
    startBot(mode = 'catching') {
        return new Promise((resolve, reject) => {
            ipcRenderer.send('startThunderboltBot', { mode });
            
            // Set up one-time listener for response
            const responseHandler = (event, response) => {
                ipcRenderer.removeListener('thunderboltBotStarted', responseHandler);
                if (response.success) {
                    this.isConnected = true;
                    resolve(response);
                } else {
                    reject(new Error(response.error));
                }
            };
            
            ipcRenderer.on('thunderboltBotStarted', responseHandler);
        });
    }

    // Stop Thunderbolt bot
    stopBot() {
        return new Promise((resolve, reject) => {
            ipcRenderer.send('stopThunderboltBot');
            
            const responseHandler = (event, response) => {
                ipcRenderer.removeListener('thunderboltBotStopped', responseHandler);
                if (response.success) {
                    this.isConnected = false;
                    resolve(response);
                } else {
                    reject(new Error(response.error));
                }
            };
            
            ipcRenderer.on('thunderboltBotStopped', responseHandler);
        });
    }

    // Pause/Resume Thunderbolt bot
    pauseBot() {
        return new Promise((resolve, reject) => {
            ipcRenderer.send('pauseThunderboltBot');
            
            const responseHandler = (event, response) => {
                ipcRenderer.removeListener('thunderboltBotPaused', responseHandler);
                if (response.success) {
                    resolve(response);
                } else {
                    reject(new Error(response.error));
                }
            };
            
            ipcRenderer.on('thunderboltBotPaused', responseHandler);
        });
    }

    // Change bot mode
    changeMode(mode) {
        return new Promise((resolve, reject) => {
            ipcRenderer.send('changeBotMode', { mode });
            
            const responseHandler = (event, response) => {
                ipcRenderer.removeListener('botModeChanged', responseHandler);
                if (response.success) {
                    resolve(response);
                } else {
                    reject(new Error(response.error));
                }
            };
            
            ipcRenderer.on('botModeChanged', responseHandler);
        });
    }

    // Get current bot status
    getStatus() {
        return new Promise((resolve, reject) => {
            ipcRenderer.send('getThunderboltStatus');
            
            const responseHandler = (event, status) => {
                ipcRenderer.removeListener('thunderboltStatus', responseHandler);
                resolve(status);
            };
            
            ipcRenderer.on('thunderboltStatus', responseHandler);
        });
    }

    // Get current bot statistics
    getStats() {
        return new Promise((resolve, reject) => {
            ipcRenderer.send('getThunderboltStats');
            
            const responseHandler = (event, stats) => {
                ipcRenderer.removeListener('thunderboltStats', responseHandler);
                resolve(stats);
            };
            
            ipcRenderer.on('thunderboltStats', responseHandler);
        });
    }

    // Update bot configuration
    updateConfig(config) {
        return new Promise((resolve, reject) => {
            ipcRenderer.send('updateThunderboltConfig', config);
            
            const responseHandler = (event, response) => {
                ipcRenderer.removeListener('thunderboltConfigUpdated', responseHandler);
                if (response.success) {
                    resolve(response);
                } else {
                    reject(new Error(response.error));
                }
            };
            
            ipcRenderer.on('thunderboltConfigUpdated', responseHandler);
        });
    }

    // Register status update callback
    onStatusUpdate(callback) {
        this.statusCallbacks.push(callback);
    }

    // Register statistics update callback
    onStatsUpdate(callback) {
        this.statsCallbacks.push(callback);
    }

    // Handle status updates
    handleStatusUpdate(status) {
        this.statusCallbacks.forEach(callback => {
            try {
                callback(status);
            } catch (error) {
                console.error('Error in status callback:', error);
            }
        });
    }

    // Handle statistics updates
    handleStatsUpdate(stats) {
        this.statsCallbacks.forEach(callback => {
            try {
                callback(stats);
            } catch (error) {
                console.error('Error in stats callback:', error);
            }
        });
    }

    // Handle errors
    handleError(error) {
        console.error('Thunderbolt bot error:', error);
        // Notify all status callbacks about the error
        this.statusCallbacks.forEach(callback => {
            try {
                callback({ error: error, running: false });
            } catch (err) {
                console.error('Error in error callback:', err);
            }
        });
    }

    // Export bot statistics
    exportStats(filename) {
        return new Promise((resolve, reject) => {
            ipcRenderer.send('exportThunderboltStats', { filename });
            
            const responseHandler = (event, response) => {
                ipcRenderer.removeListener('thunderboltStatsExported', responseHandler);
                if (response.success) {
                    resolve(response);
                } else {
                    reject(new Error(response.error));
                }
            };
            
            ipcRenderer.on('thunderboltStatsExported', responseHandler);
        });
    }

    // Reset bot statistics
    resetStats() {
        return new Promise((resolve, reject) => {
            ipcRenderer.send('resetThunderboltStats');
            
            const responseHandler = (event, response) => {
                ipcRenderer.removeListener('thunderboltStatsReset', responseHandler);
                if (response.success) {
                    resolve(response);
                } else {
                    reject(new Error(response.error));
                }
            };
            
            ipcRenderer.on('thunderboltStatsReset', responseHandler);
        });
    }

    // Get available bot modes
    getAvailableModes() {
        return [
            'catching',
            'raiding', 
            'battling',
            'exploring',
            'idle'
        ];
    }

    // Check if bot is connected
    isBotConnected() {
        return this.isConnected;
    }

    // Get connection status
    getConnectionStatus() {
        return {
            connected: this.isConnected,
            botInstance: this.botInstance
        };
    }
}

module.exports = ThunderboltIntegration;
