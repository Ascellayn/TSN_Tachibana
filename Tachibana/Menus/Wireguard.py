from ..Globals import *;
import subprocess;





Create: tuple[TUI.Menu.Entries, TUI.Menu.Entries] = (
	[
		TUI.Menu.Entry(20, f"Notice: {App.Name} at this time is unable to create / edit / delete Wireguard Configurations."),
		TUI.Menu.Entry(20, "This WG functionality is simply present to regroup in one place every connections you may turn on / off."),
		TUI.Menu.Entry(20, "")
	],
	[
		TUI.Menu.Entry(11, "Wireguard Adapter", "The name of the adapter in /etc/wireguard/*.conf", Value="wg0", ID="Adapter", Required=True),
	]
);