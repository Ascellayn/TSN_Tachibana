from TSN_Abstracter import *;
from TSN_Abstracter import TUI; # pyright: ignore[reportUnusedImport]
from . import Type;
import os, socket; # pyright: ignore[reportUnusedImport]

# If Main.py is executed outside of the Tachibana folder, make sure we are inside the correct folder
os.chdir(File.Main_Directory);


Tachibana: Type.Tachibana_JSON = cast(Type.Tachibana_JSON, File.JSON_Read("Tachibana.json"));

class Data:
	""" This class would have been inside its own module, but the IDE gets angry because it's stupid and doesn't realize Tachibana is declared in this very file even if I explicitly import it """
	@staticmethod
	def Save() -> None:
		global Tachibana;
		Log.Stateless(f"Saving Tachibana.json...");
		Tachibana["_Version"] = list(App.Version);
		File.JSON_Write("Tachibana.json", Tachibana);
		Log.Awaited().OK();

	@staticmethod
	def Recreate() -> None:
		global Tachibana;
		Log.Error("Tachibana.json is corrupted or missing, creating a backup if it exists and recreating the file!");
		if (File.Exists("Tachibana.json")): File.JSON_Write(f"Tachibana-{Time.Get_Unix()}.bak", Tachibana);
		Tachibana = cast(Type.Tachibana_JSON, {
			"_Version": list(App.Version),
			"Config": {},
			"Servers": {}
		});
		Data.Save();
