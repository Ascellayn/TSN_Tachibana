from ..Globals import *;
from .. import Register;
import Tachibana.Menus.Main as MM;
import Tachibana.Menus as M;

def Create() -> None:
	Entries: TUI.Menu.Entries = [
		TUI.Menu.Entry(20, "Create Wireguard Connection", Bold=True),
		TUI.Menu.Entry(20, f"Notice: {App.Name} at this time is unable to create / edit / delete Wireguard Configurations."),
		TUI.Menu.Entry(20, "This WG functionality is simply present to regroup in one place every connections you may turn on / off."),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(11, "Server Name", "Specify a friendly name for you to remember this Wireguard Server.", ID="Tachibana_Name", Required=True),
		TUI.Menu.Entry(11, "Wireguard Adapter", "The name of the adapter in /etc/wireguard/*.conf", Value="wg0", ID="Adapter", Required=True),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(1, f"Save Server", "Create a brand new entry with the provided information.", Required=True),
		TUI.Menu.Entry(0, f"Cancel", "Return to the Menu with all your saved SSH Servers.", Function=M.Menu_Protocol, Arguments=("Wireguard",), Indentation=-2),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(0, f"Return to Main Menu", Function=MM.Main, Indentation=-2)
	];
	uJSON: Type.uJSON_Wireguard = TUI.Menu.Interactive(Entries);
	if (uJSON):
		Register.Wireguard(uJSON);
		M.Menu_Protocol("Wireguard");

	MM.Main();