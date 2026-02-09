"""
### Tachibana.json
```
{
	"_Version": {App.Version},
	"Config": {},
	"Servers": {
		"SSH": {
			"{Address}:{Port}": {
				"Name": "{User Specified Server Name}",
				"Profiles": {
					"{User Specified Profile Name}": {
						"User": "{Connection Username}",
						"Password": "{Password}" | null,
						"Passkey": " {Path to SSH Key}" | null,
						"Folder_Remote": "{Remote Path to mount Locally}",
						"Folder_Local": "{Local Path to mount Remote to}"
					}
				}
			}
		}
	}
}
```
"""
from .Globals import Any, TypedDict;





# Basic Types
type Profile = dict[str, Connection_Info | dict[str, str]];



class Server(TypedDict):
	Name: str; Profiles: Profile;


class Connection_Info(TypedDict):
	User: str; Password: str | None;





# Tachibana JSON & uJSONs
class Tachibana_JSON(TypedDict):
	"""Tachibana.json File Format"""
	_Version: list[int];
	Config: dict[str, Any];
	Servers: dict[str, Server | dict[str, Any]];

class uJSON(TypedDict):
	Tachibana_Name: str;




class uJSON_SSH(uJSON):
	""" SSH Config"""
	# General
	Address: str; Port: int;
	Username: str; Password: str; Passkey: str;

	# SFTP
	Folder_Remote: str;
	Folder_Local: str;

	# Workarounds
	Term_Spoof: bool;
	Term_Spoofed: str;


class uJSON_WebDAV(uJSON):
	""" WebDAV Config """
	# General
	WebDAV_Name: str;
	Server_URL: str;
	Username: str; Password: str;

	# Mounting
	Folder_Remote: str;
	Folder_Local: str;

	# Caching
	Cache_VFS: bool; Cache_VFS_Type: str;
	Cache_DIR: bool; Cache_DIR_Value: str;

	# Miscellaneous
	Misc_Pace: str;


class uJSON_Wireguard(uJSON):
	""" Wireguard Config """
	Adapter: str;