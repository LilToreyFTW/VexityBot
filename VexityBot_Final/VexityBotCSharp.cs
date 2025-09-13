using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.IO;
using System.Security.Cryptography;
using System.Configuration;
using System.Data.SqlClient;
using System.Timers;
using System.Diagnostics;
using System.Management;
using System.Runtime.InteropServices;

namespace VexityBotCSharp
{
    /// <summary>
    /// VexityBot C# Main Application
    /// Advanced Bot Management System with Full GUI and Database Integration
    /// </summary>
    public partial class VexityBotMainForm : Form
    {
        #region Private Fields
        private BotManager botManager;
        private NetworkManager networkManager;
        private DatabaseManager dbManager;
        private Logger logger;
        private System.Timers.Timer statusTimer;
        private System.Timers.Timer attackTimer;
        private bool isAttacking = false;
        private List<Bot> bots;
        private AttackTarget currentTarget;
        private Random random = new Random();
        #endregion

        #region Constructor
        public VexityBotMainForm()
        {
            InitializeComponent();
            InitializeApplication();
        }
        #endregion

        #region Initialization
        private void InitializeApplication()
        {
            // Initialize managers
            botManager = new BotManager();
            networkManager = new NetworkManager();
            dbManager = new DatabaseManager();
            logger = new Logger("VexityBot.log");

            // Initialize bots
            InitializeBots();

            // Setup timers
            SetupTimers();

            // Load configuration
            LoadConfiguration();

            // Update UI
            UpdateBotStatus();
            UpdateNetworkStatus();

            logger.Log("VexityBot C# Application initialized successfully", LogLevel.Info);
        }

        private void InitializeBots()
        {
            bots = new List<Bot>
            {
                new Bot("AlphaBot", "Nuclear Warfare", 8081, AttackType.NuclearWarfare),
                new Bot("BetaBot", "Cyber Warfare", 8082, AttackType.CyberWarfare),
                new Bot("GammaBot", "Stealth Operations", 8083, AttackType.StealthOps),
                new Bot("DeltaBot", "EMP Warfare", 8084, AttackType.EmpWarfare),
                new Bot("EpsilonBot", "Biological Warfare", 8085, AttackType.BioWarfare),
                new Bot("ZetaBot", "Gravity Control", 8086, AttackType.GravityControl),
                new Bot("EtaBot", "Thermal Annihilation", 8087, AttackType.ThermalAnnihilation),
                new Bot("ThetaBot", "Cryogenic Freeze", 8088, AttackType.CryogenicFreeze),
                new Bot("IotaBot", "Quantum Entanglement", 8089, AttackType.QuantumEntanglement),
                new Bot("KappaBot", "Dimensional Portal", 8090, AttackType.DimensionalPortal),
                new Bot("LambdaBot", "Neural Network", 8091, AttackType.NeuralNetwork),
                new Bot("MuBot", "Molecular Disassembly", 8092, AttackType.MolecularDisassembly),
                new Bot("NuBot", "Sound Wave Devastation", 8093, AttackType.SoundWaveDevastation),
                new Bot("XiBot", "Light Manipulation", 8094, AttackType.LightManipulation),
                new Bot("OmicronBot", "Dark Matter Control", 8095, AttackType.DarkMatterControl),
                new Bot("PiBot", "Mathematical Chaos", 8096, AttackType.MathematicalChaos),
                new Bot("RhoBot", "Chemical Reactions", 8097, AttackType.ChemicalReactions),
                new Bot("SigmaBot", "Magnetic Fields", 8098, AttackType.MagneticFields),
                new Bot("TauBot", "Time Manipulation", 8099, AttackType.TimeManipulation),
                new Bot("UpsilonBot", "Space-Time Fabric", 8100, AttackType.SpaceTimeFabric),
                new Bot("PhiBot", "Consciousness Control", 8101, AttackType.ConsciousnessControl),
                new Bot("ChiBot", "Energy Vortex", 8102, AttackType.EnergyVortex),
                new Bot("PsiBot", "Psychic Warfare", 8103, AttackType.PsychicWarfare)
            };

            botManager.InitializeBots(bots);
        }

        private void SetupTimers()
        {
            // Status update timer (every 1 second)
            statusTimer = new System.Timers.Timer(1000);
            statusTimer.Elapsed += StatusTimer_Elapsed;
            statusTimer.AutoReset = true;
            statusTimer.Enabled = true;

            // Attack progress timer (every 100ms during attacks)
            attackTimer = new System.Timers.Timer(100);
            attackTimer.Elapsed += AttackTimer_Elapsed;
            attackTimer.AutoReset = true;
            attackTimer.Enabled = false;
        }

        private void LoadConfiguration()
        {
            try
            {
                // Load from app.config or settings file
                string vpsIp = ConfigurationManager.AppSettings["VPS_IP"] ?? "191.96.152.162";
                int vpsPort = int.Parse(ConfigurationManager.AppSettings["VPS_PORT"] ?? "8080");
                
                networkManager.SetVpsEndpoint(vpsIp, vpsPort);
                logger.Log($"Configuration loaded - VPS: {vpsIp}:{vpsPort}", LogLevel.Info);
            }
            catch (Exception ex)
            {
                logger.Log($"Error loading configuration: {ex.Message}", LogLevel.Error);
            }
        }
        #endregion

        #region Event Handlers
        private void StatusTimer_Elapsed(object sender, ElapsedEventArgs e)
        {
            if (InvokeRequired)
            {
                Invoke(new Action(() => UpdateBotStatus()));
            }
            else
            {
                UpdateBotStatus();
            }
        }

        private void AttackTimer_Elapsed(object sender, ElapsedEventArgs e)
        {
            if (InvokeRequired)
            {
                Invoke(new Action(() => UpdateAttackProgress()));
            }
            else
            {
                UpdateAttackProgress();
            }
        }

        private void btnStartAll_Click(object sender, EventArgs e)
        {
            logger.Log("Starting all bots...", LogLevel.Info);
            
            Task.Run(() =>
            {
                bool success = botManager.StartAllBots();
                
                if (InvokeRequired)
                {
                    Invoke(new Action(() =>
                    {
                        if (success)
                        {
                            MessageBox.Show("All bots started successfully!", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                            UpdateBotStatus();
                        }
                        else
                        {
                            MessageBox.Show("Failed to start some bots!", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        }
                    }));
                }
            });
        }

        private void btnStopAll_Click(object sender, EventArgs e)
        {
            logger.Log("Stopping all bots...", LogLevel.Info);
            
            Task.Run(() =>
            {
                bool success = botManager.StopAllBots();
                
                if (InvokeRequired)
                {
                    Invoke(new Action(() =>
                    {
                        if (success)
                        {
                            MessageBox.Show("All bots stopped successfully!", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                            UpdateBotStatus();
                        }
                        else
                        {
                            MessageBox.Show("Failed to stop some bots!", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        }
                    }));
                }
            });
        }

        private void btnLaunchAttack_Click(object sender, EventArgs e)
        {
            if (isAttacking)
            {
                StopAttack();
            }
            else
            {
                LaunchAttack();
            }
        }

        private void btnEmergencyStop_Click(object sender, EventArgs e)
        {
            logger.Log("EMERGENCY STOP activated!", LogLevel.Warning);
            
            Task.Run(() =>
            {
                botManager.EmergencyStopAll();
                
                if (InvokeRequired)
                {
                    Invoke(new Action(() =>
                    {
                        isAttacking = false;
                        attackTimer.Enabled = false;
                        btnLaunchAttack.Text = "🚀 Launch Attack";
                        btnLaunchAttack.BackColor = Color.FromArgb(231, 76, 60);
                        progressBarAttack.Value = 0;
                        lblAttackStatus.Text = "Attack Status: Stopped";
                        UpdateBotStatus();
                        
                        MessageBox.Show("EMERGENCY STOP executed! All bots halted immediately!", "Emergency Stop", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                    }));
                }
            });
        }

        private void btnRefresh_Click(object sender, EventArgs e)
        {
            UpdateBotStatus();
            UpdateNetworkStatus();
            logger.Log("Status refreshed", LogLevel.Info);
        }

        private void btnBotAdmin_Click(object sender, EventArgs e)
        {
            if (dgvBots.SelectedRows.Count > 0)
            {
                var selectedBot = dgvBots.SelectedRows[0].DataBoundItem as Bot;
                if (selectedBot != null)
                {
                    OpenBotAdminPanel(selectedBot);
                }
            }
            else
            {
                MessageBox.Show("Please select a bot first!", "No Selection", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
        }

        private void dgvBots_CellDoubleClick(object sender, DataGridViewCellEventArgs e)
        {
            if (e.RowIndex >= 0)
            {
                var bot = dgvBots.Rows[e.RowIndex].DataBoundItem as Bot;
                if (bot != null)
                {
                    OpenBotAdminPanel(bot);
                }
            }
        }

        private void btnNetworkScan_Click(object sender, EventArgs e)
        {
            Task.Run(() =>
            {
                logger.Log("Starting network scan...", LogLevel.Info);
                
                var scanResults = networkManager.ScanNetwork();
                
                if (InvokeRequired)
                {
                    Invoke(new Action(() =>
                    {
                        DisplayNetworkScanResults(scanResults);
                    }));
                }
            });
        }

        private void btnDatabaseBackup_Click(object sender, EventArgs e)
        {
            Task.Run(() =>
            {
                try
                {
                    string backupPath = dbManager.BackupDatabase();
                    
                    if (InvokeRequired)
                    {
                        Invoke(new Action(() =>
                        {
                            MessageBox.Show($"Database backed up to: {backupPath}", "Backup Complete", MessageBoxButtons.OK, MessageBoxIcon.Information);
                        }));
                    }
                }
                catch (Exception ex)
                {
                    if (InvokeRequired)
                    {
                        Invoke(new Action(() =>
                        {
                            MessageBox.Show($"Backup failed: {ex.Message}", "Backup Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        }));
                    }
                }
            });
        }
        #endregion

        #region Attack Methods
        private void LaunchAttack()
        {
            string targetIp = txtTargetIP.Text.Trim();
            int targetPort = int.Parse(txtTargetPort.Text);
            int intensity = (int)nudIntensity.Value;
            AttackType attackType = (AttackType)cmbAttackType.SelectedValue;

            if (string.IsNullOrEmpty(targetIp))
            {
                MessageBox.Show("Please enter a target IP address!", "Invalid Input", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            currentTarget = new AttackTarget
            {
                IP = targetIp,
                Port = targetPort,
                AttackType = attackType,
                Intensity = intensity,
                Duration = 60 // 60 seconds default
            };

            logger.Log($"Launching coordinated attack against {targetIp}:{targetPort} with intensity {intensity}", LogLevel.Info);

            Task.Run(() =>
            {
                isAttacking = true;
                attackTimer.Enabled = true;

                if (InvokeRequired)
                {
                    Invoke(new Action(() =>
                    {
                        btnLaunchAttack.Text = "⏹️ Stop Attack";
                        btnLaunchAttack.BackColor = Color.FromArgb(52, 73, 94);
                        lblAttackStatus.Text = $"Attack Status: Attacking {targetIp}:{targetPort}";
                    }));
                }

                bool success = botManager.LaunchCoordinatedAttack(currentTarget);

                if (InvokeRequired)
                {
                    Invoke(new Action(() =>
                    {
                        isAttacking = false;
                        attackTimer.Enabled = false;
                        btnLaunchAttack.Text = "🚀 Launch Attack";
                        btnLaunchAttack.BackColor = Color.FromArgb(231, 76, 60);
                        progressBarAttack.Value = 100;
                        lblAttackStatus.Text = success ? "Attack Status: Completed Successfully" : "Attack Status: Failed";
                    }));
                }

                logger.Log($"Attack completed - Success: {success}", LogLevel.Info);
            });
        }

        private void StopAttack()
        {
            logger.Log("Stopping attack...", LogLevel.Info);
            
            Task.Run(() =>
            {
                botManager.StopAllAttacks();
                
                if (InvokeRequired)
                {
                    Invoke(new Action(() =>
                    {
                        isAttacking = false;
                        attackTimer.Enabled = false;
                        btnLaunchAttack.Text = "🚀 Launch Attack";
                        btnLaunchAttack.BackColor = Color.FromArgb(231, 76, 60);
                        progressBarAttack.Value = 0;
                        lblAttackStatus.Text = "Attack Status: Stopped";
                    }));
                }
            });
        }

        private void UpdateAttackProgress()
        {
            if (isAttacking && progressBarAttack.Value < 100)
            {
                progressBarAttack.Value = Math.Min(100, progressBarAttack.Value + 1);
            }
        }
        #endregion

        #region UI Update Methods
        private void UpdateBotStatus()
        {
            try
            {
                // Update bot data grid
                dgvBots.DataSource = null;
                dgvBots.DataSource = bots;

                // Update statistics
                int onlineCount = bots.Count(b => b.Status == BotStatus.Online);
                int offlineCount = bots.Count(b => b.Status == BotStatus.Offline);
                int attackingCount = bots.Count(b => b.Status == BotStatus.Attacking);

                lblOnlineBots.Text = $"Online: {onlineCount}";
                lblOfflineBots.Text = $"Offline: {offlineCount}";
                lblAttackingBots.Text = $"Attacking: {attackingCount}";

                // Update network status
                UpdateNetworkStatus();
            }
            catch (Exception ex)
            {
                logger.Log($"Error updating bot status: {ex.Message}", LogLevel.Error);
            }
        }

        private void UpdateNetworkStatus()
        {
            try
            {
                var networkInfo = networkManager.GetNetworkStatus();
                
                lblNetworkStatus.Text = $"Network: {networkInfo.Status}";
                lblBandwidth.Text = $"Bandwidth: {networkInfo.Bandwidth}";
                lblLatency.Text = $"Latency: {networkInfo.Latency}ms";
                lblConnections.Text = $"Connections: {networkInfo.ActiveConnections}";
            }
            catch (Exception ex)
            {
                logger.Log($"Error updating network status: {ex.Message}", LogLevel.Error);
            }
        }

        private void DisplayNetworkScanResults(List<NetworkHost> hosts)
        {
            var form = new NetworkScanResultsForm(hosts);
            form.ShowDialog();
        }
        #endregion

        #region Bot Admin Panel
        private void OpenBotAdminPanel(Bot bot)
        {
            var adminForm = new BotAdminForm(bot, botManager, logger);
            adminForm.ShowDialog();
        }
        #endregion

        #region Form Events
        protected override void OnFormClosing(FormClosingEventArgs e)
        {
            if (isAttacking)
            {
                var result = MessageBox.Show("Attack is in progress. Are you sure you want to exit?", "Confirm Exit", MessageBoxButtons.YesNo, MessageBoxIcon.Question);
                if (result == DialogResult.No)
                {
                    e.Cancel = true;
                    return;
                }
            }

            // Cleanup
            statusTimer?.Stop();
            attackTimer?.Stop();
            botManager?.ShutdownAll();
            logger?.Log("Application shutting down", LogLevel.Info);

            base.OnFormClosing(e);
        }
        #endregion
    }

    #region Bot Classes
    public class Bot
    {
        public string Name { get; set; }
        public string Specialty { get; set; }
        public int Port { get; set; }
        public AttackType PrimaryWeapon { get; set; }
        public BotStatus Status { get; set; }
        public int TotalRequests { get; set; }
        public int SuccessfulRequests { get; set; }
        public int FailedRequests { get; set; }
        public double UptimePercentage { get; set; }
        public DateTime LastActivity { get; set; }
        public bool IsAttacking { get; set; }
        public string CurrentTarget { get; set; }

        public Bot(string name, string specialty, int port, AttackType primaryWeapon)
        {
            Name = name;
            Specialty = specialty;
            Port = port;
            PrimaryWeapon = primaryWeapon;
            Status = BotStatus.Offline;
            TotalRequests = 0;
            SuccessfulRequests = 0;
            FailedRequests = 0;
            UptimePercentage = 0.0;
            LastActivity = DateTime.Now;
            IsAttacking = false;
            CurrentTarget = "";
        }
    }

    public enum BotStatus
    {
        Offline,
        Online,
        Maintenance,
        Attacking,
        Error
    }

    public enum AttackType
    {
        DDoS,
        PortScan,
        VulnerabilityScan,
        BruteForce,
        Custom,
        NuclearWarfare,
        CyberWarfare,
        StealthOps,
        EmpWarfare,
        BioWarfare,
        GravityControl,
        ThermalAnnihilation,
        CryogenicFreeze,
        QuantumEntanglement,
        DimensionalPortal,
        NeuralNetwork,
        MolecularDisassembly,
        SoundWaveDevastation,
        LightManipulation,
        DarkMatterControl,
        MathematicalChaos,
        ChemicalReactions,
        MagneticFields,
        TimeManipulation,
        SpaceTimeFabric,
        ConsciousnessControl,
        EnergyVortex,
        PsychicWarfare
    }

    public class AttackTarget
    {
        public string IP { get; set; }
        public int Port { get; set; }
        public AttackType AttackType { get; set; }
        public int Intensity { get; set; }
        public int Duration { get; set; }
        public DateTime StartTime { get; set; }
        public bool ShouldStop { get; set; }
    }
    #endregion

    #region Manager Classes
    public class BotManager
    {
        private List<Bot> bots;
        private Random random;
        private object lockObject = new object();

        public BotManager()
        {
            bots = new List<Bot>();
            random = new Random();
        }

        public void InitializeBots(List<Bot> botList)
        {
            bots = botList;
        }

        public bool StartAllBots()
        {
            lock (lockObject)
            {
                bool allStarted = true;
                foreach (var bot in bots)
                {
                    if (StartBot(bot))
                    {
                        bot.Status = BotStatus.Online;
                        bot.LastActivity = DateTime.Now;
                    }
                    else
                    {
                        allStarted = false;
                    }
                }
                return allStarted;
            }
        }

        public bool StopAllBots()
        {
            lock (lockObject)
            {
                bool allStopped = true;
                foreach (var bot in bots)
                {
                    if (StopBot(bot))
                    {
                        bot.Status = BotStatus.Offline;
                        bot.IsAttacking = false;
                    }
                    else
                    {
                        allStopped = false;
                    }
                }
                return allStopped;
            }
        }

        public bool EmergencyStopAll()
        {
            lock (lockObject)
            {
                foreach (var bot in bots)
                {
                    bot.Status = BotStatus.Error;
                    bot.IsAttacking = false;
                }
                return true;
            }
        }

        public bool LaunchCoordinatedAttack(AttackTarget target)
        {
            lock (lockObject)
            {
                bool allLaunched = true;
                foreach (var bot in bots)
                {
                    if (bot.Status == BotStatus.Online)
                    {
                        if (LaunchBotAttack(bot, target))
                        {
                            bot.Status = BotStatus.Attacking;
                            bot.IsAttacking = true;
                            bot.CurrentTarget = $"{target.IP}:{target.Port}";
                        }
                        else
                        {
                            allLaunched = false;
                        }
                    }
                }
                return allLaunched;
            }
        }

        public bool StopAllAttacks()
        {
            lock (lockObject)
            {
                foreach (var bot in bots)
                {
                    if (bot.IsAttacking)
                    {
                        bot.IsAttacking = false;
                        bot.Status = BotStatus.Online;
                        bot.CurrentTarget = "";
                    }
                }
                return true;
            }
        }

        public void ShutdownAll()
        {
            StopAllBots();
        }

        private bool StartBot(Bot bot)
        {
            // Simulate bot startup
            Thread.Sleep(random.Next(100, 500));
            return true;
        }

        private bool StopBot(Bot bot)
        {
            // Simulate bot shutdown
            Thread.Sleep(random.Next(50, 200));
            return true;
        }

        private bool LaunchBotAttack(Bot bot, AttackTarget target)
        {
            // Simulate attack launch
            Task.Run(() => SimulateBotAttack(bot, target));
            return true;
        }

        private void SimulateBotAttack(Bot bot, AttackTarget target)
        {
            var startTime = DateTime.Now;
            var endTime = startTime.AddSeconds(target.Duration);

            while (DateTime.Now < endTime && !target.ShouldStop)
            {
                // Simulate attack requests
                int requests = random.Next(1, target.Intensity * 10);
                
                for (int i = 0; i < requests; i++)
                {
                    bot.TotalRequests++;
                    if (random.Next(100) > 10) // 90% success rate
                    {
                        bot.SuccessfulRequests++;
                    }
                    else
                    {
                        bot.FailedRequests++;
                    }
                }

                Thread.Sleep(random.Next(10, 100));
            }

            bot.IsAttacking = false;
            bot.Status = BotStatus.Online;
            bot.CurrentTarget = "";
        }
    }

    public class NetworkManager
    {
        private string vpsIp;
        private int vpsPort;
        private Random random;

        public NetworkManager()
        {
            random = new Random();
        }

        public void SetVpsEndpoint(string ip, int port)
        {
            vpsIp = ip;
            vpsPort = port;
        }

        public NetworkStatus GetNetworkStatus()
        {
            return new NetworkStatus
            {
                Status = "Connected",
                Bandwidth = $"{random.Next(100, 2000)} MB/s",
                Latency = random.Next(10, 100),
                ActiveConnections = 23
            };
        }

        public List<NetworkHost> ScanNetwork()
        {
            var hosts = new List<NetworkHost>();
            
            // Simulate network scan
            for (int i = 0; i < 10; i++)
            {
                hosts.Add(new NetworkHost
                {
                    IP = $"192.168.1.{i + 1}",
                    Hostname = $"host{i + 1}.local",
                    Status = random.Next(2) == 0 ? "Online" : "Offline",
                    Ports = Enumerable.Range(1, random.Next(5, 20)).Select(p => random.Next(1, 65535)).ToList()
                });
            }

            return hosts;
        }
    }

    public class DatabaseManager
    {
        private string connectionString;

        public DatabaseManager()
        {
            connectionString = ConfigurationManager.ConnectionStrings["VexityBotDB"]?.ConnectionString 
                ?? "Data Source=localhost;Initial Catalog=VexityBot;Integrated Security=True";
        }

        public string BackupDatabase()
        {
            string backupPath = Path.Combine(Application.StartupPath, "backups", $"VexityBot_Backup_{DateTime.Now:yyyyMMdd_HHmmss}.bak");
            
            Directory.CreateDirectory(Path.GetDirectoryName(backupPath));
            
            // Simulate backup
            File.WriteAllText(backupPath, $"VexityBot Database Backup - {DateTime.Now}");
            
            return backupPath;
        }
    }

    public class Logger
    {
        private string logFile;
        private object lockObject = new object();

        public Logger(string filename)
        {
            logFile = Path.Combine(Application.StartupPath, "logs", filename);
            Directory.CreateDirectory(Path.GetDirectoryName(logFile));
        }

        public void Log(string message, LogLevel level = LogLevel.Info)
        {
            lock (lockObject)
            {
                string logEntry = $"[{DateTime.Now:yyyy-MM-dd HH:mm:ss}] [{level}] {message}";
                File.AppendAllText(logFile, logEntry + Environment.NewLine);
                Console.WriteLine(logEntry);
            }
        }
    }

    public enum LogLevel
    {
        Debug,
        Info,
        Warning,
        Error
    }

    public class NetworkStatus
    {
        public string Status { get; set; }
        public string Bandwidth { get; set; }
        public int Latency { get; set; }
        public int ActiveConnections { get; set; }
    }

    public class NetworkHost
    {
        public string IP { get; set; }
        public string Hostname { get; set; }
        public string Status { get; set; }
        public List<int> Ports { get; set; }
    }
    #endregion

    #region Bot Admin Form
    public partial class BotAdminForm : Form
    {
        private Bot bot;
        private BotManager botManager;
        private Logger logger;
        private System.Timers.Timer statusTimer;

        public BotAdminForm(Bot bot, BotManager botManager, Logger logger)
        {
            this.bot = bot;
            this.botManager = botManager;
            this.logger = logger;
            
            InitializeComponent();
            InitializeBotAdmin();
        }

        private void InitializeBotAdmin()
        {
            Text = $"Bot Admin Panel - {bot.Name}";
            
            // Setup bot-specific controls
            lblBotName.Text = bot.Name;
            lblSpecialty.Text = bot.Specialty;
            lblPort.Text = bot.Port.ToString();
            
            // Setup status timer
            statusTimer = new System.Timers.Timer(1000);
            statusTimer.Elapsed += StatusTimer_Elapsed;
            statusTimer.AutoReset = true;
            statusTimer.Enabled = true;
            
            UpdateBotInfo();
        }

        private void StatusTimer_Elapsed(object sender, ElapsedEventArgs e)
        {
            if (InvokeRequired)
            {
                Invoke(new Action(() => UpdateBotInfo()));
            }
            else
            {
                UpdateBotInfo();
            }
        }

        private void UpdateBotInfo()
        {
            lblStatus.Text = $"Status: {bot.Status}";
            lblRequests.Text = $"Total Requests: {bot.TotalRequests:N0}";
            lblSuccess.Text = $"Successful: {bot.SuccessfulRequests:N0}";
            lblFailed.Text = $"Failed: {bot.FailedRequests:N0}";
            lblUptime.Text = $"Uptime: {bot.UptimePercentage:F1}%";
            lblAttacking.Text = $"Attacking: {(bot.IsAttacking ? "Yes" : "No")}";
            lblTarget.Text = $"Target: {bot.CurrentTarget}";
        }

        private void btnLaunchAttack_Click(object sender, EventArgs e)
        {
            logger.Log($"{bot.Name} launching attack", LogLevel.Info);
            
            var target = new AttackTarget
            {
                IP = txtTargetIP.Text,
                Port = int.Parse(txtTargetPort.Text),
                AttackType = (AttackType)cmbAttackType.SelectedValue,
                Intensity = (int)nudIntensity.Value,
                Duration = 60
            };
            
            // Launch attack logic here
            bot.Status = BotStatus.Attacking;
            bot.IsAttacking = true;
            bot.CurrentTarget = $"{target.IP}:{target.Port}";
        }

        private void btnStopAttack_Click(object sender, EventArgs e)
        {
            logger.Log($"{bot.Name} stopping attack", LogLevel.Info);
            
            bot.Status = BotStatus.Online;
            bot.IsAttacking = false;
            bot.CurrentTarget = "";
        }

        private void btnEmergencyStop_Click(object sender, EventArgs e)
        {
            var result = MessageBox.Show($"Emergency stop {bot.Name}? This will halt all operations immediately!", 
                "Emergency Stop", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);
            
            if (result == DialogResult.Yes)
            {
                logger.Log($"EMERGENCY STOP: {bot.Name}", LogLevel.Warning);
                
                bot.Status = BotStatus.Error;
                bot.IsAttacking = false;
                bot.CurrentTarget = "";
            }
        }

        private void btnOvercharge_Click(object sender, EventArgs e)
        {
            logger.Log($"{bot.Name} overcharging systems", LogLevel.Info);
            
            // Simulate overcharge
            MessageBox.Show($"{bot.Name} is now operating at MAXIMUM POWER!", "Overcharge", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }

        private void btnReset_Click(object sender, EventArgs e)
        {
            logger.Log($"{bot.Name} resetting systems", LogLevel.Info);
            
            bot.Status = BotStatus.Offline;
            bot.IsAttacking = false;
            bot.CurrentTarget = "";
            
            // Simulate reset
            Thread.Sleep(1000);
            
            bot.Status = BotStatus.Online;
        }

        protected override void OnFormClosing(FormClosingEventArgs e)
        {
            statusTimer?.Stop();
            base.OnFormClosing(e);
        }
    }
    #endregion

    #region Network Scan Results Form
    public partial class NetworkScanResultsForm : Form
    {
        private List<NetworkHost> hosts;

        public NetworkScanResultsForm(List<NetworkHost> scanResults)
        {
            hosts = scanResults;
            InitializeComponent();
            InitializeScanResults();
        }

        private void InitializeScanResults()
        {
            Text = "Network Scan Results";
            
            dgvScanResults.DataSource = hosts;
            dgvScanResults.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill;
        }
    }
    #endregion

    #region Program Entry Point
    public static class Program
    {
        [STAThread]
        public static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new VexityBotMainForm());
        }
    }
    #endregion
}
