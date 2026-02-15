from ..Globals import *;

def Delete_Server(Entry: TUI.Menu.Entry) -> bool:
	Description: str = f"Are you sure you want to delete {Entry.ID}?\n"

	if ("Profiles" in Tachibana["Servers"][Entry.Arguments[0]][Entry.Arguments[1]].keys()): # pyright: ignore[reportArgumentType]
		Description += f"This action will delete everything under \"{Entry.Arguments[1]}\" which, will in turn delete {len(Tachibana['Servers'][Entry.Arguments[0]][Entry.Arguments[1]]['Profiles'])} profiles.";
	else: Description += f"This action will delete internally \"{Entry.Arguments[1]}\"";
	
	if (Entry.ID and "Yes" == TUI.Menu.Popup(
		f"Confirm Deleting Server Entry",
		Description,
		TUI.Menu.Entry(12, Arguments=["Yes", "No"], Value="No")
	)):
		del Tachibana['Servers'][Entry.Arguments[0]][Entry.Arguments[1]];
		Data.Save();
	return True;


def Delete_Profile(Entry: TUI.Menu.Entry) -> bool:
	if (Entry.ID and "Yes" == TUI.Menu.Popup(
		f"Confirm Deleting Profile Entry",
		f"Are you sure you want to delete {Entry.ID}?\n",
		TUI.Menu.Entry(12, Arguments=["Yes", "No"], Value="No")
	)):
		del Tachibana['Servers'][Entry.Arguments[0]][Entry.Arguments[1]]["Profiles"][Entry.ID];
		Data.Save();
	return True;