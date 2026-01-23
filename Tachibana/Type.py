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
from Globals import Any, TypedDict;
import enum;





# Basic Types
type Profile = dict[str, Connection_Info];
class Server_Type(enum.Enum):
	SSH = "SSH";



class Server(TypedDict):
	Name: str; Profiles: Profile;


class Connection_Info(TypedDict):
	User: str; Password: str | None;





# Specific Types
class SSH(Connection_Info):
	Passkey: str | None;
	Folder_Remote: str; Folder_Local: str;





class Tachibana_JSON(TypedDict):
	"""Tachibana.json File Format"""
	_Version: tuple[int, ...];
	Config: dict[str, Any];
	Servers: dict[Server_Type, Server];