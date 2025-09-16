#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pokemon Go Bot GUI Integration for VexityBot
Complete Pokemon Go Bot management interface with PTC login integration
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog, filedialog
import threading
import time
import webbrowser
from datetime import datetime
from typing import Dict, List, Optional, Any
import json
import os
import sys

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from PokemonGoBot_SpringBoot_Integration import PokemonGoBotSpringBootIntegration
    from Thunderbolt_PokemonGO_Bot import ThunderboltPokemonGOBot
    INTEGRATION_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Pokemon Go Bot integration not available: {e}")
    INTEGRATION_AVAILABLE = False

class PokemonGoBotGUITab:
    """Complete Pokemon Go Bot GUI Tab for VexityBot with PTC Integration"""
    
    def __init__(self, parent, gui_callback=None):
        self.parent = parent
        self.gui_callback = gui_callback
        
        # PTC Login Credentials - UPDATED
        self.ptc_username = "InsaneDexHolder"
        self.ptc_password = "Torey991200@##@@##"
        self.niantic_id = "7156233866"
        
        # Initialize integrations
        if INTEGRATION_AVAILABLE:
            self.integration = PokemonGoBotSpringBootIntegration(self.update_status)
            self.thunderbolt_bot = ThunderboltPokemonGOBot(self.update_status)
        else:
            self.integration = None
            self.thunderbolt_bot = None
        
        # Bot management
        self.active_bots = {}
        self.bot_threads = {}
        self.is_running = False
        
        # GUI variables
        self.bot_vars = {}
        self.status_vars = {}
        self.stats_vars = {}
        self.location_vars = {}
        self.credentials_vars = {}
        
        # Initialize status bar early - ADDED
        self.status_bar = None  # Will be properly initialized in create_gui
        
        # Statistics
        self.stats = {
            'pokemon_caught': 0,
            'pokestops_spun': 0,
            'gyms_battled': 0,
            'raids_completed': 0,
            'xp_gained': 0,
            'stardust_earned': 0,
            'start_time': None,
            'last_update': None
        }
        
        # Create GUI elements
        self.create_gui()
        
        # Start status update thread
        self.status_thread = threading.Thread(target=self._status_update_loop, daemon=True)
        self.status_thread.start()
        
        # Initialize with PTC credentials
        self._initialize_ptc_credentials()
    
    def _initialize_ptc_credentials(self):
        """Initialize PTC credentials and auto-start bot"""
        if self.thunderbolt_bot:
            self.thunderbolt_bot.set_credentials(
                self.ptc_username,
                self.ptc_password,
                "PTC"
            )
            self.update_status(f"✅ PTC credentials set: {self.ptc_username}")
            self.update_status(f"🆔 Niantic ID: {self.niantic_id}")
            
            # AUTO-START BOT IMMEDIATELY
            self.update_status("🚀 AUTO-STARTING BOT - LOGGING IN AND PLAYING NOW!")
            self._auto_start_bot()
        else:
            self.update_status("❌ Thunderbolt bot not available")
    
    def _auto_start_bot(self):
        """Automatically start the bot and begin playing"""
        def auto_start_thread():
            try:
                # Set credentials
                self.thunderbolt_bot.set_credentials(
                    self.ptc_username,
                    self.ptc_password,
                    "PTC"
                )
                
                # Set Niantic ID
                self.thunderbolt_bot.set_niantic_id(self.niantic_id)
                
                # Set location to NYC (Times Square)
                lat = 40.7589
                lng = -73.9851
                alt = 10
                self.thunderbolt_bot.set_location(lat, lng, alt)
                
                # Apply optimal settings for playing
                self.thunderbolt_bot.set_walk_speed(4.16)
                self.thunderbolt_bot.set_catch_pokemon(True)
                self.thunderbolt_bot.set_spin_pokestops(True)
                self.thunderbolt_bot.set_battle_gyms(False)
                self.thunderbolt_bot.set_min_cp_threshold(100)
                
                # Start bot in catching mode
                if self.thunderbolt_bot.start_bot("catching"):
                    self.is_running = True
                    self.stats['start_time'] = datetime.now()
                    self.update_status("🎮 BOT IS NOW PLAYING ON YOUR ACCOUNT!")
                    self.update_status(f"🆔 Niantic ID: {self.niantic_id}")
                    self.update_status(f"📍 Location: {lat}, {lng} (Times Square, NYC)")
                    self.update_status("🎯 Mode: Catching Pokemon and Spinning Pokestops")
                    self.update_status("⚡ Walk Speed: 4.16 km/h")
                    self.update_status("🔥 Min CP: 100")
                    self._update_bot_status("PLAYING", "green")
                    
                    # Start map integration
                    self.refresh_map_data()
                    
                    # Start auto-refresh of map data
                    self._start_auto_map_refresh()
                    
                else:
                    self.update_status("❌ Failed to auto-start bot")
                    
            except Exception as e:
                self.update_status(f"❌ Error auto-starting bot: {e}")
        
        threading.Thread(target=auto_start_thread, daemon=True).start()
    
    def _start_auto_map_refresh(self):
        """Start automatic map data refresh"""
        def auto_refresh_thread():
            while self.is_running:
                try:
                    time.sleep(30)  # Refresh every 30 seconds
                    if self.is_running:
                        self.refresh_map_data()
                        self.update_status("🔄 Map data refreshed - looking for Pokemon...")
                except Exception as e:
                    self.update_status(f"❌ Map refresh error: {e}")
        
        threading.Thread(target=auto_refresh_thread, daemon=True).start()
    
    def create_gui(self):
        """Create the complete Pokemon Go Bot GUI tab"""
        # Main frame with padding - UPDATED to store main_frame in self.parent
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.parent = main_frame  # Store the main frame instead of the notebook
        
        # Header frame with title and quick actions
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title and status
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        title_label = ttk.Label(title_frame, text="⚡ Thunderbolt Pokemon GO Bot", font=('Arial', 18, 'bold'))
        title_label.pack(side=tk.LEFT)
        
        # Status indicator
        self.status_indicator = ttk.Label(title_frame, text="● OFFLINE", foreground="red", font=('Arial', 12, 'bold'))
        self.status_indicator.pack(side=tk.LEFT, padx=(20, 0))
        
        # Quick action buttons
        quick_frame = ttk.Frame(header_frame)
        quick_frame.pack(side=tk.RIGHT)
        
        ttk.Button(quick_frame, text="🚀 Start All", command=self.start_all_bots, style="Accent.TButton").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(quick_frame, text="⏹️ Stop All", command=self.stop_all_bots).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(quick_frame, text="🔄 Refresh", command=self.refresh_all_status).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(quick_frame, text="🗺️ Open Map", command=self.open_pokemon_map).pack(side=tk.LEFT, padx=(0, 5))
        
        # GPS Map Hunt Controls - ADDED
        ttk.Button(quick_frame, text="🎯 Hunt Mew", command=self.start_mew_hunt, style="Accent.TButton").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(quick_frame, text="🎯 Hunt Mewtwo", command=self.start_mewtwo_hunt, style="Accent.TButton").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(quick_frame, text="🛑 Stop Hunt", command=self.stop_gps_hunt).pack(side=tk.LEFT)
        
        # Create notebook for different sections
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Initialize status bar early - ADDED
        self.status_bar = ttk.Label(main_frame, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=(5, 0))
        
        # Dashboard Tab
        self.create_dashboard_tab(notebook)
        
        # Bot Control Tab
        self.create_bot_control_tab(notebook)
        
        # Pokemon Management Tab
        self.create_pokemon_management_tab(notebook)
        
        # Map & Location Tab
        self.create_map_location_tab(notebook)
        
        # Statistics Tab
        self.create_statistics_tab(notebook)
        
        # Configuration Tab
        self.create_configuration_tab(notebook)
        
        # Logs Tab
        self.create_logs_tab(notebook)
    
    def create_dashboard_tab(self, parent):
        """Create main dashboard tab"""
        dashboard_frame = ttk.Frame(parent)
        parent.add(dashboard_frame, text="📊 Dashboard")
        
        # Top row - Quick stats and controls
        top_frame = ttk.Frame(dashboard_frame)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Left side - Bot status and controls
        left_frame = ttk.LabelFrame(top_frame, text="Bot Status", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Bot status display
        self.bot_status_frame = ttk.Frame(left_frame)
        self.bot_status_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Bot status labels
        ttk.Label(self.bot_status_frame, text="Status:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W)
        self.bot_status_label = ttk.Label(self.bot_status_frame, text="Offline", foreground="red")
        self.bot_status_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(self.bot_status_frame, text="Location:", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky=tk.W)
        self.location_label = ttk.Label(self.bot_status_frame, text="Not Set")
        self.location_label.grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(self.bot_status_frame, text="Uptime:", font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky=tk.W)
        self.uptime_label = ttk.Label(self.bot_status_frame, text="00:00:00")
        self.uptime_label.grid(row=2, column=1, sticky=tk.W, padx=(10, 0))
        
        # Bot control buttons
        control_frame = ttk.Frame(left_frame)
        control_frame.pack(fill=tk.X)
        
        ttk.Button(control_frame, text="🚀 Start Bot", command=self.start_main_bot, style="Accent.TButton").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="⏹️ Stop Bot", command=self.stop_main_bot).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="🔄 Restart", command=self.restart_main_bot).pack(side=tk.LEFT)
        
        # Right side - Quick stats
        right_frame = ttk.LabelFrame(top_frame, text="Quick Stats", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Stats grid
        stats_grid = ttk.Frame(right_frame)
        stats_grid.pack(fill=tk.BOTH, expand=True)
        
        # Create stats labels
        stats_labels = [
            ("Pokemon Caught:", "pokemon_caught"),
            ("Pokestops Spun:", "pokestops_spun"),
            ("Gyms Battled:", "gyms_battled"),
            ("XP Gained:", "xp_gained"),
            ("Stardust Earned:", "stardust_earned"),
            ("Raids Completed:", "raids_completed"),
            ("Level:", "level"),
            ("Team:", "team"),
            ("Pokemon Storage:", "pokemon_storage"),
            ("Item Storage:", "item_storage")
        ]
        
        self.quick_stats_vars = {}
        for i, (label_text, var_name) in enumerate(stats_labels):
            row = i // 2
            col = (i % 2) * 2
            
            ttk.Label(stats_grid, text=label_text, font=('Arial', 9, 'bold')).grid(row=row, column=col, sticky=tk.W, padx=(0, 5), pady=2)
            
            var = tk.StringVar(value="0")
            self.quick_stats_vars[var_name] = var
            ttk.Label(stats_grid, textvariable=var, font=('Arial', 9), foreground="blue").grid(row=row, column=col+1, sticky=tk.W, padx=(0, 20))
        
        # Middle row - Map integration
        map_frame = ttk.LabelFrame(dashboard_frame, text="🗺️ Map Integration", padding=10)
        map_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Map controls
        map_controls = ttk.Frame(map_frame)
        map_controls.pack(fill=tk.X)
        
        ttk.Button(map_controls, text="🗺️ Open Pokemon Map", command=self.open_pokemon_map).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(map_controls, text="📍 Set Current Location", command=self.set_current_location).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(map_controls, text="🔄 Refresh Map Data", command=self.refresh_map_data).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(map_controls, text="🎯 Find Rare Pokemon", command=self.find_rare_pokemon).pack(side=tk.LEFT)
        
        # Map info display
        self.map_info_frame = ttk.Frame(map_frame)
        self.map_info_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(self.map_info_frame, text="Nearby Pokemon:", font=('Arial', 9, 'bold')).pack(side=tk.LEFT)
        self.nearby_pokemon_label = ttk.Label(self.map_info_frame, text="0")
        self.nearby_pokemon_label.pack(side=tk.LEFT, padx=(5, 20))
        
        ttk.Label(self.map_info_frame, text="Nearby Pokestops:", font=('Arial', 9, 'bold')).pack(side=tk.LEFT)
        self.nearby_pokestops_label = ttk.Label(self.map_info_frame, text="0")
        self.nearby_pokestops_label.pack(side=tk.LEFT, padx=(5, 20))
        
        ttk.Label(self.map_info_frame, text="Nearby Gyms:", font=('Arial', 9, 'bold')).pack(side=tk.LEFT)
        self.nearby_gyms_label = ttk.Label(self.map_info_frame, text="0")
        self.nearby_gyms_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # Bottom row - Recent activity
        activity_frame = ttk.LabelFrame(dashboard_frame, text="📈 Recent Activity", padding=10)
        activity_frame.pack(fill=tk.BOTH, expand=True)
        
        # Activity log
        self.activity_log = scrolledtext.ScrolledText(activity_frame, height=8, width=80, font=('Consolas', 9))
        self.activity_log.pack(fill=tk.BOTH, expand=True)
        
        # Activity controls
        activity_controls = ttk.Frame(activity_frame)
        activity_controls.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(activity_controls, text="Clear Log", command=self.clear_activity_log).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(activity_controls, text="Save Log", command=self.save_activity_log).pack(side=tk.LEFT)
        
        # Auto-scroll checkbox
        self.auto_scroll_activity = tk.BooleanVar(value=True)
        ttk.Checkbutton(activity_controls, text="Auto-scroll", variable=self.auto_scroll_activity).pack(side=tk.RIGHT)
    
    def create_bot_control_tab(self, parent):
        """Create bot control tab"""
        control_frame = ttk.Frame(parent)
        parent.add(control_frame, text="🤖 Bot Control")
        
        # Bot selection and credentials
        credentials_frame = ttk.LabelFrame(control_frame, text="🔐 Bot Credentials", padding=10)
        credentials_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Credentials form
        cred_form = ttk.Frame(credentials_frame)
        cred_form.pack(fill=tk.X)
        
        ttk.Label(cred_form, text="Username:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.username_var = tk.StringVar(value=self.ptc_username)
        ttk.Entry(cred_form, textvariable=self.username_var, width=25).grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        ttk.Label(cred_form, text="Password:", font=('Arial', 10, 'bold')).grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.password_var = tk.StringVar(value=self.ptc_password)
        ttk.Entry(cred_form, textvariable=self.password_var, show="*", width=25).grid(row=0, column=3, sticky=tk.W)
        
        # Auth type
        ttk.Label(cred_form, text="Auth Type:", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(10, 0))
        self.auth_type_var = tk.StringVar(value="PTC")
        auth_combo = ttk.Combobox(cred_form, textvariable=self.auth_type_var, values=["PTC", "Google"], width=22)
        auth_combo.grid(row=1, column=1, sticky=tk.W, pady=(10, 0))
        
        ttk.Label(cred_form, text="Niantic ID:", font=('Arial', 10, 'bold')).grid(row=1, column=2, sticky=tk.W, padx=(0, 5), pady=(10, 0))
        self.niantic_id_var = tk.StringVar(value=self.niantic_id)
        ttk.Entry(cred_form, textvariable=self.niantic_id_var, width=25).grid(row=1, column=3, sticky=tk.W, pady=(10, 0))
        
        # Location settings
        location_frame = ttk.LabelFrame(control_frame, text="📍 Location Settings", padding=10)
        location_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Location form
        loc_form = ttk.Frame(location_frame)
        loc_form.pack(fill=tk.X)
        
        ttk.Label(loc_form, text="Latitude:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.lat_var = tk.StringVar(value="40.7589")
        ttk.Entry(loc_form, textvariable=self.lat_var, width=15).grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        ttk.Label(loc_form, text="Longitude:", font=('Arial', 10, 'bold')).grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.lng_var = tk.StringVar(value="-73.9851")
        ttk.Entry(loc_form, textvariable=self.lng_var, width=15).grid(row=0, column=3, sticky=tk.W, padx=(0, 20))
        
        ttk.Label(loc_form, text="Altitude:", font=('Arial', 10, 'bold')).grid(row=0, column=4, sticky=tk.W, padx=(0, 5))
        self.alt_var = tk.StringVar(value="10")
        ttk.Entry(loc_form, textvariable=self.alt_var, width=10).grid(row=0, column=5, sticky=tk.W)
        
        # Location buttons
        loc_buttons = ttk.Frame(location_frame)
        loc_buttons.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(loc_buttons, text="📍 Set Location", command=self.set_bot_location).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(loc_buttons, text="🗺️ Get Current Location", command=self.get_current_location).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(loc_buttons, text="🎯 Random Location", command=self.set_random_location).pack(side=tk.LEFT)
        
        # Bot settings
        settings_frame = ttk.LabelFrame(control_frame, text="⚙️ Bot Settings", padding=10)
        settings_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Settings grid
        settings_grid = ttk.Frame(settings_frame)
        settings_grid.pack(fill=tk.X)
        
        # Walk speed
        ttk.Label(settings_grid, text="Walk Speed:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.walk_speed_var = tk.StringVar(value="4.16")
        ttk.Entry(settings_grid, textvariable=self.walk_speed_var, width=10).grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        # Min CP threshold
        ttk.Label(settings_grid, text="Min CP:", font=('Arial', 10, 'bold')).grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.min_cp_var = tk.StringVar(value="100")
        ttk.Entry(settings_grid, textvariable=self.min_cp_var, width=10).grid(row=0, column=3, sticky=tk.W)
        
        # Checkboxes
        checkbox_frame = ttk.Frame(settings_frame)
        checkbox_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.catch_pokemon_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(checkbox_frame, text="Catch Pokemon", variable=self.catch_pokemon_var).pack(side=tk.LEFT, padx=(0, 20))
        
        self.spin_pokestops_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(checkbox_frame, text="Spin Pokestops", variable=self.spin_pokestops_var).pack(side=tk.LEFT, padx=(0, 20))
        
        self.battle_gyms_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(checkbox_frame, text="Battle Gyms", variable=self.battle_gyms_var).pack(side=tk.LEFT, padx=(0, 20))
        
        self.catch_legendary_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(checkbox_frame, text="Catch Legendary", variable=self.catch_legendary_var).pack(side=tk.LEFT)
        
        # Bot control buttons
        control_buttons_frame = ttk.LabelFrame(control_frame, text="🎮 Bot Control", padding=10)
        control_buttons_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Main control buttons
        main_controls = ttk.Frame(control_buttons_frame)
        main_controls.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(main_controls, text="🚀 Start Bot", command=self.start_main_bot, style="Accent.TButton").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(main_controls, text="⏹️ Stop Bot", command=self.stop_main_bot).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(main_controls, text="🔄 Restart Bot", command=self.restart_main_bot).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(main_controls, text="⚙️ Apply Settings", command=self.apply_bot_settings).pack(side=tk.LEFT)
        
        # Mode selection
        mode_frame = ttk.Frame(control_buttons_frame)
        mode_frame.pack(fill=tk.X)
        
        ttk.Label(mode_frame, text="Bot Mode:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
        
        self.bot_mode_var = tk.StringVar(value="catching")
        mode_combo = ttk.Combobox(mode_frame, textvariable=self.bot_mode_var, 
                                 values=["catching", "exploring", "raiding", "battling", "map_mode"], width=15)
        mode_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(mode_frame, text="🔄 Change Mode", command=self.change_bot_mode).pack(side=tk.LEFT)
    
    def create_map_location_tab(self, parent):
        """Create map and location tab"""
        map_frame = ttk.Frame(parent)
        parent.add(map_frame, text="🗺️ Map & Location")
        
        # Map controls
        map_controls_frame = ttk.LabelFrame(map_frame, text="🗺️ Map Controls", padding=10)
        map_controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Map buttons
        map_buttons = ttk.Frame(map_controls_frame)
        map_buttons.pack(fill=tk.X)
        
        ttk.Button(map_buttons, text="🗺️ Open Pokemon Map", command=self.open_pokemon_map).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(map_buttons, text="🔄 Refresh Map Data", command=self.refresh_map_data).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(map_buttons, text="📍 Set Current Location", command=self.set_current_location).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(map_buttons, text="🎯 Find Rare Pokemon", command=self.find_rare_pokemon).pack(side=tk.LEFT)
        
        # Location search
        search_frame = ttk.Frame(map_controls_frame)
        search_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(search_frame, text="Search Location:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 5))
        self.location_search_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.location_search_var, width=30).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(search_frame, text="🔍 Search", command=self.search_location).pack(side=tk.LEFT)
        
        # Map data display
        map_data_frame = ttk.LabelFrame(map_frame, text="📍 Map Data", padding=10)
        map_data_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook for map data
        map_notebook = ttk.Notebook(map_data_frame)
        map_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Nearby Pokemon tab
        pokemon_tab = ttk.Frame(map_notebook)
        map_notebook.add(pokemon_tab, text="Pokemon")
        
        # Pokemon list
        pokemon_columns = ('Name', 'CP', 'IV', 'Distance', 'Time Left', 'Actions')
        self.map_pokemon_tree = ttk.Treeview(pokemon_tab, columns=pokemon_columns, show='headings', height=10)
        
        for col in pokemon_columns:
            self.map_pokemon_tree.heading(col, text=col)
            self.map_pokemon_tree.column(col, width=100, anchor=tk.CENTER)
        
        pokemon_scrollbar = ttk.Scrollbar(pokemon_tab, orient=tk.VERTICAL, command=self.map_pokemon_tree.yview)
        self.map_pokemon_tree.configure(yscrollcommand=pokemon_scrollbar.set)
        
        self.map_pokemon_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        pokemon_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Nearby Pokestops tab
        pokestops_tab = ttk.Frame(map_notebook)
        map_notebook.add(pokestops_tab, text="Pokestops")
        
        # Pokestops list
        pokestops_columns = ('Name', 'Lure Type', 'Distance', 'Actions')
        self.map_pokestops_tree = ttk.Treeview(pokestops_tab, columns=pokestops_columns, show='headings', height=10)
        
        for col in pokestops_columns:
            self.map_pokestops_tree.heading(col, text=col)
            self.map_pokestops_tree.column(col, width=150, anchor=tk.CENTER)
        
        pokestops_scrollbar = ttk.Scrollbar(pokestops_tab, orient=tk.VERTICAL, command=self.map_pokestops_tree.yview)
        self.map_pokestops_tree.configure(yscrollcommand=pokestops_scrollbar.set)
        
        self.map_pokestops_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        pokestops_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Nearby Gyms tab
        gyms_tab = ttk.Frame(map_notebook)
        map_notebook.add(gyms_tab, text="Gyms")
        
        # Gyms list
        gyms_columns = ('Name', 'Team', 'Level', 'Raid Boss', 'Distance', 'Actions')
        self.map_gyms_tree = ttk.Treeview(gyms_tab, columns=gyms_columns, show='headings', height=10)
        
        for col in gyms_columns:
            self.map_gyms_tree.heading(col, text=col)
            self.map_gyms_tree.column(col, width=120, anchor=tk.CENTER)
        
        gyms_scrollbar = ttk.Scrollbar(gyms_tab, orient=tk.VERTICAL, command=self.map_gyms_tree.yview)
        self.map_gyms_tree.configure(yscrollcommand=gyms_scrollbar.set)
        
        self.map_gyms_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        gyms_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bot control frame - ADDED
        control_frame = ttk.Frame(map_frame)
        control_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Bot frame - ADDED
        bot_frame = ttk.Frame(map_frame)
        bot_frame.pack(fill=tk.BOTH, expand=True)
        
        # Bot control buttons
        ttk.Button(control_frame, text="Load Bot", command=self.load_selected_bot).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="Unload Bot", command=self.unload_selected_bot).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="Reload Bot", command=self.reload_selected_bot).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="Start Bot", command=self.start_selected_bot).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="Stop Bot", command=self.stop_selected_bot).pack(side=tk.LEFT, padx=(0, 5))
        
        # Separator
        ttk.Separator(control_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=10, fill=tk.Y)
        
        # Backend control buttons
        ttk.Button(control_frame, text="Restart Backend", command=self.restart_backend).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="Refresh Status", command=self.refresh_all_status).pack(side=tk.LEFT, padx=(0, 5))
        
        # Add new bot button
        ttk.Button(control_frame, text="Add New Bot", command=self.add_new_bot).pack(side=tk.RIGHT)
        
        # Bots list frame
        bots_frame = ttk.LabelFrame(bot_frame, text="Registered Bots")
        bots_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Create treeview for bots
        columns = ('Name', 'Status', 'Location', 'Pokemon Caught', 'XP Gained', 'Last Update')
        self.bots_tree = ttk.Treeview(bots_frame, columns=columns, show='headings', height=10)
        
        # Configure columns
        for col in columns:
            self.bots_tree.heading(col, text=col)
            self.bots_tree.column(col, width=120, anchor=tk.CENTER)
        
        # Scrollbar for bots tree
        bots_scrollbar = ttk.Scrollbar(bots_frame, orient=tk.VERTICAL, command=self.bots_tree.yview)
        self.bots_tree.configure(yscrollcommand=bots_scrollbar.set)
        
        # Pack bots tree
        self.bots_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        bots_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bot actions frame
        actions_frame = ttk.Frame(bot_frame)
        actions_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Action buttons
        ttk.Button(actions_frame, text="Start Selected", command=self.start_selected_bot).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(actions_frame, text="Stop Selected", command=self.stop_selected_bot).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(actions_frame, text="Configure Selected", command=self.configure_selected_bot).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(actions_frame, text="View Details", command=self.view_bot_details).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(actions_frame, text="Remove Selected", command=self.remove_selected_bot).pack(side=tk.LEFT)
        
        # Status bar - REMOVED duplicate definition (now defined in create_gui)
    
    def create_pokemon_management_tab(self, parent):
        """Create Pokemon management tab"""
        pokemon_frame = ttk.Frame(parent)
        parent.add(pokemon_frame, text="Pokemon Management")
        
        # Bot selection frame
        bot_selection_frame = ttk.Frame(pokemon_frame)
        bot_selection_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(bot_selection_frame, text="Select Bot:").pack(side=tk.LEFT, padx=(0, 5))
        self.selected_bot_var = tk.StringVar()
        self.bot_combo = ttk.Combobox(bot_selection_frame, textvariable=self.selected_bot_var, width=20)
        self.bot_combo.pack(side=tk.LEFT, padx=(0, 10))
        self.bot_combo.bind('<<ComboboxSelected>>', self.on_bot_selected)
        
        ttk.Button(bot_selection_frame, text="Refresh Pokemon", command=self.refresh_pokemon).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(bot_selection_frame, text="Transfer All Duplicates", command=self.transfer_duplicates).pack(side=tk.LEFT, padx=(0, 5))
        
        # Pokemon list frame
        pokemon_list_frame = ttk.LabelFrame(pokemon_frame, text="Pokemon List")
        pokemon_list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Create treeview for Pokemon
        pokemon_columns = ('ID', 'Name', 'CP', 'IV', 'Level', 'Type', 'Favorite', 'Actions')
        self.pokemon_tree = ttk.Treeview(pokemon_list_frame, columns=pokemon_columns, show='headings', height=15)
        
        # Configure columns
        for col in pokemon_columns:
            self.pokemon_tree.heading(col, text=col)
            self.pokemon_tree.column(col, width=100, anchor=tk.CENTER)
        
        # Scrollbar for Pokemon tree
        pokemon_scrollbar = ttk.Scrollbar(pokemon_list_frame, orient=tk.VERTICAL, command=self.pokemon_tree.yview)
        self.pokemon_tree.configure(yscrollcommand=pokemon_scrollbar.set)
        
        # Pack Pokemon tree
        self.pokemon_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        pokemon_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Pokemon actions frame
        pokemon_actions_frame = ttk.Frame(pokemon_frame)
        pokemon_actions_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Action buttons
        ttk.Button(pokemon_actions_frame, text="🎯 Force Catch", command=self.force_catch_selected_pokemon, style="Accent.TButton").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(pokemon_actions_frame, text="Transfer Selected", command=self.transfer_selected_pokemon).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(pokemon_actions_frame, text="Evolve Selected", command=self.evolve_selected_pokemon).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(pokemon_actions_frame, text="Power Up Selected", command=self.powerup_selected_pokemon).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(pokemon_actions_frame, text="Toggle Favorite", command=self.toggle_favorite_pokemon).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(pokemon_actions_frame, text="Rename Pokemon", command=self.rename_pokemon).pack(side=tk.LEFT, padx=(0, 5))
    
    def create_item_management_tab(self, parent):
        """Create item management tab"""
        item_frame = ttk.Frame(parent)
        parent.add(item_frame, text="Item Management")
        
        # Bot selection frame
        bot_selection_frame = ttk.Frame(item_frame)
        bot_selection_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(bot_selection_frame, text="Select Bot:").pack(side=tk.LEFT, padx=(0, 5))
        self.selected_item_bot_var = tk.StringVar()
        self.item_bot_combo = ttk.Combobox(bot_selection_frame, textvariable=self.selected_item_bot_var, width=20)
        self.item_bot_combo.pack(side=tk.LEFT, padx=(0, 10))
        self.item_bot_combo.bind('<<ComboboxSelected>>', self.on_item_bot_selected)
        
        ttk.Button(bot_selection_frame, text="Refresh Items", command=self.refresh_items).pack(side=tk.LEFT, padx=(0, 5))
        
        # Item list frame
        item_list_frame = ttk.LabelFrame(item_frame, text="Items")
        item_list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Create treeview for items
        item_columns = ('ID', 'Name', 'Count', 'Actions')
        self.item_tree = ttk.Treeview(item_list_frame, columns=item_columns, show='headings', height=15)
        
        # Configure columns
        for col in item_columns:
            self.item_tree.heading(col, text=col)
            self.item_tree.column(col, width=150, anchor=tk.CENTER)
        
        # Scrollbar for item tree
        item_scrollbar = ttk.Scrollbar(item_list_frame, orient=tk.VERTICAL, command=self.item_tree.yview)
        self.item_tree.configure(yscrollcommand=item_scrollbar.set)
        
        # Pack item tree
        self.item_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        item_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Item actions frame
        item_actions_frame = ttk.Frame(item_frame)
        item_actions_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Action buttons
        ttk.Button(item_actions_frame, text="Drop Selected", command=self.drop_selected_item).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(item_actions_frame, text="Use Incense", command=self.use_incense).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(item_actions_frame, text="Use Lucky Egg", command=self.use_lucky_egg).pack(side=tk.LEFT, padx=(0, 5))
    
    def create_statistics_tab(self, parent):
        """Create statistics tab"""
        stats_frame = ttk.Frame(parent)
        parent.add(stats_frame, text="Statistics")
        
        # Overall statistics frame
        overall_frame = ttk.LabelFrame(stats_frame, text="Overall Statistics")
        overall_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Stats grid
        stats_grid = ttk.Frame(overall_frame)
        stats_grid.pack(fill=tk.X, padx=10, pady=10)
        
        # Create stats labels
        stats_labels = [
            ("Total Bots:", "total_bots"),
            ("Active Bots:", "active_bots"),
            ("Pokemon Caught:", "pokemon_caught"),
            ("Pokestops Spun:", "pokestops_spun"),
            ("Gyms Battled:", "gyms_battled"),
            ("Raids Completed:", "raids_completed"),
            ("XP Gained:", "xp_gained"),
            ("Stardust Earned:", "stardust_earned")
        ]
        
        self.stats_vars = {}
        for i, (label_text, var_name) in enumerate(stats_labels):
            row = i // 4
            col = (i % 4) * 2
            
            ttk.Label(stats_grid, text=label_text).grid(row=row, column=col, sticky=tk.W, padx=(0, 5))
            
            var = tk.StringVar(value="0")
            self.stats_vars[var_name] = var
            ttk.Label(stats_grid, textvariable=var, font=('Arial', 10, 'bold')).grid(row=row, column=col+1, sticky=tk.W, padx=(0, 20))
        
        # Individual bot statistics
        individual_frame = ttk.LabelFrame(stats_frame, text="Individual Bot Statistics")
        individual_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview for individual stats
        individual_columns = ('Bot Name', 'Status', 'Pokemon Caught', 'Pokestops Spun', 'XP Gained', 'Uptime')
        self.individual_tree = ttk.Treeview(individual_frame, columns=individual_columns, show='headings', height=8)
        
        # Configure columns
        for col in individual_columns:
            self.individual_tree.heading(col, text=col)
            self.individual_tree.column(col, width=120, anchor=tk.CENTER)
        
        # Scrollbar for individual tree
        individual_scrollbar = ttk.Scrollbar(individual_frame, orient=tk.VERTICAL, command=self.individual_tree.yview)
        self.individual_tree.configure(yscrollcommand=individual_scrollbar.set)
        
        # Pack individual tree
        self.individual_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        individual_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_configuration_tab(self, parent):
        """Create configuration tab"""
        config_frame = ttk.Frame(parent)
        parent.add(config_frame, text="Configuration")
        
        # Spring Boot configuration
        spring_frame = ttk.LabelFrame(config_frame, text="Spring Boot Backend Configuration")
        spring_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Configuration entries
        config_entries = [
            ("Base URL:", "base_url", "http://localhost:8080"),
            ("Server Port:", "server_port", "8080"),
            ("JAR File:", "jar_file", "pokemon-go-bot.jar"),
            ("Java Executable:", "java_executable", "java"),
            ("Spring Profile:", "spring_profile", "dev")
        ]
        
        self.config_vars = {}
        for i, (label_text, var_name, default_value) in enumerate(config_entries):
            row_frame = ttk.Frame(spring_frame)
            row_frame.pack(fill=tk.X, padx=10, pady=5)
            
            ttk.Label(row_frame, text=label_text, width=15).pack(side=tk.LEFT)
            
            var = tk.StringVar(value=default_value)
            self.config_vars[var_name] = var
            ttk.Entry(row_frame, textvariable=var, width=40).pack(side=tk.LEFT, padx=(10, 0))
        
        # Configuration buttons
        config_buttons = ttk.Frame(spring_frame)
        config_buttons.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(config_buttons, text="Save Configuration", command=self.save_configuration).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(config_buttons, text="Load Configuration", command=self.load_configuration).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(config_buttons, text="Reset to Defaults", command=self.reset_configuration).pack(side=tk.LEFT)
        
        # Bot template configuration
        template_frame = ttk.LabelFrame(config_frame, text="Bot Template Configuration")
        template_frame.pack(fill=tk.BOTH, expand=True)
        
        # Template settings
        template_text = """{
    "bot_name": "template_bot",
    "enabled": true,
    "location": {
        "lat": 40.7589,
        "lng": -73.9851,
        "alt": 10
    },
    "credentials": {
        "username": "",
        "password": "",
        "auth_type": "PTC"
    },
    "settings": {
        "walk_speed": 4.16,
        "catch_pokemon": true,
        "spin_pokestops": true,
        "battle_gyms": false,
        "catch_legendary": true,
        "catch_shiny": true,
        "transfer_duplicates": true,
        "min_cp_threshold": 100,
        "max_pokemon_storage": 1000
    },
    "advanced": {
        "human_like_delays": true,
        "random_movements": true,
        "smart_timing": true,
        "ban_bypass": true,
        "ai_automation": true
    }
}"""
        
        self.template_text = scrolledtext.ScrolledText(template_frame, height=15, width=70)
        self.template_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.template_text.insert(tk.END, template_text)
    
    def create_logs_tab(self, parent):
        """Create logs tab"""
        logs_frame = ttk.Frame(parent)
        parent.add(logs_frame, text="Logs")
        
        # Log controls
        log_controls = ttk.Frame(logs_frame)
        log_controls.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(log_controls, text="Clear Logs", command=self.clear_logs).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(log_controls, text="Save Logs", command=self.save_logs).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(log_controls, text="Auto-scroll", command=self.toggle_auto_scroll).pack(side=tk.LEFT)
        
        # Log level selection
        ttk.Label(log_controls, text="Log Level:").pack(side=tk.RIGHT, padx=(10, 5))
        self.log_level = tk.StringVar(value="INFO")
        log_level_combo = ttk.Combobox(log_controls, textvariable=self.log_level, values=["DEBUG", "INFO", "WARNING", "ERROR"], width=10)
        log_level_combo.pack(side=tk.RIGHT)
        
        # Log display
        self.log_text = scrolledtext.ScrolledText(logs_frame, height=20, width=80)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Auto-scroll variable
        self.auto_scroll = tk.BooleanVar(value=True)
    
    def update_status(self, message: str):
        """Update status message"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        status_message = f"{timestamp} - {message}"
        
        # Update status bar if it exists - ADDED check
        if hasattr(self, 'status_bar') and self.status_bar is not None:
            self.status_bar.config(text=status_message)
        
        # Add to logs if log_text exists - ADDED check
        if hasattr(self, 'log_text') and self.log_text is not None:
            self.log_text.insert(tk.END, status_message + "\n")
            
            # Auto-scroll if enabled
            if hasattr(self, 'auto_scroll') and self.auto_scroll.get():
                self.log_text.see(tk.END)
        
        # Call GUI callback if provided
        if self.gui_callback:
            self.gui_callback(status_message)
    
    def start_mew_hunt(self):
        """Start GPS map hunt for Mew - ADDED"""
        try:
            if self.thunderbolt_bot:
                self.thunderbolt_bot.start_gps_map_hunt(['mew'])
                self.update_status("🎯 MEW HUNT STARTED! AI is now scanning GPS map for Mew!")
            else:
                self.update_status("❌ Thunderbolt bot not available for Mew hunt")
        except Exception as e:
            self.update_status(f"❌ Mew hunt start error: {e}")
    
    def start_mewtwo_hunt(self):
        """Start GPS map hunt for Mewtwo - ADDED"""
        try:
            if self.thunderbolt_bot:
                self.thunderbolt_bot.start_gps_map_hunt(['mewtwo'])
                self.update_status("🎯 MEWTWO HUNT STARTED! AI is now scanning GPS map for Mewtwo!")
            else:
                self.update_status("❌ Thunderbolt bot not available for Mewtwo hunt")
        except Exception as e:
            self.update_status(f"❌ Mewtwo hunt start error: {e}")
    
    def stop_gps_hunt(self):
        """Stop GPS map hunt - ADDED"""
        try:
            if self.thunderbolt_bot:
                self.thunderbolt_bot.stop_gps_map_hunt()
                self.update_status("🛑 GPS MAP HUNT STOPPED!")
            else:
                self.update_status("❌ Thunderbolt bot not available")
        except Exception as e:
            self.update_status(f"❌ Stop hunt error: {e}")
    
    def start_all_bots(self):
        """Start all registered bots"""
        def start_thread():
            self.integration.start_all_bots()
        
        threading.Thread(target=start_thread, daemon=True).start()
    
    def stop_all_bots(self):
        """Stop all active bots"""
        def stop_thread():
            self.integration.stop_all_bots()
        
        threading.Thread(target=stop_thread, daemon=True).start()
    
    def restart_backend(self):
        """Restart Spring Boot backend"""
        def restart_thread():
            self.integration.restart_spring_boot()
        
        threading.Thread(target=restart_thread, daemon=True).start()
    
    def refresh_all_status(self):
        """Refresh status of all bots"""
        def refresh_thread():
            # Get all bots status
            all_status = self.integration.get_all_bots_status()
            
            # Update GUI
            self.parent.after(0, self._update_bots_display, all_status)
        
        threading.Thread(target=refresh_thread, daemon=True).start()
    
    def add_new_bot(self):
        """Add a new bot"""
        dialog = BotAddDialog(self.parent, self.integration)
        if dialog.result:
            self.refresh_all_status()
    
    def load_selected_bot(self):
        """Load selected bot"""
        selection = self.bots_tree.selection()
        if selection:
            bot_name = self.bots_tree.item(selection[0])['values'][0]
            self.integration.load_bot(bot_name)
            self.refresh_all_status()
    
    def unload_selected_bot(self):
        """Unload selected bot"""
        selection = self.bots_tree.selection()
        if selection:
            bot_name = self.bots_tree.item(selection[0])['values'][0]
            self.integration.unload_bot(bot_name)
            self.refresh_all_status()
    
    def reload_selected_bot(self):
        """Reload selected bot"""
        selection = self.bots_tree.selection()
        if selection:
            bot_name = self.bots_tree.item(selection[0])['values'][0]
            self.integration.reload_bot(bot_name)
            self.refresh_all_status()
    
    def start_selected_bot(self):
        """Start selected bot"""
        selection = self.bots_tree.selection()
        if selection:
            bot_name = self.bots_tree.item(selection[0])['values'][0]
            self.integration.start_bot(bot_name)
            self.refresh_all_status()
    
    def stop_selected_bot(self):
        """Stop selected bot"""
        selection = self.bots_tree.selection()
        if selection:
            bot_name = self.bots_tree.item(selection[0])['values'][0]
            self.integration.stop_bot(bot_name)
            self.refresh_all_status()
    
    def configure_selected_bot(self):
        """Configure selected bot"""
        selection = self.bots_tree.selection()
        if selection:
            bot_name = self.bots_tree.item(selection[0])['values'][0]
            dialog = BotConfigDialog(self.parent, self.integration, bot_name)
    
    def view_bot_details(self):
        """View bot details"""
        selection = self.bots_tree.selection()
        if selection:
            bot_name = self.bots_tree.item(selection[0])['values'][0]
            dialog = BotDetailsDialog(self.parent, self.integration, bot_name)
    
    def remove_selected_bot(self):
        """Remove selected bot"""
        selection = self.bots_tree.selection()
        if selection:
            bot_name = self.bots_tree.item(selection[0])['values'][0]
            if messagebox.askyesno("Confirm", f"Remove bot '{bot_name}'?"):
                # Remove bot logic here
                self.refresh_all_status()
    
    def save_configuration(self):
        """Save configuration"""
        # Save Spring Boot configuration
        config = {}
        for var_name, var in self.config_vars.items():
            config[var_name] = var.get()
        
        # Save to file
        with open('pokemon_go_bot_config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        self.update_status("Configuration saved")
    
    def load_configuration(self):
        """Load configuration"""
        try:
            with open('pokemon_go_bot_config.json', 'r') as f:
                config = json.load(f)
            
            for var_name, value in config.items():
                if var_name in self.config_vars:
                    self.config_vars[var_name].set(value)
            
            self.update_status("Configuration loaded")
        except FileNotFoundError:
            self.update_status("No configuration file found")
        except Exception as e:
            self.update_status(f"Error loading configuration: {e}")
    
    def reset_configuration(self):
        """Reset configuration to defaults"""
        defaults = {
            "base_url": "http://localhost:8080",
            "server_port": "8080",
            "jar_file": "pokemon-go-bot.jar",
            "java_executable": "java",
            "spring_profile": "dev"
        }
        
        for var_name, value in defaults.items():
            if var_name in self.config_vars:
                self.config_vars[var_name].set(value)
        
        self.update_status("Configuration reset to defaults")
    
    def clear_logs(self):
        """Clear log display"""
        self.log_text.delete(1.0, tk.END)
    
    def save_logs(self):
        """Save logs to file"""
        try:
            with open(f'pokemon_go_bot_logs_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt', 'w') as f:
                f.write(self.log_text.get(1.0, tk.END))
            self.update_status("Logs saved to file")
        except Exception as e:
            self.update_status(f"Error saving logs: {e}")
    
    def toggle_auto_scroll(self):
        """Toggle auto-scroll for logs"""
        self.auto_scroll.set(not self.auto_scroll.get())
        status = "enabled" if self.auto_scroll.get() else "disabled"
        self.update_status(f"Auto-scroll {status}")
    
    def _update_bots_display(self, all_status):
        """Update bots display"""
        # Clear existing items
        for item in self.bots_tree.get_children():
            self.bots_tree.delete(item)
        
        # Update bot combo boxes
        bot_names = []
        
        # Add bot data
        if 'bots' in all_status:
            for bot_name, bot_data in all_status['bots'].items():
                bot_names.append(bot_name)
                values = (
                    bot_name,
                    bot_data.get('status', 'Unknown'),
                    f"{bot_data.get('location', {}).get('lat', 0):.4f}, {bot_data.get('location', {}).get('lng', 0):.4f}",
                    bot_data.get('pokemon_caught', 0),
                    bot_data.get('xp_gained', 0),
                    bot_data.get('last_update', 'Never')
                )
                self.bots_tree.insert('', tk.END, values=values)
        
        # Update combo boxes
        self.bot_combo['values'] = bot_names
        self.item_bot_combo['values'] = bot_names
    
    def _update_statistics_display(self, stats):
        """Update statistics display"""
        for var_name, var in self.stats_vars.items():
            if var_name in stats:
                var.set(str(stats[var_name]))
    
    def _status_update_loop(self):
        """Status update loop"""
        while True:
            try:
                # Update statistics
                stats = self.integration.get_statistics()
                self.parent.after(0, self._update_statistics_display, stats)
                
                # Update individual bot stats
                all_status = self.integration.get_all_bots_status()
                self.parent.after(0, self._update_individual_stats, all_status)
                
                time.sleep(5)  # Update every 5 seconds
            except Exception as e:
                self.update_status(f"Status update error: {e}")
                time.sleep(10)  # Wait longer on error
    
    def _update_individual_stats(self, all_status):
        """Update individual bot statistics"""
        # Clear existing items
        for item in self.individual_tree.get_children():
            self.individual_tree.delete(item)
        
        # Add individual bot stats
        if 'bots' in all_status:
            for bot_name, bot_data in all_status['bots'].items():
                uptime = "Unknown"
                if 'start_time' in bot_data:
                    start_time = datetime.fromisoformat(bot_data['start_time'])
                    uptime = str(datetime.now() - start_time).split('.')[0]
                
                values = (
                    bot_name,
                    bot_data.get('status', 'Unknown'),
                    bot_data.get('pokemon_caught', 0),
                    bot_data.get('pokestops_spun', 0),
                    bot_data.get('xp_gained', 0),
                    uptime
                )
                self.individual_tree.insert('', tk.END, values=values)
    
    # Pokemon Management Methods
    def on_bot_selected(self, event=None):
        """Handle bot selection for Pokemon management"""
        bot_name = self.selected_bot_var.get()
        if bot_name:
            self.refresh_pokemon()
    
    def refresh_pokemon(self):
        """Refresh Pokemon list for selected bot"""
        bot_name = self.selected_bot_var.get()
        if not bot_name:
            self.update_status("❌ No bot selected")
            return
        
        def refresh_thread():
            pokemon_data = self.integration.get_pokemons(bot_name)
            self.parent.after(0, self._update_pokemon_display, pokemon_data)
        
        threading.Thread(target=refresh_thread, daemon=True).start()
    
    def _update_pokemon_display(self, pokemon_data):
        """Update Pokemon display"""
        # Clear existing items
        for item in self.pokemon_tree.get_children():
            self.pokemon_tree.delete(item)
        
        # Add Pokemon data
        if 'pokemons' in pokemon_data:
            for pokemon in pokemon_data['pokemons']:
                values = (
                    pokemon.get('id', ''),
                    pokemon.get('name', ''),
                    pokemon.get('cp', 0),
                    pokemon.get('iv', 0),
                    pokemon.get('level', 0),
                    pokemon.get('type', ''),
                    'Yes' if pokemon.get('favorite', False) else 'No',
                    'Actions'
                )
                self.pokemon_tree.insert('', tk.END, values=values)
    
    def transfer_selected_pokemon(self):
        """Transfer selected Pokemon"""
        selection = self.pokemon_tree.selection()
        if selection:
            pokemon_id = self.pokemon_tree.item(selection[0])['values'][0]
            bot_name = self.selected_bot_var.get()
            if bot_name:
                self.integration.transfer_pokemon(bot_name, pokemon_id)
                self.refresh_pokemon()
    
    def evolve_selected_pokemon(self):
        """Evolve selected Pokemon"""
        selection = self.pokemon_tree.selection()
        if selection:
            pokemon_id = self.pokemon_tree.item(selection[0])['values'][0]
            bot_name = self.selected_bot_var.get()
            if bot_name:
                self.integration.evolve_pokemon(bot_name, pokemon_id)
                self.refresh_pokemon()
    
    def powerup_selected_pokemon(self):
        """Power up selected Pokemon"""
        selection = self.pokemon_tree.selection()
        if selection:
            pokemon_id = self.pokemon_tree.item(selection[0])['values'][0]
            bot_name = self.selected_bot_var.get()
            if bot_name:
                self.integration.powerup_pokemon(bot_name, pokemon_id)
                self.refresh_pokemon()
    
    def toggle_favorite_pokemon(self):
        """Toggle favorite for selected Pokemon"""
        selection = self.pokemon_tree.selection()
        if selection:
            pokemon_id = self.pokemon_tree.item(selection[0])['values'][0]
            bot_name = self.selected_bot_var.get()
            if bot_name:
                self.integration.toggle_pokemon_favorite(bot_name, pokemon_id)
                self.refresh_pokemon()
    
    def rename_pokemon(self):
        """Rename selected Pokemon"""
        selection = self.pokemon_tree.selection()
        if selection:
            pokemon_id = self.pokemon_tree.item(selection[0])['values'][0]
            bot_name = self.selected_bot_var.get()
            if bot_name:
                new_name = simpledialog.askstring("Rename Pokemon", "Enter new name:")
                if new_name:
                    self.integration.rename_pokemon(bot_name, pokemon_id, new_name)
                    self.refresh_pokemon()
    
    def transfer_duplicates(self):
        """Transfer all duplicate Pokemon"""
        bot_name = self.selected_bot_var.get()
        if not bot_name:
            self.update_status("❌ No bot selected")
            return
        
        def transfer_thread():
            pokemon_data = self.integration.get_pokemons(bot_name)
            if 'pokemons' in pokemon_data:
                # Group Pokemon by name and keep only the best one
                pokemon_groups = {}
                for pokemon in pokemon_data['pokemons']:
                    name = pokemon.get('name', '')
                    if name not in pokemon_groups:
                        pokemon_groups[name] = []
                    pokemon_groups[name].append(pokemon)
                
                # Transfer duplicates (keep highest CP)
                for name, pokemon_list in pokemon_groups.items():
                    if len(pokemon_list) > 1:
                        # Sort by CP (highest first)
                        pokemon_list.sort(key=lambda x: x.get('cp', 0), reverse=True)
                        # Transfer all except the first (highest CP)
                        for pokemon in pokemon_list[1:]:
                            self.integration.transfer_pokemon(bot_name, pokemon.get('id', ''))
                
                self.parent.after(0, self.refresh_pokemon)
        
        threading.Thread(target=transfer_thread, daemon=True).start()
    
    # Item Management Methods
    def on_item_bot_selected(self, event=None):
        """Handle bot selection for item management"""
        bot_name = self.selected_item_bot_var.get()
        if bot_name:
            self.refresh_items()
    
    def refresh_items(self):
        """Refresh item list for selected bot"""
        bot_name = self.selected_item_bot_var.get()
        if not bot_name:
            self.update_status("❌ No bot selected")
            return
        
        def refresh_thread():
            item_data = self.integration.get_items(bot_name)
            self.parent.after(0, self._update_item_display, item_data)
        
        threading.Thread(target=refresh_thread, daemon=True).start()
    
    def _update_item_display(self, item_data):
        """Update item display"""
        # Clear existing items
        for item in self.item_tree.get_children():
            self.item_tree.delete(item)
        
        # Add item data
        if 'items' in item_data:
            for item in item_data['items']:
                values = (
                    item.get('id', ''),
                    item.get('name', ''),
                    item.get('count', 0),
                    'Actions'
                )
                self.item_tree.insert('', tk.END, values=values)
    
    def drop_selected_item(self):
        """Drop selected item"""
        selection = self.item_tree.selection()
        if selection:
            item_id = self.item_tree.item(selection[0])['values'][0]
            bot_name = self.selected_item_bot_var.get()
            if bot_name:
                quantity = simpledialog.askinteger("Drop Item", "Enter quantity to drop:")
                if quantity and quantity > 0:
                    self.integration.drop_item(bot_name, item_id, quantity)
                    self.refresh_items()
    
    def use_incense(self):
        """Use incense for selected bot"""
        bot_name = self.selected_item_bot_var.get()
        if bot_name:
            self.integration.use_incense(bot_name)
    
    def use_lucky_egg(self):
        """Use lucky egg for selected bot"""
        bot_name = self.selected_item_bot_var.get()
        if bot_name:
            self.integration.use_lucky_egg(bot_name)
    
    def force_catch_selected_pokemon(self):
        """Force catch the selected Pokemon"""
        if not self.thunderbolt_bot:
            self.update_status("❌ Thunderbolt bot not available")
            return
        
        # Get selected Pokemon from the tree
        selection = self.pokemon_tree.selection()
        if not selection:
            self.update_status("❌ Please select a Pokemon to catch")
            return
        
        # Get Pokemon data from the selected item
        item = self.pokemon_tree.item(selection[0])
        values = item['values']
        
        if len(values) < 6:
            self.update_status("❌ Invalid Pokemon data")
            return
        
        pokemon_name = values[1]  # Name
        cp = int(values[2]) if values[2].isdigit() else 0  # CP
        iv = int(values[3]) if values[3].isdigit() else 0  # IV
        pokemon_id = f"{pokemon_name.lower()}_{hash(pokemon_name) % 1000:03d}"
        
        def catch_thread():
            try:
                self.update_status(f"🎯 FORCE CATCHING: {pokemon_name} (CP: {cp}, IV: {iv})")
                
                # Force catch the Pokemon
                success = self.thunderbolt_bot.force_catch_pokemon(pokemon_id, pokemon_name, cp, iv)
                
                if success:
                    self.update_status(f"✅ SUCCESSFULLY CAUGHT: {pokemon_name}!")
                    # Refresh Pokemon list to show the new catch
                    self.refresh_pokemon()
                else:
                    self.update_status(f"❌ FAILED TO CATCH: {pokemon_name}")
                    
            except Exception as e:
                self.update_status(f"❌ Error force catching Pokemon: {e}")
        
        threading.Thread(target=catch_thread, daemon=True).start()
    
    # Main Bot Control Methods
    def start_main_bot(self):
        """Start the main Pokemon Go bot"""
        if not self.thunderbolt_bot:
            self.update_status("❌ Thunderbolt bot not available")
            return
        
        def start_thread():
            try:
                # Set credentials
                self.thunderbolt_bot.set_credentials(
                    self.username_var.get(),
                    self.password_var.get(),
                    self.auth_type_var.get()
                )
                
                # Set location
                lat = float(self.lat_var.get())
                lng = float(self.lng_var.get())
                alt = float(self.alt_var.get())
                self.thunderbolt_bot.set_location(lat, lng, alt)
                
                # Apply settings
                self.apply_bot_settings()
                
                # Start bot
                if self.thunderbolt_bot.start_bot(self.bot_mode_var.get()):
                    self.is_running = True
                    self.stats['start_time'] = datetime.now()
                    self.update_status("✅ Bot started successfully")
                    self._update_bot_status("Online", "green")
                else:
                    self.update_status("❌ Failed to start bot")
                    
            except Exception as e:
                self.update_status(f"❌ Error starting bot: {e}")
        
        threading.Thread(target=start_thread, daemon=True).start()
    
    def stop_main_bot(self):
        """Stop the main Pokemon Go bot"""
        if not self.thunderbolt_bot:
            self.update_status("❌ Thunderbolt bot not available")
            return
        
        def stop_thread():
            try:
                if self.thunderbolt_bot.stop_bot():
                    self.is_running = False
                    self.update_status("✅ Bot stopped successfully")
                    self._update_bot_status("Offline", "red")
                else:
                    self.update_status("❌ Failed to stop bot")
                    
            except Exception as e:
                self.update_status(f"❌ Error stopping bot: {e}")
        
        threading.Thread(target=stop_thread, daemon=True).start()
    
    def restart_main_bot(self):
        """Restart the main Pokemon Go bot"""
        self.update_status("🔄 Restarting bot...")
        self.stop_main_bot()
        time.sleep(2)
        self.start_main_bot()
    
    def apply_bot_settings(self):
        """Apply bot settings"""
        if not self.thunderbolt_bot:
            return
        
        try:
            # Set walk speed
            walk_speed = float(self.walk_speed_var.get())
            self.thunderbolt_bot.set_walk_speed(walk_speed)
            
            # Set catch settings
            self.thunderbolt_bot.set_catch_pokemon(self.catch_pokemon_var.get())
            self.thunderbolt_bot.set_spin_pokestops(self.spin_pokestops_var.get())
            self.thunderbolt_bot.set_battle_gyms(self.battle_gyms_var.get())
            
            # Set min CP threshold
            min_cp = int(self.min_cp_var.get())
            self.thunderbolt_bot.set_min_cp_threshold(min_cp)
            
            self.update_status("✅ Bot settings applied")
            
        except Exception as e:
            self.update_status(f"❌ Error applying settings: {e}")
    
    def change_bot_mode(self):
        """Change bot mode"""
        if not self.thunderbolt_bot or not self.is_running:
            self.update_status("❌ Bot not running")
            return
        
        try:
            new_mode = self.bot_mode_var.get()
            if self.thunderbolt_bot.set_mode(new_mode):
                self.update_status(f"✅ Bot mode changed to: {new_mode}")
            else:
                self.update_status(f"❌ Failed to change mode to: {new_mode}")
                
        except Exception as e:
            self.update_status(f"❌ Error changing mode: {e}")
    
    # Location Methods
    def set_bot_location(self):
        """Set bot location"""
        try:
            lat = float(self.lat_var.get())
            lng = float(self.lng_var.get())
            alt = float(self.alt_var.get())
            
            if self.thunderbolt_bot:
                self.thunderbolt_bot.set_location(lat, lng, alt)
                self.update_status(f"✅ Location set to: {lat}, {lng}, {alt}")
                self.location_label.config(text=f"{lat:.4f}, {lng:.4f}")
            else:
                self.update_status("❌ Thunderbolt bot not available")
                
        except ValueError:
            self.update_status("❌ Invalid location coordinates")
        except Exception as e:
            self.update_status(f"❌ Error setting location: {e}")
    
    def get_current_location(self):
        """Get current location from bot"""
        if not self.thunderbolt_bot:
            self.update_status("❌ Thunderbolt bot not available")
            return
        
        try:
            location_info = self.thunderbolt_bot.get_location_info()
            if 'lat' in location_info and 'lng' in location_info:
                lat = location_info['lat']
                lng = location_info['lng']
                alt = location_info.get('alt', 10)
                
                self.lat_var.set(str(lat))
                self.lng_var.set(str(lng))
                self.alt_var.set(str(alt))
                
                self.update_status(f"✅ Current location: {lat}, {lng}, {alt}")
                self.location_label.config(text=f"{lat:.4f}, {lng:.4f}")
            else:
                self.update_status("❌ No location data available")
                
        except Exception as e:
            self.update_status(f"❌ Error getting location: {e}")
    
    def set_random_location(self):
        """Set random location"""
        import random
        
        # Random location around NYC area
        lat = round(random.uniform(40.7, 40.8), 4)
        lng = round(random.uniform(-74.0, -73.9), 4)
        alt = random.randint(5, 50)
        
        self.lat_var.set(str(lat))
        self.lng_var.set(str(lng))
        self.alt_var.set(str(alt))
        
        self.update_status(f"✅ Random location set: {lat}, {lng}, {alt}")
    
    # Map Integration Methods
    def open_pokemon_map(self):
        """Open Pokemon map in browser"""
        if not self.thunderbolt_bot:
            self.update_status("❌ Thunderbolt bot not available")
            return
        
        try:
            if self.thunderbolt_bot.open_pokemon_map():
                self.update_status("✅ Pokemon map opened in browser")
            else:
                self.update_status("❌ Failed to open Pokemon map")
        except Exception as e:
            self.update_status(f"❌ Error opening map: {e}")
    
    def refresh_map_data(self):
        """Refresh map data"""
        if not self.thunderbolt_bot:
            self.update_status("❌ Thunderbolt bot not available")
            return
        
        def refresh_thread():
            try:
                map_data = self.thunderbolt_bot.get_map_data()
                self.parent.after(0, self._update_map_display, map_data)
            except Exception as e:
                self.update_status(f"❌ Error refreshing map data: {e}")
        
        threading.Thread(target=refresh_thread, daemon=True).start()
    
    def set_current_location(self):
        """Set current location from map"""
        self.get_current_location()
        self.refresh_map_data()
    
    def find_rare_pokemon(self):
        """Find rare Pokemon nearby"""
        if not self.thunderbolt_bot:
            self.update_status("❌ Thunderbolt bot not available")
            return
        
        def find_thread():
            try:
                rare_pokemon = self.thunderbolt_bot.find_rare_pokemon(2.0)  # 2km radius
                if rare_pokemon:
                    self.update_status(f"✅ Found {len(rare_pokemon)} rare Pokemon nearby")
                    for pokemon in rare_pokemon[:3]:  # Show first 3
                        self.update_status(f"  - {pokemon['name']} (CP: {pokemon['cp']}, IV: {pokemon['iv']})")
                else:
                    self.update_status("❌ No rare Pokemon found nearby")
            except Exception as e:
                self.update_status(f"❌ Error finding rare Pokemon: {e}")
        
        threading.Thread(target=find_thread, daemon=True).start()
    
    def search_location(self):
        """Search for location"""
        search_term = self.location_search_var.get().strip()
        if not search_term:
            self.update_status("❌ Please enter a location to search")
            return
        
        self.update_status(f"🔍 Searching for: {search_term}")
        # TODO: Implement location search
        self.update_status("❌ Location search not implemented yet")
    
    # Display Update Methods
    def _update_bot_status(self, status, color):
        """Update bot status display"""
        self.bot_status_label.config(text=status, foreground=color)
        self.status_indicator.config(text=f"● {status.upper()}", foreground=color)
    
    def _update_map_display(self, map_data):
        """Update map data display"""
        try:
            # Update Pokemon list
            for item in self.map_pokemon_tree.get_children():
                self.map_pokemon_tree.delete(item)
            
            pokemon_spawns = map_data.get('pokemon_spawns', [])
            for pokemon in pokemon_spawns[:20]:  # Show first 20
                values = (
                    pokemon.get('name', ''),
                    pokemon.get('cp', 0),
                    pokemon.get('iv', 0),
                    f"{pokemon.get('distance_km', 0):.2f}km",
                    pokemon.get('time_left', 'Unknown'),
                    'Actions'
                )
                self.map_pokemon_tree.insert('', tk.END, values=values)
            
            # Update Pokestops list
            for item in self.map_pokestops_tree.get_children():
                self.map_pokestops_tree.delete(item)
            
            pokestops = map_data.get('pokestops', [])
            for stop in pokestops[:20]:  # Show first 20
                values = (
                    stop.get('name', ''),
                    stop.get('lure_type', 'None'),
                    f"{stop.get('distance_km', 0):.2f}km",
                    'Actions'
                )
                self.map_pokestops_tree.insert('', tk.END, values=values)
            
            # Update Gyms list
            for item in self.map_gyms_tree.get_children():
                self.map_gyms_tree.delete(item)
            
            gyms = map_data.get('gyms', [])
            for gym in gyms[:20]:  # Show first 20
                values = (
                    gym.get('name', ''),
                    gym.get('team', ''),
                    gym.get('level', 0),
                    gym.get('raid_boss', 'None'),
                    f"{gym.get('distance_km', 0):.2f}km",
                    'Actions'
                )
                self.map_gyms_tree.insert('', tk.END, values=values)
            
            # Update map info labels
            self.nearby_pokemon_label.config(text=str(len(pokemon_spawns)))
            self.nearby_pokestops_label.config(text=str(len(pokestops)))
            self.nearby_gyms_label.config(text=str(len(gyms)))
            
        except Exception as e:
            self.update_status(f"❌ Error updating map display: {e}")
    
    # Activity Log Methods
    def clear_activity_log(self):
        """Clear activity log"""
        self.activity_log.delete(1.0, tk.END)
    
    def save_activity_log(self):
        """Save activity log to file"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.activity_log.get(1.0, tk.END))
                self.update_status(f"✅ Activity log saved to: {filename}")
        except Exception as e:
            self.update_status(f"❌ Error saving log: {e}")
    
    # Status Update Methods
    def start_all_bots(self):
        """Start all bots"""
        self.start_main_bot()
    
    def stop_all_bots(self):
        """Stop all bots"""
        self.stop_main_bot()
    
    def refresh_all_status(self):
        """Refresh all status displays"""
        self.refresh_map_data()
        self._update_quick_stats()
    
    def _update_quick_stats(self):
        """Update quick stats display"""
        try:
            if self.thunderbolt_bot:
                stats = self.thunderbolt_bot.get_statistics()
                for var_name, var in self.quick_stats_vars.items():
                    if var_name in stats:
                        var.set(str(stats[var_name]))
        except Exception as e:
            self.update_status(f"❌ Error updating stats: {e}")
    
    def _status_update_loop(self):
        """Status update loop"""
        while True:
            try:
                # Update uptime
                if self.is_running and self.stats['start_time']:
                    uptime = datetime.now() - self.stats['start_time']
                    uptime_str = str(uptime).split('.')[0]
                    self.uptime_label.config(text=uptime_str)
                
                # Update quick stats
                self._update_quick_stats()
                
                # Update map data every 30 seconds
                if self.is_running and hasattr(self, '_last_map_update'):
                    if time.time() - self._last_map_update > 30:
                        self.refresh_map_data()
                        self._last_map_update = time.time()
                elif self.is_running:
                    self._last_map_update = time.time()
                
                time.sleep(5)  # Update every 5 seconds
                
            except Exception as e:
                self.update_status(f"Status update error: {e}")
                time.sleep(10)

class BotAddDialog:
    """Dialog for adding a new bot"""
    
    def __init__(self, parent, integration):
        self.integration = integration
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add New Bot")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        
        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Create form
        self.create_form()
        
        # Center dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        # Wait for dialog to close
        self.dialog.wait_window()
    
    def create_form(self):
        """Create the form"""
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Bot name
        ttk.Label(main_frame, text="Bot Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.bot_name_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.bot_name_var, width=30).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Username
        ttk.Label(main_frame, text="Username:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.username_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.username_var, width=30).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Password
        ttk.Label(main_frame, text="Password:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.password_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.password_var, show="*", width=30).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Auth type
        ttk.Label(main_frame, text="Auth Type:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.auth_type_var = tk.StringVar(value="PTC")
        auth_combo = ttk.Combobox(main_frame, textvariable=self.auth_type_var, values=["PTC", "Google"], width=27)
        auth_combo.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Location
        ttk.Label(main_frame, text="Location (Lat, Lng):").grid(row=4, column=0, sticky=tk.W, pady=5)
        location_frame = ttk.Frame(main_frame)
        location_frame.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        self.lat_var = tk.StringVar(value="40.7589")
        self.lng_var = tk.StringVar(value="-73.9851")
        ttk.Entry(location_frame, textvariable=self.lat_var, width=12).pack(side=tk.LEFT)
        ttk.Label(location_frame, text=", ").pack(side=tk.LEFT)
        ttk.Entry(location_frame, textvariable=self.lng_var, width=12).pack(side=tk.LEFT)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Add Bot", command=self.add_bot).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side=tk.LEFT)
    
    def add_bot(self):
        """Add the bot"""
        try:
            bot_name = self.bot_name_var.get().strip()
            if not bot_name:
                messagebox.showerror("Error", "Bot name is required")
                return
            
            config = {
                'credentials': {
                    'username': self.username_var.get().strip(),
                    'password': self.password_var.get().strip(),
                    'auth_type': self.auth_type_var.get()
                },
                'location': {
                    'lat': float(self.lat_var.get()),
                    'lng': float(self.lng_var.get()),
                    'alt': 10
                }
            }
            
            if self.integration.register_bot(bot_name, config):
                self.result = True
                self.dialog.destroy()
            else:
                messagebox.showerror("Error", "Failed to add bot")
        except ValueError:
            messagebox.showerror("Error", "Invalid location coordinates")
        except Exception as e:
            messagebox.showerror("Error", f"Error adding bot: {e}")
    
    def cancel(self):
        """Cancel dialog"""
        self.dialog.destroy()

class BotConfigDialog:
    """Dialog for configuring a bot"""
    
    def __init__(self, parent, integration, bot_name):
        self.integration = integration
        self.bot_name = bot_name
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"Configure Bot: {bot_name}")
        self.dialog.geometry("500x400")
        self.dialog.resizable(True, True)
        
        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Create form
        self.create_form()
        
        # Center dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
    
    def create_form(self):
        """Create the configuration form"""
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configuration text area
        ttk.Label(main_frame, text="Bot Configuration (JSON):").pack(anchor=tk.W)
        
        self.config_text = scrolledtext.ScrolledText(main_frame, height=15, width=60)
        self.config_text.pack(fill=tk.BOTH, expand=True, pady=(5, 10))
        
        # Load current configuration
        self.load_current_config()
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Save", command=self.save_config).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.LEFT)
    
    def load_current_config(self):
        """Load current bot configuration"""
        try:
            # Get bot data
            bot_data = self.integration.get_bot_data(self.bot_name)
            if 'error' not in bot_data:
                config_json = json.dumps(bot_data, indent=2)
                self.config_text.insert(tk.END, config_json)
        except Exception as e:
            self.config_text.insert(tk.END, f"Error loading configuration: {e}")
    
    def save_config(self):
        """Save bot configuration"""
        try:
            config_text = self.config_text.get(1.0, tk.END).strip()
            config = json.loads(config_text)
            
            if self.integration.update_bot_config(self.bot_name, config):
                messagebox.showinfo("Success", "Configuration saved")
                self.dialog.destroy()
            else:
                messagebox.showerror("Error", "Failed to save configuration")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON format")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving configuration: {e}")

class BotDetailsDialog:
    """Dialog for viewing bot details"""
    
    def __init__(self, parent, integration, bot_name):
        self.integration = integration
        self.bot_name = bot_name
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"Bot Details: {bot_name}")
        self.dialog.geometry("600x500")
        self.dialog.resizable(True, True)
        
        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Create details display
        self.create_details_display()
        
        # Center dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
    
    def create_details_display(self):
        """Create the details display"""
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Details text area
        self.details_text = scrolledtext.ScrolledText(main_frame, height=25, width=70)
        self.details_text.pack(fill=tk.BOTH, expand=True)
        
        # Load bot details
        self.load_bot_details()
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="Refresh", command=self.load_bot_details).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Close", command=self.dialog.destroy).pack(side=tk.LEFT)
    
    def load_bot_details(self):
        """Load bot details"""
        try:
            # Clear text
            self.details_text.delete(1.0, tk.END)
            
            # Get bot status
            status = self.integration.get_bot_status(self.bot_name)
            
            # Get bot data
            data = self.integration.get_bot_data(self.bot_name)
            
            # Format details
            details = f"Bot Name: {self.bot_name}\n"
            details += f"Status: {status.get('status', 'Unknown')}\n"
            details += f"Last Update: {status.get('last_update', 'Never')}\n\n"
            
            details += "Status Information:\n"
            details += json.dumps(status, indent=2)
            details += "\n\n"
            
            details += "Bot Data:\n"
            details += json.dumps(data, indent=2)
            
            self.details_text.insert(tk.END, details)
        except Exception as e:
            self.details_text.insert(tk.END, f"Error loading details: {e}")

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Pokemon Go Bot GUI Integration Test")
    root.geometry("800x600")
    
    # Create Pokemon Go Bot tab
    pokemon_tab = PokemonGoBotGUITab(root)
    
    root.mainloop()
