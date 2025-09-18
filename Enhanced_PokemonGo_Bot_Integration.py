# -*- coding: utf-8 -*-
"""
Enhanced Pokemon GO Bot Integration with VexityBot GUI
Integrates the enhanced pgoapi-based bot with the existing Thunderbolt GUI
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
import json
import os
import sys
from typing import Dict, List, Optional, Any

# ADDED: Add pgoapi to Python path
pgoapi_path = os.path.join(os.getcwd(), 'pgoapi')
if pgoapi_path not in sys.path:
    sys.path.insert(0, pgoapi_path)

# Import the enhanced bot
from Enhanced_PokemonGo_Bot import EnhancedPokemonGoBot

class EnhancedPokemonGoBotGUI:
    """Enhanced Pokemon GO Bot GUI Integration"""
    
    def __init__(self, parent_frame=None):
        self.parent_frame = parent_frame
        self.bot = None
        self.gui_initialized = False
        
        # GUI variables
        self.status_var = tk.StringVar(value="Bot not initialized")
        self.mode_var = tk.StringVar(value="idle")
        self.location_var = tk.StringVar(value="40.7589, -73.9851")
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.auth_provider_var = tk.StringVar(value="ptc")
        
        # Statistics variables
        self.stats_vars = {
            'pokemon_caught': tk.StringVar(value="0"),
            'pokestops_spun': tk.StringVar(value="0"),
            'gyms_battled': tk.StringVar(value="0"),
            'xp_gained': tk.StringVar(value="0"),
            'session_duration': tk.StringVar(value="00:00:00")
        }
        
        self._create_gui()
    
    def _create_gui(self):
        """Create the enhanced bot GUI"""
        if not self.parent_frame:
            # Create main window if no parent frame
            self.root = tk.Tk()
            self.root.title("Enhanced Pokemon GO Bot - pgoapi Integration")
            self.root.geometry("800x600")
            self.parent_frame = self.root
        
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(self.parent_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self._create_control_tab()
        self._create_settings_tab()
        self._create_statistics_tab()
        self._create_logs_tab()
        
        self.gui_initialized = True
    
    def _create_control_tab(self):
        """Create the main control tab"""
        control_frame = ttk.Frame(self.notebook)
        self.notebook.add(control_frame, text="🎮 Control")
        
        # Bot status section
        status_frame = ttk.LabelFrame(control_frame, text="Bot Status", padding=10)
        status_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(status_frame, text="Status:").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(status_frame, textvariable=self.status_var, foreground="blue").grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(status_frame, text="Mode:").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(status_frame, textvariable=self.mode_var, foreground="green").grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
        
        # Control buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.start_button = ttk.Button(button_frame, text="🚀 Start Bot", command=self.start_bot)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.pause_button = ttk.Button(button_frame, text="⏸️ Pause", command=self.pause_bot, state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT, padx=5)
        
        self.resume_button = ttk.Button(button_frame, text="▶️ Resume", command=self.resume_bot, state=tk.DISABLED)
        self.resume_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="⏹️ Stop", command=self.stop_bot, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # Mode selection
        mode_frame = ttk.LabelFrame(control_frame, text="Bot Mode", padding=10)
        mode_frame.pack(fill=tk.X, padx=5, pady=5)
        
        modes = ["idle", "catching", "raiding", "battling", "exploring", "farming", "hunting", "evolving", "powering_up", "mega_evolving"]
        self.mode_combo = ttk.Combobox(mode_frame, values=modes, textvariable=self.mode_var, state="readonly")
        self.mode_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(mode_frame, text="Set Mode", command=self.set_mode).pack(side=tk.LEFT, padx=5)
        
        # Quick stats
        stats_frame = ttk.LabelFrame(control_frame, text="Quick Stats", padding=10)
        stats_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(stats_frame, text="Pokemon Caught:").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(stats_frame, textvariable=self.stats_vars['pokemon_caught']).grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(stats_frame, text="Pokestops Spun:").grid(row=0, column=2, sticky=tk.W, padx=(20, 0))
        ttk.Label(stats_frame, textvariable=self.stats_vars['pokestops_spun']).grid(row=0, column=3, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(stats_frame, text="Session Time:").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(stats_frame, textvariable=self.stats_vars['session_duration']).grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
    
    def _create_settings_tab(self):
        """Create the settings tab"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="⚙️ Settings")
        
        # Authentication section
        auth_frame = ttk.LabelFrame(settings_frame, text="Authentication", padding=10)
        auth_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(auth_frame, text="Provider:").grid(row=0, column=0, sticky=tk.W)
        provider_combo = ttk.Combobox(auth_frame, values=["ptc", "google"], textvariable=self.auth_provider_var, state="readonly")
        provider_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(auth_frame, text="Username:").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(auth_frame, textvariable=self.username_var, width=30).grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(auth_frame, text="Password:").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(auth_frame, textvariable=self.password_var, show="*", width=30).grid(row=2, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Button(auth_frame, text="Set Credentials", command=self.set_credentials).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Location section
        location_frame = ttk.LabelFrame(settings_frame, text="Location", padding=10)
        location_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(location_frame, text="Coordinates (lat, lng):").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(location_frame, textvariable=self.location_var, width=30).grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Button(location_frame, text="Set Location", command=self.set_location).grid(row=1, column=0, columnspan=2, pady=10)
        
        # Bot settings section
        bot_settings_frame = ttk.LabelFrame(settings_frame, text="Bot Settings", padding=10)
        bot_settings_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.catch_pokemon_var = tk.BooleanVar(value=True)
        self.spin_pokestops_var = tk.BooleanVar(value=True)
        self.battle_gyms_var = tk.BooleanVar(value=False)
        self.human_like_delays_var = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(bot_settings_frame, text="Catch Pokemon", variable=self.catch_pokemon_var).grid(row=0, column=0, sticky=tk.W)
        ttk.Checkbutton(bot_settings_frame, text="Spin Pokestops", variable=self.spin_pokestops_var).grid(row=0, column=1, sticky=tk.W)
        ttk.Checkbutton(bot_settings_frame, text="Battle Gyms", variable=self.battle_gyms_var).grid(row=1, column=0, sticky=tk.W)
        ttk.Checkbutton(bot_settings_frame, text="Human-like Delays", variable=self.human_like_delays_var).grid(row=1, column=1, sticky=tk.W)
        
        ttk.Button(bot_settings_frame, text="Apply Settings", command=self.apply_settings).grid(row=2, column=0, columnspan=2, pady=10)
    
    def _create_statistics_tab(self):
        """Create the statistics tab"""
        stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(stats_frame, text="📊 Statistics")
        
        # Create statistics display
        stats_text = scrolledtext.ScrolledText(stats_frame, height=20, width=80)
        stats_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.stats_text = stats_text
        
        # Refresh button
        ttk.Button(stats_frame, text="🔄 Refresh Stats", command=self.refresh_statistics).pack(pady=5)
    
    def _create_logs_tab(self):
        """Create the logs tab"""
        logs_frame = ttk.Frame(self.notebook)
        self.notebook.add(logs_frame, text="📝 Logs")
        
        # Create logs display
        logs_text = scrolledtext.ScrolledText(logs_frame, height=20, width=80)
        logs_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.logs_text = logs_text
        
        # Clear button
        ttk.Button(logs_frame, text="🗑️ Clear Logs", command=self.clear_logs).pack(pady=5)
    
    def start_bot(self):
        """Start the enhanced bot"""
        try:
            if not self.bot:
                # Create bot instance
                self.bot = EnhancedPokemonGoBot(gui_callback=self._bot_callback)
                
                # Set credentials if provided
                if self.username_var.get() and self.password_var.get():
                    self.bot.set_credentials(
                        self.username_var.get(),
                        self.password_var.get(),
                        self.auth_provider_var.get()
                    )
                
                # Set location if provided
                if self.location_var.get():
                    try:
                        coords = self.location_var.get().split(',')
                        if len(coords) >= 2:
                            lat = float(coords[0].strip())
                            lng = float(coords[1].strip())
                            alt = float(coords[2].strip()) if len(coords) > 2 else 10
                            self.bot.set_location(lat, lng, alt)
                    except ValueError:
                        messagebox.showerror("Error", "Invalid location format. Use: lat, lng, alt")
                        return
            
            # Start bot
            if self.bot.start():
                self.status_var.set("Bot running")
                self.start_button.config(state=tk.DISABLED)
                self.pause_button.config(state=tk.NORMAL)
                self.stop_button.config(state=tk.NORMAL)
                self._log_message("✅ Bot started successfully")
            else:
                messagebox.showerror("Error", "Failed to start bot")
                self._log_message("❌ Failed to start bot")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error starting bot: {e}")
            self._log_message(f"❌ Error starting bot: {e}")
    
    def pause_bot(self):
        """Pause the bot"""
        if self.bot:
            self.bot.pause()
            self.status_var.set("Bot paused")
            self.pause_button.config(state=tk.DISABLED)
            self.resume_button.config(state=tk.NORMAL)
            self._log_message("⏸️ Bot paused")
    
    def resume_bot(self):
        """Resume the bot"""
        if self.bot:
            self.bot.resume()
            self.status_var.set("Bot running")
            self.resume_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            self._log_message("▶️ Bot resumed")
    
    def stop_bot(self):
        """Stop the bot"""
        if self.bot:
            self.bot.stop()
            self.status_var.set("Bot stopped")
            self.start_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED)
            self.resume_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.DISABLED)
            self._log_message("⏹️ Bot stopped")
    
    def set_mode(self):
        """Set bot mode"""
        if self.bot:
            mode = self.mode_var.get()
            self.bot.set_mode(mode)
            self._log_message(f"🎯 Mode changed to: {mode}")
    
    def set_credentials(self):
        """Set authentication credentials"""
        username = self.username_var.get()
        password = self.password_var.get()
        provider = self.auth_provider_var.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return
        
        if self.bot:
            self.bot.set_credentials(username, password, provider)
            self._log_message(f"🔐 Credentials set for {provider} account: {username}")
        else:
            self._log_message(f"🔐 Credentials will be set when bot starts")
    
    def set_location(self):
        """Set bot location"""
        location_str = self.location_var.get()
        
        try:
            coords = location_str.split(',')
            if len(coords) >= 2:
                lat = float(coords[0].strip())
                lng = float(coords[1].strip())
                alt = float(coords[2].strip()) if len(coords) > 2 else 10
                
                if self.bot:
                    self.bot.set_location(lat, lng, alt)
                    self._log_message(f"📍 Location set to: {lat}, {lng}, {alt}")
                else:
                    self._log_message(f"📍 Location will be set when bot starts")
            else:
                messagebox.showerror("Error", "Invalid location format. Use: lat, lng, alt")
        
        except ValueError:
            messagebox.showerror("Error", "Invalid location format. Use: lat, lng, alt")
    
    def apply_settings(self):
        """Apply bot settings"""
        if self.bot:
            # Update bot configuration
            self.bot.config['catch_pokemon'] = self.catch_pokemon_var.get()
            self.bot.config['spin_pokestops'] = self.spin_pokestops_var.get()
            self.bot.config['battle_gyms'] = self.battle_gyms_var.get()
            self.bot.config['human_like_delays'] = self.human_like_delays_var.get()
            
            self._log_message("⚙️ Settings applied")
        else:
            self._log_message("⚙️ Settings will be applied when bot starts")
    
    def refresh_statistics(self):
        """Refresh bot statistics"""
        if self.bot:
            stats = self.bot.get_detailed_statistics()
            
            # Clear and update statistics display
            self.stats_text.delete(1.0, tk.END)
            
            stats_text = "📊 Enhanced Pokemon GO Bot Statistics\n"
            stats_text += "=" * 50 + "\n\n"
            
            # Basic stats
            stats_text += "🎮 Basic Statistics:\n"
            stats_text += f"  • Pokemon Caught: {stats.get('pokemon_caught', 0)}\n"
            stats_text += f"  • Pokestops Spun: {stats.get('pokestops_spun', 0)}\n"
            stats_text += f"  • Gyms Battled: {stats.get('gyms_battled', 0)}\n"
            stats_text += f"  • Eggs Hatched: {stats.get('eggs_hatched', 0)}\n"
            stats_text += f"  • Distance Walked: {stats.get('distance_walked', 0):.2f} km\n"
            stats_text += f"  • XP Gained: {stats.get('xp_gained', 0)}\n"
            stats_text += f"  • Stardust Gained: {stats.get('stardust_gained', 0)}\n"
            stats_text += f"  • Items Collected: {stats.get('items_collected', 0)}\n\n"
            
            # Session stats
            stats_text += "⏱️ Session Statistics:\n"
            stats_text += f"  • Session Duration: {stats.get('runtime_formatted', '00:00:00')}\n"
            stats_text += f"  • Pokemon per Hour: {stats.get('pokemon_per_hour', 0):.2f}\n"
            stats_text += f"  • Pokestops per Hour: {stats.get('pokestops_per_hour', 0):.2f}\n"
            stats_text += f"  • XP per Hour: {stats.get('xp_per_hour', 0):.2f}\n\n"
            
            # Pokemon stats
            stats_text += "🐾 Pokemon Statistics:\n"
            stats_text += f"  • Total Pokemon: {stats.get('total_pokemon', 0)}\n"
            stats_text += f"  • Unique Pokemon: {stats.get('unique_pokemon', 0)}\n"
            stats_text += f"  • Shiny Pokemon: {stats.get('shiny_pokemon', 0)}\n"
            stats_text += f"  • Perfect IV Pokemon: {stats.get('perfect_iv_pokemon', 0)}\n"
            stats_text += f"  • Legendary Pokemon: {stats.get('legendary_pokemon', 0)}\n"
            stats_text += f"  • Mythical Pokemon: {stats.get('mythical_pokemon', 0)}\n\n"
            
            # Bot status
            stats_text += "🤖 Bot Status:\n"
            stats_text += f"  • Current Level: {stats.get('current_level', 1)}\n"
            stats_text += f"  • Errors Encountered: {stats.get('errors_encountered', 0)}\n"
            stats_text += f"  • API Initialized: {self.bot.api_initialized}\n"
            stats_text += f"  • pgoapi Available: {self.bot.pgoapi is not None}\n"
            
            self.stats_text.insert(1.0, stats_text)
            
            # Update quick stats
            self.stats_vars['pokemon_caught'].set(str(stats.get('pokemon_caught', 0)))
            self.stats_vars['pokestops_spun'].set(str(stats.get('pokestops_spun', 0)))
            self.stats_vars['gyms_battled'].set(str(stats.get('gyms_battled', 0)))
            self.stats_vars['xp_gained'].set(str(stats.get('xp_gained', 0)))
            self.stats_vars['session_duration'].set(stats.get('runtime_formatted', '00:00:00'))
    
    def clear_logs(self):
        """Clear the logs"""
        self.logs_text.delete(1.0, tk.END)
    
    def _bot_callback(self, message):
        """Callback function for bot status updates"""
        self._log_message(message)
    
    def _log_message(self, message):
        """Log a message to the logs tab"""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.logs_text.insert(tk.END, log_entry)
        self.logs_text.see(tk.END)
    
    def run(self):
        """Run the GUI"""
        if hasattr(self, 'root'):
            self.root.mainloop()

# ADDED: Integration with existing Thunderbolt GUI
def integrate_with_thunderbolt_gui(parent_frame):
    """Integrate the enhanced bot with the existing Thunderbolt GUI"""
    try:
        # Create enhanced bot GUI
        enhanced_bot_gui = EnhancedPokemonGoBotGUI(parent_frame)
        
        # Add to Thunderbolt notebook if available
        if hasattr(parent_frame, 'notebook'):
            # Add as a new tab to existing notebook
            enhanced_bot_gui.notebook.pack_forget()  # Remove from parent
            enhanced_tab = ttk.Frame(parent_frame.notebook)
            parent_frame.notebook.add(enhanced_tab, text="🚀 Enhanced pgoapi")
            
            # Move all tabs to the new frame
            for tab_id in enhanced_bot_gui.notebook.tabs():
                tab_frame = enhanced_bot_gui.notebook.nametowidget(tab_id)
                tab_text = enhanced_bot_gui.notebook.tab(tab_id, "text")
                enhanced_bot_gui.notebook.forget(tab_id)
                parent_frame.notebook.add(tab_frame, text=tab_text)
        
        return enhanced_bot_gui
    
    except Exception as e:
        print(f"Error integrating with Thunderbolt GUI: {e}")
        return None

# ADDED: Standalone usage
if __name__ == "__main__":
    # Create and run the enhanced bot GUI
    app = EnhancedPokemonGoBotGUI()
    app.run()
