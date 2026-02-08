from .Globals import *;
from .Type import *;





def Wireguard(uJSON: uJSON_Wireguard) -> bool:
	global Tachibana;

	#if (not File.Exists(f"/etc/wireguard/{uJSON['Adapter']}.conf")): return False;
	if ("Wireguard" not in Tachibana["Servers"].keys()):
		Tachibana["Servers"]["Wireguard"] = {};

	Tachibana["Servers"]["Wireguard"][uJSON["Adapter"]] = {
		"Name": uJSON["Tachibana_Name"] if (uJSON["Tachibana_Name"]) else str(Time.Get_Unix())
	};

	Data.Save()
	return True;