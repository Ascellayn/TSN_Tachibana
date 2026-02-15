from Tachibana import *;










def Menu_Main() -> None:
	Favorites: list[TUI.Menu.Entry] = [
		TUI.Menu.Entry(0, "Create new SSH Connection", f"Save a brand new SSH server entry for {App.Name} to remember.", Function=Menu_SSH_Create),
	]
	Entries: TUI.Menu.Entries = [
		TUI.Menu.Entry(20, "Welcome to Tachibana, the Server Connection Manager of Adellian."),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(20, "Quick Actions", Bold=True),
		*Favorites,
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(20, "Server Protocols", Bold=True),
		TUI.Menu.Entry(0, "Secure Shell Server", f"Access the SSH Servers that {App.Name} has saved.", Function=Menu_Protocol, Arguments=("SSH",)),
		TUI.Menu.Entry(0, "WebDAV", f"Access the WebDAV Servers that {App.Name} has saved.", Function=Menu_Protocol, Arguments=("WebDAV",)),
		TUI.Menu.Entry(0, "Wireguard", f"Access the Wireguard Servers that {App.Name} has saved.", Function=Menu_Protocol, Arguments=("Wireguard",)),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(0, "Settings", f"Configure {App.Name} to your liking.", Function=Menu_Settings, Indentation=-2),
		TUI.Menu.Entry(0, f"Exit {App.Name}", "Your train will always be waiting for you, see you next time!", Function=Quit, Indentation=-2)
	];
	TUI.Menu.Interactive(Entries);
	Quit();




def Menu_Settings() -> None:
	Entries: TUI.Menu.Entries = [
		TUI.Menu.Entry(20, f"{App.Name} Settings", Bold=True),
		TUI.Menu.Entry(20, ""),
			TUI.Menu.Entry(20, "Per-Protocol Settings", Bold=True, Indentation=1),
				TUI.Menu.Entry(20, "SSH", Bold=True, Indentation=2),
				TUI.Menu.Entry(10, "Ping Servers", f"Allow {App.Name} to automatically mesure latency when you are selecting a server.", "Server_SSH_Ping", Indentation=2, Value=Safe.Nested_Dict(cast(dict[str, Any], Tachibana["Config"]), ["Servers", "SSH", "Ping"], True)),
		TUI.Menu.Entry(20, ""),
				TUI.Menu.Entry(20, "WebDAV", Bold=True, Indentation=2),
				TUI.Menu.Entry(10, "Ping Servers", f"Allow {App.Name} to automatically mesure latency when you are selecting a server.", "Server_WebDAV_Ping", Indentation=2, Value=Safe.Nested_Dict(cast(dict[str, Any], Tachibana["Config"]), ["Servers", "WebDAV", "Ping"], True)),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(1, f"Save Configuration", "Save all your settings visually present on this page."),
		TUI.Menu.Entry(0, f"Return to Main Menu", Function=Menu_Main, Indentation=-2)
	];
	uJSON: Type.uJSON_Config = TUI.Menu.Interactive(Entries);
	if (uJSON):
		Register.Tachibana_Config(uJSON);
		Menu_Main();
	TUI.Menu.Interactive(Entries);
	Menu_Main();





def Keybind_Delete_Server(Entry: TUI.Menu.Entry) -> bool:
	Description: str = f"Are you sure you want to delete {Entry.ID}?\n"

	if ("Profiles" in Tachibana["Servers"][Entry.Arguments[0]][Entry.Arguments[1]].keys()): # pyright: ignore[reportArgumentType]
		Description += f"This action will delete everything under \"{Entry.Arguments[1]}\" which, will in turn delete {len(Tachibana['Servers'][Entry.Arguments[0]][Entry.Arguments[1]]['Profiles'])} profiles.";
	else: Description += f"This action will delete internally \"{Entry.Arguments[1]}\"";
	
	if (Entry.ID and "Yes" == TUI.Menu.Popup(
		f"Confirm Deleting Server Entry",
		Description,
		TUI.Menu.Entry(12, Arguments=["Yes", "No"], Value="No")
	)):
		del Tachibana['Servers'][Entry.Arguments[0]][Entry.Arguments[1]];
		Data.Save();
	return True;


def Menu_Creation(Protocol: str) -> None:
	match Protocol:
		case "SSH": Menu_SSH_Create();
		case "WebDAV": Menu_WebDAV_Create();
		case "Wireguard": Menu_Wireguard_Create();
		case _: Menu_Main();


def Menu_Protocol(Protocol: str) -> None:
	Keybinds: TUI.Menu.Keybinds = [
		TUI.Menu.Keybind(100, "Delete Server Entry", Keybind_Delete_Server)
	];
	while True:
		Entries: TUI.Menu.Entries = [
			TUI.Menu.Entry(20, f"{Protocol} - Connections", Bold=True),
			*Menu_Entries(Protocol),
			TUI.Menu.Entry(20, ""),
			TUI.Menu.Entry(0, f"Register Server", f"Save a brand new {Protocol} server entry for {App.Name} to remember.", Function=Menu_Creation, Arguments=(Protocol,), Indentation=-2),
			TUI.Menu.Entry(0, f"Return to Main Menu", Function=Menu_Main, Indentation=-2)
		];

		Stay: bool = TUI.Menu.Interactive(Entries, Keybinds);
		match (Stay):
			case True: continue;
			case _: Menu_Main();



def Menu_Entries(Protocol: str) -> list[TUI.Menu.Entry]:
	Server_Entries: list[TUI.Menu.Entry] = [];
	Pinged: set[str] = set();
	Ping_Allowed: bool = Safe.Nested_Dict(cast(dict[str, Any], Tachibana["Config"]), ["Servers", Protocol, "Ping"], True);

	if (Protocol in Tachibana["Servers"].keys()):
		for Count, Server in enumerate(Tachibana["Servers"][Protocol].keys()):
			Latency: str = "";
			if (":" in Server and Ping_Allowed): # Ping Calculation using Sockets
				if (Server not in Pinged):
					Pinged.add(Server);

					TUI.Menu.Base();
					# Progress Bar
					Bar: str = f"█" * round(
						(Count/len(Tachibana["Servers"][Protocol].keys()))
						* (TUI.curses.COLS - 2)
					);
					TUI.Window.insstr(TUI.curses.LINES - 2, 1, Bar);

					# Text Information
					TUI.Window.insstr(2, 3, f"Pinging Servers... [{Count + 1}/{len(Tachibana["Servers"][Protocol].keys())}]");
					TUI.Window.insstr(3, 3, f"> {Server}");
					TUI.Window.refresh();
					#Time.time.sleep(1);


					Init: float = Time.Get_Unix(True);
					Socket: socket.socket = socket.socket(socket.AF_INET);
					Socket.settimeout(1);
					try:
						Address, Port = Server.split(":");
						Socket.connect((Address, int(Port)));
						Latency = f" ({round((Time.Get_Unix(True) - Init)*1000)}ms)";
					except: Latency = f" (Unreachable)";

			Server_Entries.append(
				TUI.Menu.Entry(
					0, 
					f"{Tachibana["Servers"][Protocol][Server]["Name"]}{Latency}",
					f"{App.Name} knows this server internally as \"{Server}\".",
					cast(str, Tachibana["Servers"][Protocol][Server]["Name"]),
					Unavailable=True,
					Arguments=(Protocol, Server)
				));
	
	if (len(Server_Entries) == 0): Server_Entries.append(TUI.Menu.Entry(20, f"{App.Name} does not have any {Protocol} Servers saved, try registering one!", Unavailable=True))
	return Server_Entries;










def Menu_SSH_Create() -> None:
	Entries: TUI.Menu.Entries = [
		TUI.Menu.Entry(20, "Create SSH Connection", Bold=True),
		TUI.Menu.Entry(11, "Server Name", "Specify a friendly name for you to remember this SSH Server. Will overwrite the name if a server with the same Address, Port and Protocol already exists.", ID="Tachibana_Name"),
		TUI.Menu.Entry(11, "Server Address", "Specify the IP Address or Hostname the SSH Server is on.", ID="Address"),
		TUI.Menu.Entry(11, "Server Port", "Specify which port the SSH Server is on.", Value="22", ID="Port", Arguments=(r"\d",)),
		TUI.Menu.Entry(11, "Username", "The username we should log on as.", Value="root", ID="Username"),
		TUI.Menu.Entry(11, "Password", "The password we should use to login.", ID="Password"),
		TUI.Menu.Entry(11, "SSH Key", "An absolute path to an SSH Key we should use.", Value="~/.ssh/id_rsa", ID="Passkey"),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(20, "SFTP Settings", Bold=True, Indentation=1),
		TUI.Menu.Entry(11, "Remote Folder", "Specify the folder you'd like to access from the Server remotely.", Value="/", Indentation=1, ID="Folder_Remote"),
		TUI.Menu.Entry(11, "Local Folder", "Specify a place in your filesystem where you would like to mount the remote folder.", Value="/media/SFTP", Indentation=1, ID="Folder_Local"),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(20, "Workarounds", Bold=True),
		TUI.Menu.Entry(10, "Spoof Terminal", "Enable to spoof to the Server which Terminal you are using. Useful if the Server does not support your Terminal.", ID="Term_Spoof"),
			TUI.Menu.Entry(11, "Exported Terminal", "Increases compatibility if your Server does not support your Terminal.", Indentation=1, Value="xterm-256color", ID="Term_Spoofed"),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(1, f"Save Server", "Create a brand new entry with the provided information."),
		TUI.Menu.Entry(0, f"Cancel", "Return to the Menu with all your saved SSH Servers.", Function=Menu_Protocol, Arguments=("SSH",), Indentation=-2),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(0, f"Return to Main Menu", Function=Menu_Main, Indentation=-2)
	];
	uJSON: Type.uJSON_SSH = TUI.Menu.Interactive(Entries);
	if (uJSON):
		Register.SSH(uJSON);
		Menu_Protocol("SSH");

	Menu_Main();





def Menu_WebDAV_Create() -> None:
	Entries: TUI.Menu.Entries = [
		TUI.Menu.Entry(20, "Create WebDAV Connection", Bold=True),
		TUI.Menu.Entry(11, "Server Name", "Specify a friendly name for you to remember this WebDAV Server. Will overwrite the name if a server with the same Address, Port and Protocol already exists.", ID="Tachibana_Name"),
		TUI.Menu.Entry(11, "WebDAV Name", "Specify a name used by the WebDAV Configurator.", ID="WebDAV_Name"),
		TUI.Menu.Entry(10, "Enable Encryption (HTTPS)", "Enable the use of HTTPS, recommended if you're connecting to a non-local WebDAV Server.", Value=False, ID="Encryption"),
		TUI.Menu.Entry(11, "Address", "Specify the IP Address or Hostname of the WebDAV Server.", ID="Address"),
		TUI.Menu.Entry(11, "Server Port", "Specify which port the WebDAV Server is on.", Value="80", ID="Port", Arguments=(r"\d",)),
		TUI.Menu.Entry(11, "Username", "The username we should log on as.", Value="admin", ID="Username"),
		TUI.Menu.Entry(11, "Password", "The password we should use to login.", ID="Password"),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(20, "Mounting Settings", Bold=True, Indentation=1),
		TUI.Menu.Entry(11, "Remote Folder", "Specify the folder you'd like to access from the Server remotely.", Value="/", Indentation=1, ID="Folder_Remote"),
		TUI.Menu.Entry(11, "Local Folder", "Specify a place in your filesystem where you would like to mount the remote folder.", Value="/media/WebDAV", Indentation=1, ID="Folder_Local"),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(20, "Caching", Bold=True),
		TUI.Menu.Entry(10, "Enable VFS Cache", "This settings allows the WebDAV Client to store certain files for faster file access at the cost of increased disk usage on the client side.", Value=True, ID="Cache_VFS"),
			TUI.Menu.Entry(12, "Cache Mode", "Specify which VFS Caching Mode we should use.", Value="full", Arguments=("off", "writes", "full", "writeback"), ID="Cache_VFS_Type"),
		TUI.Menu.Entry(10, "Enable Directory Cache", "This settings allows the WebDAV Client to store the contents of folders. Useful if you're frequently accessing repeatedly the same folder.", Value=True, ID="Cache_DIR"),
			TUI.Menu.Entry(11, "Cache Duration", "Specify how long the directory cache should last before expiring.", Value="1h", ID="Cache_DIR_Value"),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(20, "Miscellaneous", Bold=True),
		TUI.Menu.Entry(11, "Pacer Minimum Sleep", "Specify the minimum time in milliseconds the WebDAV client should wait before sending a new request.", Value="0.01", Arguments=(r"[\d\.]",), ID="Misc_Pace"),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(1, f"Save Server", "Create a brand new entry with the provided information."),
		TUI.Menu.Entry(0, f"Cancel", "Return to the Menu with all your saved SSH Servers.", Function=Menu_Protocol, Arguments=("WebDAV",), Indentation=-2),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(1, f"Return to Main Menu", Function=Menu_Main)
	];
	uJSON: Type.uJSON_WebDAV = TUI.Menu.Interactive(Entries);
	if (uJSON):
		Register.WebDAV(uJSON);
		Menu_Protocol("WebDAV");

	Menu_Main();





def Menu_Wireguard_Create() -> None:
	Entries: TUI.Menu.Entries = [
		TUI.Menu.Entry(20, "Create Wireguard Connection", Bold=True),
		TUI.Menu.Entry(20, f"Notice: {App.Name} at this time is unable to create / edit / delete Wireguard Configurations."),
		TUI.Menu.Entry(20, "This WG functionality is simply present to regroup in one place every connections you may turn on / off."),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(11, "Server Name", "Specify a friendly name for you to remember this Wireguard Server.", ID="Tachibana_Name"),
		TUI.Menu.Entry(11, "Wireguard Adapter", "The name of the adapter in /etc/wireguard/*.conf", Value="wg0", ID="Adapter"),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(1, f"Save Server", "Create a brand new entry with the provided information."),
		TUI.Menu.Entry(0, f"Cancel", "Return to the Menu with all your saved SSH Servers.", Function=Menu_Protocol, Arguments=("Wireguard",), Indentation=-2),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(1, f"Return to Main Menu", Function=Menu_Main)
	];
	uJSON: Type.uJSON_Wireguard = TUI.Menu.Interactive(Entries);
	if (uJSON):
		Register.Wireguard(uJSON);
		Menu_Protocol("Wireguard");

	Menu_Main();










def Quit() -> None: TUI.Exit(); exit(0);
def Ignition() -> None:
	Log.Stateless("Loading Tachibana JSON...");

	# File Checks
	if (not Misc.All_Includes(Tachibana.keys(), ["_Version", "Config", "Servers"])):
		Data.Recreate();


	if (not type(Tachibana["_Version"]) is list): Data.Recreate();
	elif (not type(Tachibana["Config"]) is dict): Data.Recreate(); # pyright: ignore[reportUnnecessaryComparison]
	elif (not type(Tachibana["Servers"]) is dict): Data.Recreate();

	if (Misc.Under_At(Tachibana["_Version"], App.Version) == 0):
		# Upgrading version json logic here
		Log.Warning(f"{App.Name} was updated but the saved data is too old to function with this version! Attempting to upgrade...");
		File.JSON_Write(f"Tachibana-v{''.join(String.ify_Array(Tachibana['_Version']))}.bak", Tachibana);
		... # Upgrades will only be available after Tachibana v1.0

		File.JSON_Write("Tachibana.json", Tachibana);

	Log.Awaited().OK();

	TUI.Init();
	Menu_Main();


if (__name__ != "__main__"): TSN_Abstracter.Import_Unsupported();
else: TSN_Abstracter.App_Init(True); Ignition(); 