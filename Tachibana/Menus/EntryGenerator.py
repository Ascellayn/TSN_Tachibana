from ..Globals import *;

import Tachibana.Menus.Templates as T;

def Servers(Protocol: str) -> TUI.Menu.Entries:
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
					TUI.Menu.Base_Box();
					# Progress Bar
					Bar: str = f"█" * round(
						(Count/len(Tachibana["Servers"][Protocol].keys()))
						* (TUI.curses.COLS - 2)
					);
					TUI.Window.addstr(TUI.curses.LINES - 2, 1, Bar);

					# Text Information
					TUI.Window.addstr(2, 3, String.Abbreviate(f"Pinging Servers... [{Count + 1}/{len(Tachibana["Servers"][Protocol].keys())}]", TUI.curses.COLS - 4));
					TUI.Window.addstr(3, 3, String.Abbreviate(f"> {Server}", TUI.curses.COLS - 4));
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
					Function=T.Profiles, # pyright: ignore[reportArgumentType]
					Arguments=(Protocol, Server)
				));
	
	if (len(Server_Entries) == 0): Server_Entries.append(TUI.Menu.Entry(20, f"{App.Name} does not have any {Protocol} Servers saved, try registering one!", Unavailable=True));
	return Server_Entries;





def Profiles(Protocol: str, Address: str) -> TUI.Menu.Entries:
	Profile_Entries: TUI.Menu.Entries = [];
	Key: str;
	for Key in cast(Type.uJSON, Tachibana["Servers"][Protocol][Address]["Profiles"]).keys():
		Profile_Entries.append(
			TUI.Menu.Entry(
				0,
				Key,
				f"Connect to {Address} as {Key}",
				Key,
				Function=T.Actions, # pyright: ignore[reportArgumentType]
				Arguments=(Protocol, Address, Key)
			));

	return Profile_Entries;