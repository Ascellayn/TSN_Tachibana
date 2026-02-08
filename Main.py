from Tachibana import *;










def Quit(Entries: TUI.Menu.Entries | None) -> None:
	TUI.Exit(); exit(0);




def Menu_SSH_Create(*args: Any) -> None:
	Entries: TUI.Menu.Entries = [
		TUI.Menu.Entry(20, "Create SSH Connection", Bold=True),
		TUI.Menu.Entry(11, "Server Name", "Specify a friendly name for you to remember this SSH Server."),
		TUI.Menu.Entry(11, "Server Address", "Specify the IP Address or Hostname the SSH Server is on."),
		TUI.Menu.Entry(11, "Server Port", "Specify which port the SSH Server is on.", Value="22"),
		TUI.Menu.Entry(11, "Username", "The username we should log on as.", Value="root"),
		TUI.Menu.Entry(11, "Password", "The password we should use to login."),
		TUI.Menu.Entry(11, "SSH Key", "An absolute path to an SSH Key we should use.", Value="~/.ssh/id_rsa"),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(20, "SFTP Settings", Bold=True, Indentation=1),
		TUI.Menu.Entry(11, "Remote Folder", "Specify the folder you'd like to access from the Server remotely.", Value="/", Indentation=1),
		TUI.Menu.Entry(11, "Local Folder", "Specify a place in your filesystem where you would like to mount the remote folder.", Value="/media/SFTP", Indentation=1),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(20, "Workarounds", Bold=True),
		TUI.Menu.Entry(10, "Spoof Terminal", "Enable to spoof to the Server which Terminal you are using. Useful if the Server does not support your Terminal."),
			TUI.Menu.Entry(11, "Exported Terminal", "Increases compatibility if your Server does not support your Terminal.", 1, Value="xterm-256color"),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(1, f"Save Server", "Create a brand new entry with the provided information.", Unavailable=True, Function=Menu_Main),
		TUI.Menu.Entry(1, f"Cancel", "Return to the Menu with all your saved SSH Servers.", Function=Menu_SSH),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(1, f"Return to Main Menu", Function=Menu_Main)
	];
	TUI.Menu.Interactive(Entries);
	Menu_Main();


def Menu_SSH(*args: Any) -> None:
	Entries: TUI.Menu.Entries = [
		TUI.Menu.Entry(20, "Secure Shell Server - Connections", Bold=True),
		TUI.Menu.Entry(20, "TO BE DONE - DISPLAY SERVERS PER NAME / ADDRESS"),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(1, f"Register New Server", "Register a brand new SSH Server.", Function=Menu_SSH_Create),
		TUI.Menu.Entry(1, f"Return to Main Menu", Function=Menu_Main)
	];
	TUI.Menu.Interactive(Entries);
	Menu_Main();





def Menu_Main(*args: Any) -> None:
	Entries: TUI.Menu.Entries = [
		TUI.Menu.Entry(20, "Welcome to Tachibana, the Server Connection Manager of Adellian."),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(20, "Quick Actions", Bold=True),
		TUI.Menu.Entry(0, "Create new SSH Connection", Function=Menu_SSH_Create),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(20, "Server Protocols", Bold=True),
		TUI.Menu.Entry(0, "Secure Shell Server", Function=Menu_SSH),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(1, f"Exit {App.Name}", "Your train will always be waiting for you, see you next time!", Function=Quit)
	];
	TUI.Menu.Interactive(Entries);
	Quit(None);











def Ignition() -> None:
	Log.Stateless("Loading Tachibana JSON...");
	Tachibana: Type.Tachibana_JSON = cast(Type.Tachibana_JSON, File.JSON_Read("Tachibana.json"));

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