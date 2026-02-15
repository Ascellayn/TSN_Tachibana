from ..Globals import *;
import Tachibana.Menus.SSH as mSSH;
import Tachibana.Menus as M;
import Tachibana.Menus.Settings as MS;

def Quit() -> None: TUI.Exit(); exit(0);
def Main() -> None:
	Favorites: list[TUI.Menu.Entry] = [
		TUI.Menu.Entry(0, "Create new SSH Connection", f"Save a brand new SSH server entry for {App.Name} to remember.", Function=mSSH.Create),
	]
	Entries: TUI.Menu.Entries = [
		TUI.Menu.Entry(20, "Welcome to Tachibana, the Server Connection Manager of Adellian."),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(20, "Quick Actions", Bold=True),
		*Favorites,
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(20, "Server Protocols", Bold=True),
		TUI.Menu.Entry(0, "Secure Shell Server", f"Access the SSH Servers that {App.Name} has saved.", Function=M.Menu_Protocol, Arguments=("SSH",)),
		TUI.Menu.Entry(0, "WebDAV", f"Access the WebDAV Servers that {App.Name} has saved.", Function=M.Menu_Protocol, Arguments=("WebDAV",)),
		TUI.Menu.Entry(0, "Wireguard", f"Access the Wireguard Servers that {App.Name} has saved.", Function=M.Menu_Protocol, Arguments=("Wireguard",)),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(0, "Settings", f"Configure {App.Name} to your liking.", Function=MS.Settings, Indentation=-2),
		TUI.Menu.Entry(0, f"Exit {App.Name}", "Your train will always be waiting for you, see you next time!", Function=Quit, Indentation=-2)
	];
	TUI.Menu.Interactive(Entries);