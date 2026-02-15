from ..Globals import *;

import Tachibana.Menus.Main as MM;
import Tachibana.Menus.Keybinds as KB;

import Tachibana.Menus.SSH as mSSH;
import Tachibana.Menus.WebDAV as mWebDAV;
import Tachibana.Menus.Wireguard as mWireguard;



def Menu_Creation(Protocol: str) -> None:
	match Protocol:
		case "SSH": mSSH.Create();
		case "WebDAV": mWebDAV.Create();
		case "Wireguard": mWireguard.Create();
		case _: MM.Main();

def Profile_Orchestrator(Protocol: str, Address: str) -> None:
	match Protocol:
		case "SSH": TUI.Menu.Popup("Work in Progress", "This function is currently unavailable.", TUI.Menu.Entry(12, Arguments=["Ok"]), "Left");
		case "WebDAV": TUI.Menu.Popup("Work in Progress", "This function is currently unavailable.", TUI.Menu.Entry(12, Arguments=["Ok"]), "Left");
		case "Wireguard": TUI.Menu.Popup("Work in Progress", "This function is currently unavailable.", TUI.Menu.Entry(12, Arguments=["Ok"]), "Left");
		case _: pass;
	Menu_Protocol(Protocol);



def Menu_Protocol(Protocol: str) -> None:
	Keybinds: TUI.Menu.Keybinds = [
		TUI.Menu.Keybind(100, "Delete Server Entry", KB.Keybind_Delete_Server) # pyright: ignore[reportUnknownArgumentType]
	];
	while True:
		Entries: TUI.Menu.Entries = [
			TUI.Menu.Entry(20, f"{Protocol} - Connections", Bold=True),
			*Menu_Entries(Protocol),
			TUI.Menu.Entry(20, ""),
			TUI.Menu.Entry(0, f"Register Server", f"Save a brand new {Protocol} server entry for {App.Name} to remember.", Function=Menu_Creation, Arguments=(Protocol,), Indentation=-2),
			TUI.Menu.Entry(0, f"Return to Main Menu", Function=MM.Main, Indentation=-2)
		];

		Stay: bool = TUI.Menu.Interactive(Entries, Keybinds);
		match (Stay):
			case True: continue;
			case _: MM.Main();





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
					Function=Profile_Orchestrator, # pyright: ignore[reportArgumentType]
					Arguments=(Protocol, Server)
				));
	
	if (len(Server_Entries) == 0): Server_Entries.append(TUI.Menu.Entry(20, f"{App.Name} does not have any {Protocol} Servers saved, try registering one!", Unavailable=True));
	return Server_Entries;