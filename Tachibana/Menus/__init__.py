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



def Menu_Profiles(Protocol: str, Address: str) -> None:
	if (Protocol in ["WebDAV", "Wireguard"]):
		TUI.Menu.Popup("Work in Progress", f"This function is currently unavailable for {Protocol} Servers.", TUI.Menu.Entry(12, Arguments=["Ok"]), "Left")
		Menu_Protocol(Protocol);

	Keybinds: TUI.Menu.Keybinds = [
		TUI.Menu.Keybind(100, "Delete Profile Entry", KB.Delete_Profile) # pyright: ignore[reportUnknownArgumentType]
	];
	while True:
		Profiles: TUI.Menu.Entries = Entries_Profiles(Protocol, Address);
		if (len(Profiles) == 1):
			Menu_Actions(*Profiles[0].Arguments);
			break;

		Entries: TUI.Menu.Entries = [
			TUI.Menu.Entry(20, f"{Protocol}:\\\\{Tachibana['Servers'][Protocol][Address]['Name']} - Profiles", Bold=True),
			*Profiles,
			TUI.Menu.Entry(20, ""),
			TUI.Menu.Entry(0, f"Return to all {Protocol} Entries", Function=Menu_Protocol, Arguments=[Protocol], Indentation=-2),
			TUI.Menu.Entry(0, f"Return to Main Menu", Function=MM.Main, Indentation=-2)
		];

		Stay: bool = TUI.Menu.Interactive(Entries, Keybinds);
		match (Stay):
			case True: continue;
			case _: MM.Main();



def Menu_Protocol(Protocol: str) -> None:
	Keybinds: TUI.Menu.Keybinds = [
		TUI.Menu.Keybind(100, "Delete Server Entry", KB.Delete_Server) # pyright: ignore[reportUnknownArgumentType]
	];
	while True:
		Entries: TUI.Menu.Entries = [
			TUI.Menu.Entry(20, f"{Protocol} - Connections", Bold=True),
			*Entries_Server(Protocol),
			TUI.Menu.Entry(20, ""),
			TUI.Menu.Entry(0, f"Register Server", f"Save a brand new {Protocol} server entry for {App.Name} to remember.", Function=Menu_Creation, Arguments=(Protocol,), Indentation=-2),
			TUI.Menu.Entry(0, f"Return to Main Menu", Function=MM.Main, Indentation=-2)
		];

		Stay: bool = TUI.Menu.Interactive(Entries, Keybinds);
		match (Stay):
			case True: continue;
			case _: MM.Main();



def Menu_Actions(Protocol: str, Address: str, Profile_Name: str) -> None:
	while True:
		Actions: TUI.Menu.Entries = [];

		match Protocol:
			case "SSH": Actions = mSSH.Actions(Address, Profile_Name);
			case _: pass;

		Entries: TUI.Menu.Entries = [
			TUI.Menu.Entry(20, f"{Protocol}:\\\\{Profile_Name}@{Tachibana['Servers'][Protocol][Address]['Name']} - Actions", Bold=True),
			TUI.Menu.Entry(20, ""),
			*Actions,
			TUI.Menu.Entry(20, ""),
			TUI.Menu.Entry(0, f"Edit Profile", f"Edit the entry for \"{Profile_Name}@{Address}\".", Function=MM.Main, Indentation=-2, Unavailable=True),
			TUI.Menu.Entry(0, f"Delete Profile", f"Delete the entry for \"{Profile_Name}@{Address}\".", Function=KB.Delete_Profile, Indentation=-2, Arguments=({"Protocol": Protocol, "Address": Address, "ID": Profile_Name},)),
			TUI.Menu.Entry(20, ""),
			TUI.Menu.Entry(0, f"Return to all {Tachibana['Servers'][Protocol][Address]['Name']} Profiles", f"Return to the Menu with all your saved profiles for {Address}.", Function=Menu_Profiles, Arguments=(Protocol, Address), Indentation=-2), # pyright: ignore[reportArgumentType]
			TUI.Menu.Entry(0, f"Return to all {Protocol} Servers", f"Return to the Menu with all your saved {Protocol} Servers.", Function=Menu_Protocol, Arguments=(Protocol,), Indentation=-2),
			TUI.Menu.Entry(0, f"Return to Main Menu", Function=MM.Main, Indentation=-2)
		];

		Stay = Type.uJSON_SSH = TUI.Menu.Interactive(Entries);
		if (not Stay): Menu_Profiles(Protocol, Address);





def Entries_Server(Protocol: str) -> TUI.Menu.Entries:
	Server_Entries: TUI.Menu.Entries = [];
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
					Function=Menu_Profiles, # pyright: ignore[reportArgumentType]
					Arguments=(Protocol, Server)
				));
	
	if (len(Server_Entries) == 0): Server_Entries.append(TUI.Menu.Entry(20, f"{App.Name} does not have any {Protocol} Servers saved, try registering one!", Unavailable=True));
	return Server_Entries;



def Entries_Profiles(Protocol: str, Address: str) -> TUI.Menu.Entries:
	Profile_Entries: TUI.Menu.Entries = [];
	Key: str;
	for Key in cast(Type.uJSON, Tachibana["Servers"][Protocol][Address]["Profiles"]).keys():
		Profile_Entries.append(
			TUI.Menu.Entry(
				0,
				Key,
				f"Connect to {Address} as {Key}",
				Key,
				Function=Menu_Actions, # pyright: ignore[reportArgumentType]
				Arguments=(Protocol, Address, Key)
			));

	return Profile_Entries;