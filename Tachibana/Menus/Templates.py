from ..Globals import *;
from .. import Register;

import Tachibana.Menus.EntryGenerator as EG;

import Tachibana.Menus.Main as MM;
import Tachibana.Menus.Keybinds as KB;

import Tachibana.Menus.SSH as mSSH;
import Tachibana.Menus.WebDAV as mWebDAV;
import Tachibana.Menus.Wireguard as mWireguard;



def Create(Protocol: str) -> None:
	match Protocol:
		case "SSH": Parameters: tuple[TUI.Menu.Entries, TUI.Menu.Entries] = mSSH.Create;
		case "WebDAV": Parameters: tuple[TUI.Menu.Entries, TUI.Menu.Entries] = mWebDAV.Create;
		case "Wireguard": Parameters: tuple[TUI.Menu.Entries, TUI.Menu.Entries] = mWireguard.Create;
		case _:
			TUI.Menu.Popup("Unknown Protocol", f"Tachibana → Menu → Create: Unhandled Protocol \"{Protocol}\".", Entry=TUI.Menu.Entry(12, Arguments=["Return to Main Menu"]));
			raise ValueError(f"Unknown Protocol: {Protocol}");

	Entries: TUI.Menu.Entries = [
		TUI.Menu.Entry(20, f"Create {Protocol} Connection", Bold=True),
		*Parameters[0],
		TUI.Menu.Entry(11, "Server Name", "Specify a friendly name for you to remember this SSH Server. Will overwrite the name if a server with the same Address, Port and Protocol already exists.", ID="Tachibana_Name", Required=True),
		*Parameters[1],
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(1, f"Save Server", "Create a brand new entry with the provided information.", Required=True),
		TUI.Menu.Entry(0, f"Cancel", "Return to the Menu with all your saved SSH Servers.", Function=Servers, Arguments=("SSH",), Indentation=-2),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(0, f"Return to Main Menu", Function=MM.Main, Indentation=-2)
	];

	uJSON: Type.uJSON = TUI.Menu.Interactive(Entries);
	if (not uJSON): MM.Main();

	match Protocol:
		case "SSH": Register.SSH(uJSON); # type: ignore
		case "WebDAV": Register.WebDAV(uJSON); # type: ignore
		case "Wireguard": Register.Wireguard(uJSON); # type: ignore
		case _:
			TUI.Menu.Popup("Unknown Protocol", f"Tachibana → Menu → Create: Unhandled Protocol \"{Protocol}\".", Entry=TUI.Menu.Entry(12, Arguments=["Return to Main Menu"]));
			raise ValueError(f"Unknown Protocol: {Protocol}");
	Servers(Protocol);
	





def Servers(Protocol: str, Index: int = 0) -> None:
	Keybinds: TUI.Menu.Keybinds = [
		TUI.Menu.Keybind(100, "Delete Server Entry", KB.Delete_Server) # pyright: ignore[reportUnknownArgumentType]
	];
	while True:
		Entries: TUI.Menu.Entries = [
			TUI.Menu.Entry(20, f"{Protocol} - Connections", Bold=True),
			*EG.Servers(Protocol),
			TUI.Menu.Entry(20, ""),
			TUI.Menu.Entry(0, f"Register Server", f"Save a brand new {Protocol} server entry for {App.Name} to remember.", Function=Create, Arguments=(Protocol,), Indentation=-2),
			TUI.Menu.Entry(0, f"Return to Main Menu", Function=MM.Main, Indentation=-2)
		];

		Stay: bool = TUI.Menu.Interactive(Entries, Keybinds, Index);
		match (Stay):
			case True: continue;
			case _: MM.Main();





def Profiles(Protocol: str, Address: str, Index: int = 0) -> None:
	if (Protocol in ["WebDAV", "Wireguard"]):
		TUI.Menu.Popup("Work in Progress", f"This function is currently unavailable for {Protocol} Servers.", TUI.Menu.Entry(12, Arguments=["Ok"]), "Left")
		Servers(Protocol);

	Keybinds: TUI.Menu.Keybinds = [
		TUI.Menu.Keybind(100, "Delete Profile Entry", KB.Delete_Profile) # pyright: ignore[reportUnknownArgumentType]
	];
	while True:
		Profiles: TUI.Menu.Entries = EG.Profiles(Protocol, Address);
		if (len(Profiles) == 1):
			Actions(*Profiles[0].Arguments);
			break;

		Entries: TUI.Menu.Entries = [
			TUI.Menu.Entry(20, f"{Protocol}:\\\\{Tachibana['Servers'][Protocol][Address]['Name']} - Profiles", Bold=True),
			*Profiles,
			TUI.Menu.Entry(20, ""),
			TUI.Menu.Entry(0, f"Return to all {Protocol} Entries", Function=Servers, Arguments=(Protocol, Index), Indentation=-2),
			TUI.Menu.Entry(0, f"Return to Main Menu", Function=MM.Main, Indentation=-2)
		];

		Stay: bool = TUI.Menu.Interactive(Entries, Keybinds, Index);
		match (Stay):
			case True: continue;
			case _: MM.Main();





def Actions(Protocol: str, Address: str, Profile_Name: str) -> None:
	while True:
		Actions: TUI.Menu.Entries = [];

		match Protocol:
			case "SSH": Actions = mSSH.Actions(Address, Profile_Name);
			case _: pass;
		
		Profiles_Disabled: bool = True if (len(Tachibana["Servers"][Protocol][Address]["Profiles"]) == 1) else False; # pyright: ignore[reportUnknownArgumentType]
		indexProfile: int = 1;
		for pIndex, Profile in enumerate(Tachibana["Servers"][Protocol][Address]["Profiles"].keys()): # type: ignore
			if (Profile == Profile_Name):
				indexProfile = 1 + pIndex;
		

		indexServer: int = 1;
		for sIndex, Server in enumerate(Tachibana["Servers"][Protocol].keys()): # type: ignore
			if (Server == Address):
				indexServer = 1 + sIndex;

		Entries: TUI.Menu.Entries = [
			TUI.Menu.Entry(20, f"{Protocol}:\\\\{Profile_Name}@{Tachibana['Servers'][Protocol][Address]['Name']} - Actions", Bold=True),
			TUI.Menu.Entry(20, ""),
			*Actions,
			TUI.Menu.Entry(20, ""),
			TUI.Menu.Entry(0, f"Edit Profile", f"Edit the entry for \"{Profile_Name}@{Address}\".", Function=MM.Main, Indentation=-2, Unavailable=True),
			TUI.Menu.Entry(0, f"Delete Profile", f"Delete the entry for \"{Profile_Name}@{Address}\".", Function=KB.Delete_Profile, Indentation=-2, Arguments=({"Protocol": Protocol, "Address": Address, "ID": Profile_Name},)),
			TUI.Menu.Entry(20, ""),
			TUI.Menu.Entry(0, f"Return to all {Tachibana['Servers'][Protocol][Address]['Name']} Profiles", f"Return to the Menu with all your saved profiles for {Address}.", Function=Profiles, Arguments=(Protocol, Address, indexProfile), Indentation=-2, Unavailable=Profiles_Disabled), # pyright: ignore[reportArgumentType]
			TUI.Menu.Entry(0, f"Return to all {Protocol} Servers", f"Return to the Menu with all your saved {Protocol} Servers.", Function=Servers, Arguments=(Protocol, indexServer), Indentation=-2),
			TUI.Menu.Entry(0, f"Return to Main Menu", Function=MM.Main, Indentation=-2)
		];

		Stay = Type.uJSON_SSH = TUI.Menu.Interactive(Entries);
		if (not Stay): Profiles(Protocol, Address, indexProfile);