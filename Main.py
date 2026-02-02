from Tachibana import *;

def Ignition() -> None:
	Log.Stateless("Loading Tachibana JSON...");
	Tachibana: Type.Tachibana_JSON = cast(Type.Tachibana_JSON, File.JSON_Read("Tachibana.json"));

	# File Checks
	if (not Misc.All_Includes(Tachibana.keys(), ["_Version", "Config", "Servers"])):
		Data.Recreate();


	if (not type(Tachibana["_Version"]) is list): Data.Recreate();
	elif (not type(Tachibana["Config"]) is dict): Data.Recreate();
	elif (not type(Tachibana["Servers"]) is dict): Data.Recreate();

	if (Misc.Under_At(Tachibana["_Version"], App.Version) == 0):
		# Upgrading version json logic here
		Log.Warning(f"{App.Name} was updated but the saved data is too old to function with this version! Attempting to upgrade...");
		File.JSON_Write(f"Tachibana-v{''.join(String.ify_Array(Tachibana['_Version']))}.bak", Tachibana);
		...

		File.JSON_Write("Tachibana.json", Tachibana);

	Log.Awaited().OK();



if (__name__ != "__main__"): TSN_Abstracter.Import_Unsupported();
else: TSN_Abstracter.App_Init(True); Ignition(); 