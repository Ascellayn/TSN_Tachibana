from .Globals import *;
from . import Type;


def Protocol(Protocol: str) -> None:
	if (Protocol not in Tachibana["Servers"].keys()):
		Tachibana["Servers"][Protocol] = {};

def Profile(Protocol: str, Internal_Name: str, Profile_Name: str, uJSON: Type.uJSON) -> None:
	if (not Internal_Name in Tachibana["Servers"][Protocol].keys()):
		Tachibana["Servers"][Protocol][Internal_Name] = {
			"Name": uJSON["Tachibana_Name"],
			"Profiles": {}
		};

	Tachibana["Servers"][Protocol][Internal_Name]["Profiles"][Profile_Name] = uJSON





def SSH(uJSON: Type.uJSON_SSH) -> bool:
	global Tachibana; Protocol("SSH");
	Profile("SSH", f"{uJSON['Address']}:{uJSON['Port']}", uJSON["Username"], uJSON);
	Data.Save()
	return True;


def WebDAV(uJSON: Type.uJSON_WebDAV) -> bool:
	global Tachibana; Protocol("WebDAV");
	Profile("WebDAV", f"{uJSON['Address']}:{uJSON['Port']}", uJSON["Username"], uJSON);
	Data.Save()
	return True;



def Wireguard(uJSON: Type.uJSON_Wireguard) -> bool:
	global Tachibana; Protocol("Wireguard");

	Tachibana["Servers"]["Wireguard"][uJSON["Adapter"]] = {
		"Name": uJSON["Tachibana_Name"] if (uJSON["Tachibana_Name"]) else str(Time.Get_Unix())
	};

	Data.Save()
	return True;