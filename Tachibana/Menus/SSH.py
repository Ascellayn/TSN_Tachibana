from ..Globals import *;
from .. import Register;
import Tachibana.Menus.Main as MM;
import Tachibana.Menus as M;

def Create() -> None:
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
		TUI.Menu.Entry(0, f"Cancel", "Return to the Menu with all your saved SSH Servers.", Function=M.Menu_Protocol, Arguments=("SSH",), Indentation=-2),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(0, f"Return to Main Menu", Function=MM.Main, Indentation=-2)
	];
	uJSON: Type.uJSON_SSH = TUI.Menu.Interactive(Entries);
	if (uJSON):
		Register.SSH(uJSON);
		M.Menu_Protocol("SSH");

	MM.Main();