from Tachibana import *;










def Quit() -> None:
	TUI.Exit(); exit(0);



def Menu_Entries(Protocol: str) -> list[TUI.Menu.Entry]:
	Server_Entries: list[TUI.Menu.Entry] = [];
	if (Protocol in Tachibana["Servers"].keys()):
		for Server in Tachibana["Servers"][Protocol].keys():
			Server_Entries.append(TUI.Menu.Entry(0, f"{Tachibana["Servers"][Protocol][Server]["Name"]}", f"{App.Name} knows this Server Internally as \"{Server}\".", Unavailable=True));
	
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
		TUI.Menu.Entry(1, f"Save Server", "Create a brand new entry with the provided information.", Unavailable=True),
		TUI.Menu.Entry(0, f"Cancel", "Return to the Menu with all your saved SSH Servers.", Function=Menu_SSH, Indentation=-2),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(0, f"Return to Main Menu", Function=Menu_Main, Indentation=-2)
	];
	uJSON: dict[str, Any] = TUI.Menu.Interactive(Entries);
	if (uJSON):
		Menu_SSH();

	Menu_Main();



def Menu_WebDAV_Create() -> None:
	Entries: TUI.Menu.Entries = [
		TUI.Menu.Entry(20, "Create WebDAV Connection", Bold=True),
		TUI.Menu.Entry(11, "Server Name", "Specify a friendly name for you to remember this WebDAV Server. Will overwrite the name if a server with the same URL and Protocol already exists.", ID="Tachibana_Name"),
		TUI.Menu.Entry(11, "WebDAV Name", "Specify a name used by the WebDAV Configurator.", ID="WebDAV_Name"),
		TUI.Menu.Entry(11, "Server URL", "Specify the URL of the WebDAV Server.", ID="Server_URL"),
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
		TUI.Menu.Entry(11, "Pacer Minimum Sleep", "Specify the minimum time in milliseconds the WebDAV client should wait before sending a new request.", Value="0.01", Arguments=(r"[\d\.]",), ID="Pace"),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(1, f"Save Server", "Create a brand new entry with the provided information.", Unavailable=True, Function=Menu_Main),
		TUI.Menu.Entry(0, f"Cancel", "Return to the Menu with all your saved SSH Servers.", Function=Menu_WebDAV, Indentation=-2),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(1, f"Return to Main Menu", Function=Menu_Main)
	];
	uJSON: dict[str, Any] = TUI.Menu.Interactive(Entries);
	if (uJSON):
		Menu_WebDAV();
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
		TUI.Menu.Entry(1, f"Save Server", "Create a brand new entry with the provided information.", Function=Menu_Main),
		TUI.Menu.Entry(0, f"Cancel", "Return to the Menu with all your saved SSH Servers.", Function=Menu_Wireguard, Indentation=-2),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(1, f"Return to Main Menu", Function=Menu_Main)
	];
	uJSON: uJSON_Wireguard = TUI.Menu.Interactive(Entries);
	if (uJSON):
		Register.Wireguard(uJSON);
		Menu_Wireguard();

	Menu_Main();





def Menu_SSH() -> None:
	Entries: TUI.Menu.Entries = [
		TUI.Menu.Entry(20, "Secure Shell Server - Connections", Bold=True),
		*Menu_Entries("SSH"),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(0, f"Register New Server", "Register a brand new SSH Server.", Function=Menu_SSH_Create, Indentation=-2),
		TUI.Menu.Entry(0, f"Return to Main Menu", Function=Menu_Main, Indentation=-2)
	];
	TUI.Menu.Interactive(Entries);
	Menu_Main();

def Menu_WebDAV() -> None:
	Entries: TUI.Menu.Entries = [
		TUI.Menu.Entry(20, "WebDAV - Connections", Bold=True),
		*Menu_Entries("WebDAV"),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(0, f"Register New Server", "Register a brand new WebDAV Server.", Function=Menu_WebDAV_Create, Indentation=-2),
		TUI.Menu.Entry(0, f"Return to Main Menu", Function=Menu_Main, Indentation=-2)
	];
	TUI.Menu.Interactive(Entries);
	Menu_Main();

def Menu_Wireguard() -> None:
	Entries: TUI.Menu.Entries = [
		TUI.Menu.Entry(20, "Wireguard - Connections", Bold=True),
		*Menu_Entries("Wireguard"),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(0, f"Register New Adapter", "Register a brand new Wireguard Adapter.", Function=Menu_Wireguard_Create, Indentation=-2),
		TUI.Menu.Entry(0, f"Return to Main Menu", Function=Menu_Main, Indentation=-2)
	];
	TUI.Menu.Interactive(Entries);
	Menu_Main();





def Menu_Main() -> None:
	Entries: TUI.Menu.Entries = [
		TUI.Menu.Entry(20, "Welcome to Tachibana, the Server Connection Manager of Adellian."),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(20, "Quick Actions", Bold=True),
		TUI.Menu.Entry(0, "Create new SSH Connection", Function=Menu_SSH_Create),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(20, "Server Protocols", Bold=True),
		TUI.Menu.Entry(0, "Secure Shell Server", Function=Menu_SSH),
		TUI.Menu.Entry(0, "WebDAV", Function=Menu_WebDAV),
		TUI.Menu.Entry(0, "Wireguard", Function=Menu_Wireguard),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(0, f"Exit {App.Name}", "Your train will always be waiting for you, see you next time!", Function=Quit, Indentation=-2)
	];
	TUI.Menu.Interactive(Entries);
	Quit();











def Ignition() -> None:
	Log.Stateless("Loading Tachibana JSON...");

	# File Checks
	if (not Misc.All_Includes(Tachibana.keys(), ["_Version", "Config", "Servers"])):
		Data.Recreate();


	if (not type(Tachibana["_Version"]) is list): Data.Recreate();
	elif (not type(Tachibana["Config"]) is dict): Data.Recreate();
	elif (not type(Tachibana["Servers"]) is dict): Data.Recreate();

	if (Misc.Under_At(Tachibana["_Version"], App.Version) == 0):
		# Upgrading version json logic here
		Log.Warning(f"{App.Name} was updated but the saved data is too old to function with this version! Attempting to upgrade...");
		File.JSON_Write(f"Tachibana-v{''.join(String.ify_Array(Tachibana['_Version']))}.bak", Tachibana);
		...

		File.JSON_Write("Tachibana.json", Tachibana);

	Log.Awaited().OK();

	TUI.Init();
	Menu_Main();


if (__name__ != "__main__"): TSN_Abstracter.Import_Unsupported();
else: TSN_Abstracter.App_Init(True); Ignition(); 