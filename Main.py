from Tachibana import *;

def Ignition() -> None:
	Log.Stateless("Loading Tachibana JSON...");
	Tachibana: Type.Tachibana_JSON = File.JSON_Read("Tachibana.json"); # pyright: ignore[reportAssignmentType] | In normal circumstances, this SHOULD return a Tachibana_JSON

	# File Checks
	if (not Misc.All_Includes(Tachibana.keys(), ["_Version", "Config", "Servers"])):
		Data.Recreate();


	if (not type(Tachibana["_Version"]) is tuple): Data.Recreate();
	if (not type(Tachibana["Config"]) is dict): Data.Recreate();
	if (not type(Tachibana["Servers"]) is dict): Data.Recreate();

	Misc.Under_At(App.Version, Tachibana["_Version"]);


if (__name__ != "__main__"): TSN_Abstracter.Import_Unsupported();
else: TSN_Abstracter.App_Init(True); Ignition(); 