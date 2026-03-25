from ..Globals import *;
from .. import Register;

import Tachibana.Menus.EntryGenerator as EG;

import Tachibana.Menus.Main as MM;
import Tachibana.Menus.Keybinds as KB;

import Tachibana.Menus.SSH as mSSH;
import Tachibana.Menus.WebDAV as mWebDAV;
import Tachibana.Menus.Wireguard as mWireguard;



def __Get_Parameters(Protocol: str) -> tuple[TUI.Entries, TUI.Entries]:
	match Protocol:
		case "SSH": return mSSH.Create;
		case "WebDAV": return mWebDAV.Create;
		case "Wireguard": return mWireguard.Create;
		case _:
			TUI.Prompt("Unknown Protocol", f"Tachibana → Menu → Create: Unhandled Protocol \"{Protocol}\".", Entry=TUI.Entry(12, Arguments=["Return to Main Menu"]));
			raise ValueError(f"Unknown Protocol: {Protocol}");


def __Get_Base(Protocol: str, Parameters: tuple[TUI.Entries, TUI.Entries]) -> TUI.Entries:
	return [
		TUI.Entry(20, f"Create {Protocol} Connection", Bold=True),
		*Parameters[0],
		TUI.Entry(10, "Ping Server", "Allow Tachibana to automatically ping this server to acquire latency information.", ID="Tachibana_Ping", Value=True),
		TUI.Entry(11, "Server Name", f"Specify a friendly name for you to remember this {Protocol} Server. Will overwrite the name if a server with the same Address, Port and Protocol already exists.", ID="Tachibana_Name", Required=True),
		*Parameters[1],
		TUI.Entry(20, ""),
		TUI.Entry(1, f"Save Server", "Create a brand new entry with the provided information.", Required=True),
		TUI.Entry(0, f"Cancel", f"Return to the Menu with all your saved {Protocol} Servers.", Function=Servers, Arguments=("SSH",), Indentation=-2),
		TUI.Entry(20, ""),
		TUI.Entry(0, f"Return to Main Menu", Function=MM.Main, Indentation=-2)
	];


def __Register(Protocol: str, uJSON: Type.uJSON) -> None:
	match Protocol:
		case "SSH": Register.SSH(uJSON); # type: ignore
		case "WebDAV": Register.WebDAV(uJSON); # type: ignore
		case "Wireguard": Register.Wireguard(uJSON); # type: ignore
		case _:
			TUI.Prompt("Unknown Protocol", f"Tachibana → Menu → Create: Unhandled Protocol \"{Protocol}\".", Entry=TUI.Entry(12, Arguments=["Return to Main Menu"]));
			raise ValueError(f"Unknown Protocol: {Protocol}");
	Servers(Protocol);



def Create(Protocol: str, Entries: TUI.Entries | None = None) -> None: # pyright: ignore[reportRedeclaration]
	if (not Entries):
		Entries: TUI.Entries = __Get_Base(Protocol, __Get_Parameters(Protocol))

	uJSON: Type.uJSON = TUI.Menu(Entries);
	if (not uJSON): MM.Main();

	__Register(Protocol, uJSON);
	Servers(Protocol);



def Edit(Protocol: str, Address: str, Profile_Name: str) -> bool:
	Entries: TUI.Entries = __Get_Base(Protocol, __Get_Parameters(Protocol));
	Profile: dict[str, Any] = cast(dict[str, Any], Tachibana["Servers"][Protocol][Address]["Profiles"][Profile_Name]);

	Profile["Tachibana_Ping"] = Tachibana["Servers"][Protocol][Address]["Ping"];
	Profile["Tachibana_Name"] = Tachibana["Servers"][Protocol][Address]["Name"];

	for Entry in Entries:
		for Key, Value in Profile.items():
			if (Entry.ID == Key):
				Entry.Value = Value;

	uJSON: Type.uJSON = TUI.Menu(Entries);
	if (not uJSON): return True;

	KB.Delete_Profile({
		"Protocol": Protocol,
		"Address": Address,
		"ID": Profile_Name
	}, True);
	__Register(Protocol, uJSON);

	return True;
#





def Servers(Protocol: str, Index: int = 0) -> None:
	Keybinds: TUI.Keybinds = [
		TUI.Keybind(100, "Delete Server Entry", KB.Delete_Server), # pyright: ignore[reportUnknownArgumentType]
		TUI.Keybind(117, "Refresh Servers", KB.Refresh_Servers) # pyright: ignore[reportUnknownArgumentType]
	];
	while True:
		Entries: TUI.Entries = [
			TUI.Entry(20, f"{Protocol} - Connections", Bold=True),
			*EG.Servers(Protocol),
			TUI.Entry(20, ""),
			TUI.Entry(0, f"Register Server", f"Save a brand new {Protocol} server entry for {App.Name} to remember.", Function=Create, Arguments=(Protocol,), Indentation=-2),
			TUI.Entry(0, f"Return to Main Menu", Function=MM.Main, Indentation=-2)
		];

		Stay: bool = TUI.Menu(Entries, Keybinds, Index);
		match (Stay):
			case True: continue;
			case _: MM.Main();





def Profiles(Protocol: str, Address: str, Index: int = 0) -> None:
	if (Protocol in ["Wireguard"]):
		TUI.Prompt("Work in Progress", f"This function is currently unavailable for {Protocol} Servers.", TUI.Entry(12, Arguments=["Ok"]), "Left")
		Servers(Protocol);

	Keybinds: TUI.Keybinds = [
		TUI.Keybind(100, "Delete Profile Entry", KB.Delete_Profile) # pyright: ignore[reportUnknownArgumentType]
	];
	while True:
		Profiles: TUI.Entries = EG.Profiles(Protocol, Address);
		if (len(Profiles) == 1):
			Actions(*Profiles[0].Arguments);
			break;

		Entries: TUI.Entries = [
			TUI.Entry(20, f"{Protocol}:\\\\{Tachibana['Servers'][Protocol][Address]['Name']} - Profiles", Bold=True),
			*Profiles,
			TUI.Entry(20, ""),
			TUI.Entry(0, f"Return to all {Protocol} Entries", Function=Servers, Arguments=(Protocol, Index), Indentation=-2),
			TUI.Entry(0, f"Return to Main Menu", Function=MM.Main, Indentation=-2)
		];

		Stay: bool = TUI.Menu(Entries, Keybinds, Index);
		match (Stay):
			case True: continue;
			case _: MM.Main();





def Actions(Protocol: str, Address: str, Profile_Name: str) -> None:
	while True:
		Actions: TUI.Entries = [];

		match Protocol:
			case "SSH": Actions = mSSH.Actions(Address, Profile_Name);
			case "WebDAV": Actions = mWebDAV.Actions(Address, Profile_Name);
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

		Entries: TUI.Entries = [
			TUI.Entry(20, f"{Protocol}:\\\\{Profile_Name}@{Tachibana['Servers'][Protocol][Address]['Name']} - Actions", Bold=True),
			TUI.Entry(20, ""),
			*Actions,
			TUI.Entry(20, ""),
			TUI.Entry(0, f"Edit Profile", f"Edit the entry for \"{Profile_Name}@{Address}\".", Function=Edit, Indentation=-2, Arguments=(Protocol, Address, Profile_Name)), # pyright: ignore[reportArgumentType]
			TUI.Entry(0, f"Delete Profile", f"Delete the entry for \"{Profile_Name}@{Address}\".", Function=KB.Delete_Profile, Indentation=-2, Arguments=({"Protocol": Protocol, "Address": Address, "ID": Profile_Name},)),
			TUI.Entry(20, ""),
			TUI.Entry(0, f"Return to all {Tachibana['Servers'][Protocol][Address]['Name']} Profiles", f"Return to the Menu with all your saved profiles for {Address}.", Function=Profiles, Arguments=(Protocol, Address, indexProfile), Indentation=-2, Unavailable=Profiles_Disabled), # pyright: ignore[reportArgumentType]
			TUI.Entry(0, f"Return to all {Protocol} Servers", f"Return to the Menu with all your saved {Protocol} Servers.", Function=Servers, Arguments=(Protocol, indexServer), Indentation=-2),
			TUI.Entry(0, f"Return to Main Menu", Function=MM.Main, Indentation=-2)
		];

		Stay = Type.uJSON_SSH = TUI.Menu(Entries);
		if (not Stay): Profiles(Protocol, Address, indexProfile);