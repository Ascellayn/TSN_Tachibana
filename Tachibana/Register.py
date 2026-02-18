from .Globals import *;
from . import Type;


def Tachibana_Config(uJSON: Type.uJSON_Config) -> bool:
	global Tachibana;
	Tachibana_CFG = cast(Type.Tachibana_Config, {
		"Mounts": {
			"Keep_Open": uJSON["Mounts_Keep_Open"],
		},
		"Servers": {
			"SSH": {
				"Ping": uJSON["Server_SSH_Ping"],
				"Binary_SSH": uJSON["Server_SSH_Binary_SSH"],
				"Binary_SSHFS": uJSON["Server_SSH_Binary_SSHFS"]
			},
			"WebDAV": {
				"Ping": uJSON["Server_WebDAV_Ping"]
			}
		}
	});
	Tachibana["Config"] = Tachibana_CFG;
	Data.Save()
	return True;
#










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