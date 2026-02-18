from ..Globals import *;
from .. import Register;
import Tachibana.Menus.Main as MM;

def Settings() -> None:
	Entries: TUI.Menu.Entries = [
		TUI.Menu.Entry(20, f"{App.Name} Settings", Bold=True),
		TUI.Menu.Entry(10, "Keep Servers Mounted", f"Allow {App.Name} to keep mounts alive if the Terminal {App.Name} was ran on gets closed.", "Mounts_Keep_Open", 0, Value=Safe.Nested_Dict(cast(dict[str, Any], Tachibana["Config"]), ["Mounts"], True), Unavailable=True),
		TUI.Menu.Entry(20, ""),
			TUI.Menu.Entry(20, "Per-Protocol Settings", Bold=True, Indentation=1),
				TUI.Menu.Entry(20, "SSH", Bold=True, Indentation=2),
				TUI.Menu.Entry(10, "Ping Servers", f"Allow {App.Name} to automatically mesure latency when you are selecting a server.", "Server_SSH_Ping", 1, Value=Safe.Nested_Dict(cast(dict[str, Any], Tachibana["Config"]), ["Servers", "SSH", "Ping"], True)),
				TUI.Menu.Entry(11, "SSH Binary", "Specify the executable to use when attempting to create SSH Connections.", "Server_SSH_Binary_SSH", 1, Value=Safe.Nested_Dict(cast(dict[str, Any], Tachibana["Config"]), ["Servers", "SSH", "Binary_SSH"], "/bin/ssh"), Required=True),
				TUI.Menu.Entry(11, "SSHFS Binary", "Specify the executable to use when attempting to mount SSHFS Connections.", "Server_SSH_Binary_SSHFS", 1, Value=Safe.Nested_Dict(cast(dict[str, Any], Tachibana["Config"]), ["Servers", "SSH", "Binary_SSHFS"], "/bin/sshfs"), Required=True),
		TUI.Menu.Entry(20, ""),
				TUI.Menu.Entry(20, "WebDAV", Bold=True, Indentation=2),
				TUI.Menu.Entry(10, "Ping Servers", f"Allow {App.Name} to automatically mesure latency when you are selecting a server.", "Server_WebDAV_Ping", 1, Value=Safe.Nested_Dict(cast(dict[str, Any], Tachibana["Config"]), ["Servers", "WebDAV", "Ping"], True)),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(1, f"Save Configuration", "Save all your settings visually present on this page.", Required=True),
		TUI.Menu.Entry(0, f"Return to Main Menu", Function=MM.Main, Indentation=-2)
	];
	uJSON: Type.uJSON_Config = TUI.Menu.Interactive(Entries);
	if (uJSON):
		Register.Tachibana_Config(uJSON);
		MM.Main();
	TUI.Menu.Interactive(Entries);
	MM.Main();