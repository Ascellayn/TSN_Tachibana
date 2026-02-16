from ..Globals import *;
from .. import Register;
import Tachibana.Menus.Main as MM;
import Tachibana.Menus as M;
import subprocess;

def Create() -> None:
	Entries: TUI.Menu.Entries = [
		TUI.Menu.Entry(20, "Create SSH Connection", Bold=True),
		TUI.Menu.Entry(11, "Server Name", "Specify a friendly name for you to remember this SSH Server. Will overwrite the name if a server with the same Address, Port and Protocol already exists.", ID="Tachibana_Name"),
		TUI.Menu.Entry(11, "Server Address", "Specify the IP Address or Hostname the SSH Server is on.", ID="Address"),
		TUI.Menu.Entry(11, "Server Port", "Specify which port the SSH Server is on.", Value="22", ID="Port", Arguments=(r"\d",)),
		TUI.Menu.Entry(11, "Username", "The username we should log on as.", Value="root", ID="Username"),
		TUI.Menu.Entry(11, "SSH Key", "An absolute path to an SSH Key we should use.", Value="~/.ssh/id_rsa", ID="Passkey"),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(20, "SFTP Settings", Bold=True, Indentation=1),
		TUI.Menu.Entry(11, "Remote Folder", "Specify the folder you'd like to access from the Server remotely.", Value="/", Indentation=1, ID="Folder_Remote"),
		TUI.Menu.Entry(11, "Local Folder", "Specify a place in your filesystem where you would like to mount the remote folder.", Value="/media/SFTP", Indentation=1, ID="Folder_Local"),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(20, "Workarounds", Bold=True),
		TUI.Menu.Entry(10, "Spoof Terminal", "Enable to spoof to the Server which Terminal you are using. Useful if the Server does not support your Terminal.", ID="Term_Spoof"),
			TUI.Menu.Entry(11, "Exported Terminal", "Increases compatibility if your Server does not support your Terminal.", Indentation=1, Value="xterm-256color", ID="Term_Spoofed"),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(1, f"Save Server", "Create a brand new entry with the provided information."),
		TUI.Menu.Entry(0, f"Cancel", "Return to the Menu with all your saved SSH Servers.", Function=M.Menu_Protocol, Arguments=("SSH",), Indentation=-2),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(0, f"Return to Main Menu", Function=MM.Main, Indentation=-2)
	];
	uJSON: Type.uJSON_SSH = TUI.Menu.Interactive(Entries);
	if (uJSON):
		Register.SSH(uJSON);
		M.Menu_Protocol("SSH");

	MM.Main();



def Actions(Address: str, Profile_Name: str) -> TUI.Menu.Entries:
	Profile: Type.uJSON_SSH = cast(Type.uJSON_SSH, Tachibana["Servers"]["SSH"][Address]["Profiles"][Profile_Name]);

	if (len(File.List(Profile["Folder_Local"])[0]) == 0 and len(File.List(Profile["Folder_Local"])[1]) == 0):
		Mount_Entry = TUI.Menu.Entry(0, f"Mount \"{Profile['Folder_Remote']}\" Locally", f"Mount {Address}{Profile['Folder_Remote']} to {Profile['Folder_Local']}", Function=Mount, Arguments=(Profile, ));
	else: Mount_Entry = TUI.Menu.Entry(0, f"Unmount \"{Profile['Folder_Remote']}\"", f"Unmount {Address}{Profile['Folder_Remote']} which is currently mounted at {Profile['Folder_Local']}", Function=Unmount, Arguments=(Profile, ));

	return cast(TUI.Menu.Entries, [
		TUI.Menu.Entry(0, f"Connect to {Profile['Tachibana_Name']} as {Profile_Name}", f"Start a remote SSH Connection to {Address} as user \"{Profile_Name}\"", Function=Connect, Arguments=(Profile, )),
		Mount_Entry
	]); # os.path.ismount does not work with sshfs, don't ask me why I have no clue.


def Connect(Profile: Type.uJSON_SSH) -> bool:
	TUI.Exit();

	Command: str = "";
	if (Profile["Term_Spoof"]):
		Command += f"export TERM={Profile['Term_Spoofed']}; ";

	Command += f"{Safe.Nested_Dict(cast(dict[str, Any], Tachibana["Config"]), ["SSH", "Binary_SSH"], "/usr/bin/ssh")} ";

	if (Profile["Passkey"] != ""):
		Command += f"-oIdentityFile={Profile['Passkey']} ";

	Command += f"-p {Profile['Port']} {Profile['Username']}@{Profile['Address']} ";
	Log.Info(f"Running {Command}...");
	Return = subprocess.run(Command, shell=True);
	try: Return.check_returncode();
	except Exception as Except:
		Log.Critical(f"Got a non-null return code while running the command!\n{Except}");
		input("Press Enter to continue.");

	TUI.Init();
	return True;


def Mount(Profile: Type.uJSON_SSH) -> bool:
	TUI.Exit();
	Command: str= f"{Safe.Nested_Dict(cast(dict[str, Any], Tachibana["Config"]), ["SSH", "Binary_SSHFS"], "/usr/bin/sshfs")} ";

	if (Profile["Passkey"] != ""):
		Command += f"-oIdentityFile={Profile['Passkey']} ";

	Command += f"-p {Profile['Port']} {Profile['Username']}@{Profile['Address']}:{Profile['Folder_Remote']} {Profile['Folder_Local']}";

	if (not File.Exists(Profile["Folder_Local"])):
		File.Path_Create(Profile["Folder_Local"]);
		Log.Warning(f"Local Path \"{Profile['Folder_Local']}\" did not exist and was created automatically.");

	Log.Info(f"Running {Command}...");
	Return: subprocess.CompletedProcess[bytes] = subprocess.run(Command, shell=True);
	try: Return.check_returncode();
	except Exception as Except:
		Log.Critical(f"Got a non-null return code while running the command!\n{Except}");
		input("Press Enter to continue.");

	TUI.Init();
	return True;

def Unmount(Profile: Type.uJSON_SSH) -> bool:
	TUI.Exit();
	Command: str = f"umount {Profile['Folder_Local']}";

	Log.Info(f"Running {Command}...");
	Return: subprocess.CompletedProcess[bytes] = subprocess.run(Command, shell=True);
	try: Return.check_returncode();
	except Exception as Except:
		Log.Warning(f"Caught exception when running unmount, trying with option \"-l\"...\n{Except}");
		Command += " -l";
		Return: subprocess.CompletedProcess[bytes] = subprocess.run(Command, shell=True);
		try: Return.check_returncode();
		except Exception as sExcept:
			Log.Critical(f"Got a non-null return code while running the command!\n{sExcept}");
			input("Press Enter to continue.");

	TUI.Init();
	return True;