from Tachibana import *;
from Tachibana.Menus import *;

def Ignition() -> None:
	Log.Stateless("Loading Tachibana JSON...");

	# File Checks
	if (not Misc.All_Includes(Tachibana.keys(), ["_Version", "Config", "Servers"])):
		Data.Recreate();


	if (not type(Tachibana["_Version"]) is list): Data.Recreate();
	elif (not type(Tachibana["Config"]) is dict): Data.Recreate(); # pyright: ignore[reportUnnecessaryComparison]
	elif (not type(Tachibana["Servers"]) is dict): Data.Recreate();

	if (Misc.Under_At(Tachibana["_Version"], App.Version) == 0):
		# Upgrading version json logic here
		Log.Warning(f"{App.Name} was updated but the saved data is too old to function with this version! Attempting to upgrade...");
		File.JSON_Write(f"Tachibana-v{''.join(String.ify_Array(Tachibana['_Version']))}.bak", Tachibana);
		... # Upgrades will only be available after Tachibana v1.0

		File.JSON_Write("Tachibana.json", Tachibana);

	Log.Awaited().OK();

	TUI.Init();
	MM.Main();


if (__name__ != "__main__"): TSN_Abstracter.Import_Unsupported();
else: TSN_Abstracter.App_Init(True); Ignition();