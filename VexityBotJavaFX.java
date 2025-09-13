package com.vexitybot.gui;

import javafx.application.Application;
import javafx.application.Platform;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;
import javafx.stage.Stage;
import javafx.concurrent.Task;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/**
 * VexityBot JavaFX GUI Application
 * Advanced Bot Management System with Database Integration
 */
public class VexityBotJavaFX extends Application {
    
    private Stage primaryStage;
    private TabPane mainTabPane;
    private TableView<Bot> botTable;
    private ObservableList<Bot> botData;
    private ExecutorService executorService;
    private DatabaseManager dbManager;
    private NetworkManager networkManager;
    
    // Bot Management Components
    private TextField targetIpField;
    private TextField targetPortField;
    private ComboBox<String> attackTypeCombo;
    private Slider intensitySlider;
    private ProgressBar attackProgress;
    private TextArea logArea;
    
    @Override
    public void start(Stage primaryStage) {
        this.primaryStage = primaryStage;
        this.executorService = Executors.newFixedThreadPool(10);
        this.dbManager = new DatabaseManager();
        this.networkManager = new NetworkManager();
        
        initializeDatabase();
        createMainInterface();
        
        primaryStage.setTitle("VexityBot - Advanced Bot Management System");
        primaryStage.setScene(new Scene(createMainLayout(), 1200, 800));
        primaryStage.show();
    }
    
    private void initializeDatabase() {
        try {
            dbManager.initializeDatabase();
            loadBotData();
        } catch (SQLException e) {
            showAlert("Database Error", "Failed to initialize database: " + e.getMessage());
        }
    }
    
    private void loadBotData() {
        botData = FXCollections.observableArrayList();
        try {
            List<Bot> bots = dbManager.getAllBots();
            botData.addAll(bots);
        } catch (SQLException e) {
            showAlert("Database Error", "Failed to load bot data: " + e.getMessage());
        }
    }
    
    private VBox createMainLayout() {
        VBox mainLayout = new VBox(10);
        mainLayout.setPadding(new Insets(10));
        
        // Header
        HBox header = createHeader();
        mainLayout.getChildren().add(header);
        
        // Main Tab Pane
        mainTabPane = new TabPane();
        mainTabPane.getTabs().addAll(
            createBotManagementTab(),
            createAttackControlTab(),
            createNetworkMonitorTab(),
            createDatabaseTab(),
            createSettingsTab()
        );
        mainLayout.getChildren().add(mainTabPane);
        
        return mainLayout;
    }
    
    private HBox createHeader() {
        HBox header = new HBox(20);
        header.setAlignment(Pos.CENTER_LEFT);
        header.setPadding(new Insets(10));
        header.setStyle("-fx-background-color: #2c3e50; -fx-background-radius: 5;");
        
        Label title = new Label("🤖 VexityBot Management System");
        title.setFont(Font.font("Arial", FontWeight.BOLD, 24));
        title.setTextFill(Color.WHITE);
        
        Label status = new Label("🟢 System Online");
        status.setFont(Font.font("Arial", 14));
        status.setTextFill(Color.LIGHTGREEN);
        
        HBox.setHgrow(title, Priority.ALWAYS);
        header.getChildren().addAll(title, status);
        
        return header;
    }
    
    private Tab createBotManagementTab() {
        Tab botTab = new Tab("Bot Management");
        botTab.setClosable(false);
        
        VBox botLayout = new VBox(10);
        
        // Bot Table
        botTable = new TableView<>();
        setupBotTable();
        
        // Control Buttons
        HBox controlButtons = createBotControlButtons();
        
        botLayout.getChildren().addAll(botTable, controlButtons);
        botTab.setContent(botLayout);
        
        return botTab;
    }
    
    private void setupBotTable() {
        TableColumn<Bot, String> nameCol = new TableColumn<>("Bot Name");
        nameCol.setCellValueFactory(new PropertyValueFactory<>("name"));
        
        TableColumn<Bot, String> statusCol = new TableColumn<>("Status");
        statusCol.setCellValueFactory(new PropertyValueFactory<>("status"));
        statusCol.setCellFactory(column -> new TableCell<Bot, String>() {
            @Override
            protected void updateItem(String status, boolean empty) {
                super.updateItem(status, empty);
                if (!empty) {
                    setText(status);
                    if ("Online".equals(status)) {
                        setTextFill(Color.GREEN);
                    } else if ("Offline".equals(status)) {
                        setTextFill(Color.RED);
                    } else {
                        setTextFill(Color.ORANGE);
                    }
                }
            }
        });
        
        TableColumn<Bot, Integer> portCol = new TableColumn<>("Port");
        portCol.setCellValueFactory(new PropertyValueFactory<>("port"));
        
        TableColumn<Bot, String> specialtyCol = new TableColumn<>("Specialty");
        specialtyCol.setCellValueFactory(new PropertyValueFactory<>("specialty"));
        
        TableColumn<Bot, Integer> requestsCol = new TableColumn<>("Requests");
        requestsCol.setCellValueFactory(new PropertyValueFactory<>("requests"));
        
        TableColumn<Bot, String> uptimeCol = new TableColumn<>("Uptime");
        uptimeCol.setCellValueFactory(new PropertyValueFactory<>("uptime"));
        
        botTable.getColumns().addAll(nameCol, statusCol, portCol, specialtyCol, requestsCol, uptimeCol);
        botTable.setItems(botData);
        botTable.setRowFactory(tv -> {
            TableRow<Bot> row = new TableRow<>();
            row.setOnMouseClicked(event -> {
                if (event.getClickCount() == 2 && !row.isEmpty()) {
                    Bot bot = row.getItem();
                    openBotAdminPanel(bot);
                }
            });
            return row;
        });
    }
    
    private HBox createBotControlButtons() {
        HBox buttonBox = new HBox(10);
        buttonBox.setAlignment(Pos.CENTER);
        
        Button startAllBtn = new Button("🚀 Start All Bots");
        startAllBtn.setOnAction(e -> startAllBots());
        
        Button stopAllBtn = new Button("⏹️ Stop All Bots");
        stopAllBtn.setOnAction(e -> stopAllBots());
        
        Button refreshBtn = new Button("🔄 Refresh");
        refreshBtn.setOnAction(e -> refreshBotData());
        
        Button addBotBtn = new Button("➕ Add Bot");
        addBotBtn.setOnAction(e -> addNewBot());
        
        buttonBox.getChildren().addAll(startAllBtn, stopAllBtn, refreshBtn, addBotBtn);
        return buttonBox;
    }
    
    private Tab createAttackControlTab() {
        Tab attackTab = new Tab("Attack Control");
        attackTab.setClosable(false);
        
        VBox attackLayout = new VBox(20);
        attackLayout.setPadding(new Insets(20));
        
        // Target Configuration
        VBox targetConfig = createTargetConfiguration();
        
        // Attack Controls
        VBox attackControls = createAttackControls();
        
        // Progress and Logs
        VBox progressLogs = createProgressAndLogs();
        
        attackLayout.getChildren().addAll(targetConfig, attackControls, progressLogs);
        attackTab.setContent(attackLayout);
        
        return attackTab;
    }
    
    private VBox createTargetConfiguration() {
        VBox targetConfig = new VBox(10);
        targetConfig.setStyle("-fx-background-color: #ecf0f1; -fx-padding: 15; -fx-background-radius: 5;");
        
        Label title = new Label("🎯 Target Configuration");
        title.setFont(Font.font("Arial", FontWeight.BOLD, 16));
        
        GridPane configGrid = new GridPane();
        configGrid.setHgap(10);
        configGrid.setVgap(10);
        
        targetIpField = new TextField("1.1.1.1");
        targetPortField = new TextField("8080");
        attackTypeCombo = new ComboBox<>();
        attackTypeCombo.getItems().addAll("DDoS", "Port Scan", "Vulnerability Scan", "Brute Force", "Custom");
        attackTypeCombo.setValue("DDoS");
        
        intensitySlider = new Slider(1, 10, 5);
        intensitySlider.setShowTickLabels(true);
        intensitySlider.setShowTickMarks(true);
        intensitySlider.setMajorTickUnit(1);
        intensitySlider.setBlockIncrement(1);
        
        configGrid.add(new Label("Target IP:"), 0, 0);
        configGrid.add(targetIpField, 1, 0);
        configGrid.add(new Label("Port:"), 0, 1);
        configGrid.add(targetPortField, 1, 1);
        configGrid.add(new Label("Attack Type:"), 0, 2);
        configGrid.add(attackTypeCombo, 1, 2);
        configGrid.add(new Label("Intensity:"), 0, 3);
        configGrid.add(intensitySlider, 1, 3);
        
        targetConfig.getChildren().addAll(title, configGrid);
        return targetConfig;
    }
    
    private VBox createAttackControls() {
        VBox attackControls = new VBox(10);
        attackControls.setStyle("-fx-background-color: #e74c3c; -fx-padding: 15; -fx-background-radius: 5;");
        
        Label title = new Label("⚡ Attack Controls");
        title.setFont(Font.font("Arial", FontWeight.BOLD, 16));
        title.setTextFill(Color.WHITE);
        
        HBox buttonBox = new HBox(10);
        buttonBox.setAlignment(Pos.CENTER);
        
        Button launchBtn = new Button("🚀 Launch Attack");
        launchBtn.setStyle("-fx-background-color: #c0392b; -fx-text-fill: white; -fx-font-weight: bold;");
        launchBtn.setOnAction(e -> launchCoordinatedAttack());
        
        Button stopBtn = new Button("⏹️ Stop Attack");
        stopBtn.setStyle("-fx-background-color: #34495e; -fx-text-fill: white;");
        stopBtn.setOnAction(e -> stopAttack());
        
        Button testBtn = new Button("🧪 Test Mode");
        testBtn.setStyle("-fx-background-color: #f39c12; -fx-text-fill: white;");
        testBtn.setOnAction(e -> testAttack());
        
        buttonBox.getChildren().addAll(launchBtn, stopBtn, testBtn);
        attackControls.getChildren().addAll(title, buttonBox);
        
        return attackControls;
    }
    
    private VBox createProgressAndLogs() {
        VBox progressLogs = new VBox(10);
        
        // Progress Bar
        Label progressLabel = new Label("Attack Progress:");
        attackProgress = new ProgressBar(0);
        attackProgress.setPrefWidth(Double.MAX_VALUE);
        
        // Log Area
        Label logLabel = new Label("Attack Logs:");
        logArea = new TextArea();
        logArea.setPrefHeight(200);
        logArea.setEditable(false);
        logArea.setStyle("-fx-font-family: 'Courier New'; -fx-font-size: 12;");
        
        progressLogs.getChildren().addAll(progressLabel, attackProgress, logLabel, logArea);
        return progressLogs;
    }
    
    private Tab createNetworkMonitorTab() {
        Tab networkTab = new Tab("Network Monitor");
        networkTab.setClosable(false);
        
        VBox networkLayout = new VBox(10);
        
        // Network Statistics
        VBox networkStats = createNetworkStatistics();
        
        // Real-time Network Graph (simplified)
        VBox networkGraph = createNetworkGraph();
        
        networkLayout.getChildren().addAll(networkStats, networkGraph);
        networkTab.setContent(networkLayout);
        
        return networkTab;
    }
    
    private VBox createNetworkStatistics() {
        VBox statsBox = new VBox(10);
        statsBox.setStyle("-fx-background-color: #3498db; -fx-padding: 15; -fx-background-radius: 5;");
        
        Label title = new Label("📊 Network Statistics");
        title.setFont(Font.font("Arial", FontWeight.BOLD, 16));
        title.setTextFill(Color.WHITE);
        
        GridPane statsGrid = new GridPane();
        statsGrid.setHgap(20);
        statsGrid.setVgap(10);
        
        statsGrid.add(new Label("Active Connections:"), 0, 0);
        statsGrid.add(new Label("23"), 1, 0);
        statsGrid.add(new Label("Bandwidth Usage:"), 0, 1);
        statsGrid.add(new Label("1.2 GB/s"), 1, 1);
        statsGrid.add(new Label("Latency:"), 0, 2);
        statsGrid.add(new Label("45ms"), 1, 2);
        statsGrid.add(new Label("Packet Loss:"), 0, 3);
        statsGrid.add(new Label("0.1%"), 1, 3);
        
        statsBox.getChildren().addAll(title, statsGrid);
        return statsBox;
    }
    
    private VBox createNetworkGraph() {
        VBox graphBox = new VBox(10);
        graphBox.setStyle("-fx-background-color: #2c3e50; -fx-padding: 15; -fx-background-radius: 5;");
        
        Label title = new Label("🌐 Network Topology");
        title.setFont(Font.font("Arial", FontWeight.BOLD, 16));
        title.setTextFill(Color.WHITE);
        
        TextArea graphArea = new TextArea();
        graphArea.setPrefHeight(300);
        graphArea.setEditable(false);
        graphArea.setStyle("-fx-font-family: 'Courier New'; -fx-font-size: 10;");
        
        // Simple ASCII network diagram
        String networkDiagram = """
            VexityBot Network Topology
            =========================
            
            VPS Server (191.96.152.162:8080)
            ├── AlphaBot (8081) - Nuclear Warfare
            ├── BetaBot (8082) - Cyber Warfare
            ├── GammaBot (8083) - Stealth Ops
            ├── DeltaBot (8084) - EMP Warfare
            ├── EpsilonBot (8085) - Bio Warfare
            ├── ZetaBot (8086) - Gravity Control
            ├── EtaBot (8087) - Thermal Annihilation
            ├── ThetaBot (8088) - Cryogenic Freeze
            ├── IotaBot (8089) - Quantum Entanglement
            ├── KappaBot (8090) - Dimensional Portal
            ├── LambdaBot (8091) - Neural Network
            ├── MuBot (8092) - Molecular Disassembly
            ├── NuBot (8093) - Sound Wave Devastation
            ├── XiBot (8094) - Light Manipulation
            ├── OmicronBot (8095) - Dark Matter Control
            ├── PiBot (8096) - Mathematical Chaos
            ├── RhoBot (8097) - Chemical Reactions
            ├── SigmaBot (8098) - Magnetic Fields
            ├── TauBot (8099) - Time Manipulation
            ├── UpsilonBot (8100) - Space-Time Fabric
            ├── PhiBot (8101) - Consciousness Control
            ├── ChiBot (8102) - Energy Vortex
            └── PsiBot (8103) - Psychic Warfare
            """;
        
        graphArea.setText(networkDiagram);
        graphBox.getChildren().addAll(title, graphArea);
        
        return graphBox;
    }
    
    private Tab createDatabaseTab() {
        Tab dbTab = new Tab("Database");
        dbTab.setClosable(false);
        
        VBox dbLayout = new VBox(10);
        
        // Database Controls
        HBox dbControls = new HBox(10);
        Button refreshDbBtn = new Button("🔄 Refresh Database");
        Button backupBtn = new Button("💾 Backup Database");
        Button restoreBtn = new Button("📥 Restore Database");
        
        dbControls.getChildren().addAll(refreshDbBtn, backupBtn, restoreBtn);
        
        // Database Query Area
        VBox queryArea = new VBox(10);
        TextArea queryText = new TextArea();
        queryText.setPromptText("Enter SQL query here...");
        queryText.setPrefHeight(100);
        
        Button executeBtn = new Button("▶️ Execute Query");
        executeBtn.setOnAction(e -> executeQuery(queryText.getText()));
        
        TextArea resultArea = new TextArea();
        resultArea.setPrefHeight(200);
        resultArea.setEditable(false);
        
        queryArea.getChildren().addAll(
            new Label("SQL Query:"), queryText, executeBtn,
            new Label("Results:"), resultArea
        );
        
        dbLayout.getChildren().addAll(dbControls, queryArea);
        dbTab.setContent(dbLayout);
        
        return dbTab;
    }
    
    private Tab createSettingsTab() {
        Tab settingsTab = new Tab("Settings");
        settingsTab.setClosable(false);
        
        VBox settingsLayout = new VBox(20);
        settingsLayout.setPadding(new Insets(20));
        
        // General Settings
        VBox generalSettings = createGeneralSettings();
        
        // Network Settings
        VBox networkSettings = createNetworkSettings();
        
        // Security Settings
        VBox securitySettings = createSecuritySettings();
        
        settingsLayout.getChildren().addAll(generalSettings, networkSettings, securitySettings);
        settingsTab.setContent(settingsLayout);
        
        return settingsTab;
    }
    
    private VBox createGeneralSettings() {
        VBox generalBox = new VBox(10);
        generalBox.setStyle("-fx-background-color: #ecf0f1; -fx-padding: 15; -fx-background-radius: 5;");
        
        Label title = new Label("⚙️ General Settings");
        title.setFont(Font.font("Arial", FontWeight.BOLD, 16));
        
        GridPane settingsGrid = new GridPane();
        settingsGrid.setHgap(10);
        settingsGrid.setVgap(10);
        
        CheckBox autoStart = new CheckBox("Auto-start bots on launch");
        CheckBox logToFile = new CheckBox("Log to file");
        CheckBox notifications = new CheckBox("Enable notifications");
        
        ComboBox<String> themeCombo = new ComboBox<>();
        themeCombo.getItems().addAll("Light", "Dark", "High Contrast");
        themeCombo.setValue("Light");
        
        settingsGrid.add(new Label("Theme:"), 0, 0);
        settingsGrid.add(themeCombo, 1, 0);
        settingsGrid.add(autoStart, 0, 1);
        settingsGrid.add(logToFile, 0, 2);
        settingsGrid.add(notifications, 0, 3);
        
        generalBox.getChildren().addAll(title, settingsGrid);
        return generalBox;
    }
    
    private VBox createNetworkSettings() {
        VBox networkBox = new VBox(10);
        networkBox.setStyle("-fx-background-color: #3498db; -fx-padding: 15; -fx-background-radius: 5;");
        
        Label title = new Label("🌐 Network Settings");
        title.setFont(Font.font("Arial", FontWeight.BOLD, 16));
        title.setTextFill(Color.WHITE);
        
        GridPane networkGrid = new GridPane();
        networkGrid.setHgap(10);
        networkGrid.setVgap(10);
        
        TextField vpsIpField = new TextField("191.96.152.162");
        TextField vpsPortField = new TextField("8080");
        TextField maxConnectionsField = new TextField("1000");
        TextField timeoutField = new TextField("30");
        
        networkGrid.add(new Label("VPS IP:"), 0, 0);
        networkGrid.add(vpsIpField, 1, 0);
        networkGrid.add(new Label("VPS Port:"), 0, 1);
        networkGrid.add(vpsPortField, 1, 1);
        networkGrid.add(new Label("Max Connections:"), 0, 2);
        networkGrid.add(maxConnectionsField, 1, 2);
        networkGrid.add(new Label("Timeout (seconds):"), 0, 3);
        networkGrid.add(timeoutField, 1, 3);
        
        networkBox.getChildren().addAll(title, networkGrid);
        return networkBox;
    }
    
    private VBox createSecuritySettings() {
        VBox securityBox = new VBox(10);
        securityBox.setStyle("-fx-background-color: #e74c3c; -fx-padding: 15; -fx-background-radius: 5;");
        
        Label title = new Label("🔒 Security Settings");
        title.setFont(Font.font("Arial", FontWeight.BOLD, 16));
        title.setTextFill(Color.WHITE);
        
        GridPane securityGrid = new GridPane();
        securityGrid.setHgap(10);
        securityGrid.setVgap(10);
        
        CheckBox encryption = new CheckBox("Enable encryption");
        CheckBox firewall = new CheckBox("Enable firewall");
        CheckBox logging = new CheckBox("Enable security logging");
        
        ComboBox<String> encryptionCombo = new ComboBox<>();
        encryptionCombo.getItems().addAll("AES-128", "AES-256", "RSA-2048", "RSA-4096");
        encryptionCombo.setValue("AES-256");
        
        securityGrid.add(new Label("Encryption:"), 0, 0);
        securityGrid.add(encryptionCombo, 1, 0);
        securityGrid.add(encryption, 0, 1);
        securityGrid.add(firewall, 0, 2);
        securityGrid.add(logging, 0, 3);
        
        securityBox.getChildren().addAll(title, securityGrid);
        return securityBox;
    }
    
    // Bot Management Methods
    private void startAllBots() {
        Task<Void> startTask = new Task<Void>() {
            @Override
            protected Void call() throws Exception {
                for (Bot bot : botData) {
                    bot.setStatus("Online");
                    Platform.runLater(() -> {
                        logArea.appendText("Started " + bot.getName() + " on port " + bot.getPort() + "\n");
                    });
                    Thread.sleep(100); // Simulate startup delay
                }
                return null;
            }
        };
        
        executorService.submit(startTask);
    }
    
    private void stopAllBots() {
        Task<Void> stopTask = new Task<Void>() {
            @Override
            protected Void call() throws Exception {
                for (Bot bot : botData) {
                    bot.setStatus("Offline");
                    Platform.runLater(() -> {
                        logArea.appendText("Stopped " + bot.getName() + "\n");
                    });
                    Thread.sleep(100);
                }
                return null;
            }
        };
        
        executorService.submit(stopTask);
    }
    
    private void refreshBotData() {
        loadBotData();
        botTable.refresh();
    }
    
    private void addNewBot() {
        // Create dialog for adding new bot
        Dialog<Bot> dialog = new Dialog<>();
        dialog.setTitle("Add New Bot");
        
        ButtonType addButton = new ButtonType("Add", ButtonBar.ButtonData.OK_DONE);
        dialog.getDialogPane().getButtonTypes().addAll(addButton, ButtonType.CANCEL);
        
        GridPane grid = new GridPane();
        grid.setHgap(10);
        grid.setVgap(10);
        grid.setPadding(new Insets(20));
        
        TextField nameField = new TextField();
        TextField portField = new TextField();
        ComboBox<String> specialtyCombo = new ComboBox<>();
        specialtyCombo.getItems().addAll("Nuclear Warfare", "Cyber Warfare", "Stealth Ops", "EMP Warfare", "Bio Warfare");
        
        grid.add(new Label("Bot Name:"), 0, 0);
        grid.add(nameField, 1, 0);
        grid.add(new Label("Port:"), 0, 1);
        grid.add(portField, 1, 1);
        grid.add(new Label("Specialty:"), 0, 2);
        grid.add(specialtyCombo, 1, 2);
        
        dialog.getDialogPane().setContent(grid);
        
        dialog.setResultConverter(dialogButton -> {
            if (dialogButton == addButton) {
                return new Bot(nameField.getText(), "Offline", 
                    Integer.parseInt(portField.getText()), 
                    specialtyCombo.getValue(), 0, "0%");
            }
            return null;
        });
        
        dialog.showAndWait().ifPresent(bot -> {
            botData.add(bot);
            try {
                dbManager.addBot(bot);
            } catch (SQLException e) {
                showAlert("Database Error", "Failed to add bot: " + e.getMessage());
            }
        });
    }
    
    private void openBotAdminPanel(Bot bot) {
        Stage adminStage = new Stage();
        adminStage.setTitle("Admin Panel - " + bot.getName());
        
        VBox adminLayout = new VBox(20);
        adminLayout.setPadding(new Insets(20));
        
        Label title = new Label("👑 " + bot.getName() + " - " + bot.getSpecialty());
        title.setFont(Font.font("Arial", FontWeight.BOLD, 20));
        
        // Bot-specific controls
        VBox controls = createBotSpecificControls(bot);
        
        // Status display
        TextArea statusArea = new TextArea();
        statusArea.setPrefHeight(200);
        statusArea.setEditable(false);
        statusArea.setText("Bot Status: " + bot.getStatus() + "\n" +
                          "Port: " + bot.getPort() + "\n" +
                          "Specialty: " + bot.getSpecialty() + "\n" +
                          "Requests: " + bot.getRequests() + "\n" +
                          "Uptime: " + bot.getUptime());
        
        adminLayout.getChildren().addAll(title, controls, statusArea);
        
        adminStage.setScene(new Scene(adminLayout, 600, 500));
        adminStage.show();
    }
    
    private VBox createBotSpecificControls(Bot bot) {
        VBox controls = new VBox(10);
        controls.setStyle("-fx-background-color: #2c3e50; -fx-padding: 15; -fx-background-radius: 5;");
        
        HBox buttonBox = new HBox(10);
        
        Button attackBtn = new Button("🚀 Launch Attack");
        attackBtn.setOnAction(e -> launchBotAttack(bot));
        
        Button stopBtn = new Button("⏹️ Emergency Stop");
        stopBtn.setOnAction(e -> emergencyStopBot(bot));
        
        Button resetBtn = new Button("🔄 Reset Systems");
        resetBtn.setOnAction(e -> resetBotSystems(bot));
        
        Button overchargeBtn = new Button("⚡ Overcharge");
        overchargeBtn.setOnAction(e -> overchargeBot(bot));
        
        buttonBox.getChildren().addAll(attackBtn, stopBtn, resetBtn, overchargeBtn);
        controls.getChildren().add(buttonBox);
        
        return controls;
    }
    
    private void launchBotAttack(Bot bot) {
        logArea.appendText(bot.getName() + " launched attack with " + bot.getSpecialty() + " capabilities!\n");
    }
    
    private void emergencyStopBot(Bot bot) {
        bot.setStatus("Offline");
        logArea.appendText("EMERGENCY STOP: " + bot.getName() + " halted immediately!\n");
    }
    
    private void resetBotSystems(Bot bot) {
        logArea.appendText("Resetting systems for " + bot.getName() + "...\n");
    }
    
    private void overchargeBot(Bot bot) {
        logArea.appendText(bot.getName() + " overcharged - operating at maximum power!\n");
    }
    
    private void launchCoordinatedAttack() {
        String targetIp = targetIpField.getText();
        String targetPort = targetPortField.getText();
        String attackType = attackTypeCombo.getValue();
        int intensity = (int) intensitySlider.getValue();
        
        logArea.appendText("🚀 COORDINATED ATTACK LAUNCHED\n");
        logArea.appendText("Target: " + targetIp + ":" + targetPort + "\n");
        logArea.appendText("Type: " + attackType + "\n");
        logArea.appendText("Intensity: " + intensity + "\n");
        logArea.appendText("Bots: 23 active\n\n");
        
        // Simulate attack progress
        Task<Void> attackTask = new Task<Void>() {
            @Override
            protected Void call() throws Exception {
                for (int i = 0; i <= 100; i++) {
                    final int progress = i;
                    Platform.runLater(() -> {
                        attackProgress.setProgress(progress / 100.0);
                        logArea.appendText("Attack Progress: " + progress + "%\n");
                    });
                    Thread.sleep(100);
                }
                return null;
            }
        };
        
        executorService.submit(attackTask);
    }
    
    private void stopAttack() {
        logArea.appendText("⏹️ ATTACK STOPPED\n");
        attackProgress.setProgress(0);
    }
    
    private void testAttack() {
        logArea.appendText("🧪 TEST MODE ACTIVATED\n");
        logArea.appendText("Running diagnostic tests...\n");
    }
    
    private void executeQuery(String query) {
        try {
            String result = dbManager.executeQuery(query);
            // Display result in result area
            logArea.appendText("Query executed successfully\n");
        } catch (SQLException e) {
            showAlert("Query Error", "Failed to execute query: " + e.getMessage());
        }
    }
    
    private void showAlert(String title, String message) {
        Alert alert = new Alert(Alert.AlertType.ERROR);
        alert.setTitle(title);
        alert.setHeaderText(null);
        alert.setContentText(message);
        alert.showAndWait();
    }
    
    @Override
    public void stop() {
        if (executorService != null) {
            executorService.shutdown();
        }
        if (dbManager != null) {
            try {
                dbManager.close();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
    }
    
    public static void main(String[] args) {
        launch(args);
    }
}

/**
 * Bot Data Model
 */
class Bot {
    private String name;
    private String status;
    private int port;
    private String specialty;
    private int requests;
    private String uptime;
    
    public Bot(String name, String status, int port, String specialty, int requests, String uptime) {
        this.name = name;
        this.status = status;
        this.port = port;
        this.specialty = specialty;
        this.requests = requests;
        this.uptime = uptime;
    }
    
    // Getters and Setters
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    
    public int getPort() { return port; }
    public void setPort(int port) { this.port = port; }
    
    public String getSpecialty() { return specialty; }
    public void setSpecialty(String specialty) { this.specialty = specialty; }
    
    public int getRequests() { return requests; }
    public void setRequests(int requests) { this.requests = requests; }
    
    public String getUptime() { return uptime; }
    public void setUptime(String uptime) { this.uptime = uptime; }
}

/**
 * Database Manager
 */
class DatabaseManager {
    private Connection connection;
    
    public void initializeDatabase() throws SQLException {
        // Initialize H2 database
        String url = "jdbc:h2:mem:vexitybot;DB_CLOSE_DELAY=-1";
        connection = DriverManager.getConnection(url);
        
        // Create tables
        String createBotsTable = """
            CREATE TABLE IF NOT EXISTS bots (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                status VARCHAR(20) NOT NULL,
                port INT NOT NULL,
                specialty VARCHAR(100) NOT NULL,
                requests INT DEFAULT 0,
                uptime VARCHAR(10) DEFAULT '0%',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """;
        
        try (Statement stmt = connection.createStatement()) {
            stmt.execute(createBotsTable);
            
            // Insert sample data
            insertSampleBots();
        }
    }
    
    private void insertSampleBots() throws SQLException {
        String[] botNames = {"AlphaBot", "BetaBot", "GammaBot", "DeltaBot", "EpsilonBot", 
                           "ZetaBot", "EtaBot", "ThetaBot", "IotaBot", "KappaBot",
                           "LambdaBot", "MuBot", "NuBot", "XiBot", "OmicronBot",
                           "PiBot", "RhoBot", "SigmaBot", "TauBot", "UpsilonBot",
                           "PhiBot", "ChiBot", "PsiBot"};
        
        String[] specialties = {"Nuclear Warfare", "Cyber Warfare", "Stealth Ops", "EMP Warfare", "Bio Warfare",
                              "Gravity Control", "Thermal Annihilation", "Cryogenic Freeze", "Quantum Entanglement", "Dimensional Portal",
                              "Neural Network", "Molecular Disassembly", "Sound Wave Devastation", "Light Manipulation", "Dark Matter Control",
                              "Mathematical Chaos", "Chemical Reactions", "Magnetic Fields", "Time Manipulation", "Space-Time Fabric",
                              "Consciousness Control", "Energy Vortex", "Psychic Warfare"};
        
        String insertBot = "INSERT INTO bots (name, status, port, specialty, requests, uptime) VALUES (?, ?, ?, ?, ?, ?)";
        
        try (PreparedStatement pstmt = connection.prepareStatement(insertBot)) {
            for (int i = 0; i < botNames.length; i++) {
                pstmt.setString(1, botNames[i]);
                pstmt.setString(2, "Online");
                pstmt.setInt(3, 8081 + i);
                pstmt.setString(4, specialties[i]);
                pstmt.setInt(5, new Random().nextInt(10000));
                pstmt.setString(6, String.format("%.1f%%", 95 + Math.random() * 5));
                pstmt.executeUpdate();
            }
        }
    }
    
    public List<Bot> getAllBots() throws SQLException {
        List<Bot> bots = new ArrayList<>();
        String query = "SELECT name, status, port, specialty, requests, uptime FROM bots";
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(query)) {
            
            while (rs.next()) {
                Bot bot = new Bot(
                    rs.getString("name"),
                    rs.getString("status"),
                    rs.getInt("port"),
                    rs.getString("specialty"),
                    rs.getInt("requests"),
                    rs.getString("uptime")
                );
                bots.add(bot);
            }
        }
        
        return bots;
    }
    
    public void addBot(Bot bot) throws SQLException {
        String insert = "INSERT INTO bots (name, status, port, specialty, requests, uptime) VALUES (?, ?, ?, ?, ?, ?)";
        
        try (PreparedStatement pstmt = connection.prepareStatement(insert)) {
            pstmt.setString(1, bot.getName());
            pstmt.setString(2, bot.getStatus());
            pstmt.setInt(3, bot.getPort());
            pstmt.setString(4, bot.getSpecialty());
            pstmt.setInt(5, bot.getRequests());
            pstmt.setString(6, bot.getUptime());
            pstmt.executeUpdate();
        }
    }
    
    public String executeQuery(String query) throws SQLException {
        StringBuilder result = new StringBuilder();
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(query)) {
            
            ResultSetMetaData metaData = rs.getMetaData();
            int columnCount = metaData.getColumnCount();
            
            // Add column headers
            for (int i = 1; i <= columnCount; i++) {
                result.append(metaData.getColumnName(i)).append("\t");
            }
            result.append("\n");
            
            // Add data rows
            while (rs.next()) {
                for (int i = 1; i <= columnCount; i++) {
                    result.append(rs.getString(i)).append("\t");
                }
                result.append("\n");
            }
        }
        
        return result.toString();
    }
    
    public void close() throws SQLException {
        if (connection != null) {
            connection.close();
        }
    }
}

/**
 * Network Manager
 */
class NetworkManager {
    public void sendAttackCommand(String targetIp, int targetPort, String attackType) {
        // Simulate network attack command
        System.out.println("Sending attack command to " + targetIp + ":" + targetPort + " using " + attackType);
    }
    
    public void stopAttack() {
        System.out.println("Stopping all attack commands");
    }
    
    public String getNetworkStatus() {
        return "Network Status: Active\nConnections: 23\nBandwidth: 1.2 GB/s\nLatency: 45ms";
    }
}
