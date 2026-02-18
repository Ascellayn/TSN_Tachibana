from ..Globals import *;
import subprocess;





Create: tuple[TUI.Menu.Entries, TUI.Menu.Entries] = (
	[],
	[
		TUI.Menu.Entry(11, "WebDAV Name", "Specify a name used by the WebDAV Configurator.", ID="WebDAV_Name", Required=True),
		TUI.Menu.Entry(10, "Enable Encryption (HTTPS)", "Enable the use of HTTPS, recommended if you're connecting to a non-local WebDAV Server.", Value=False, ID="Encryption"),
		TUI.Menu.Entry(11, "Address", "Specify the IP Address or Hostname of the WebDAV Server.", ID="Address", Required=True),
		TUI.Menu.Entry(11, "Server Port", "Specify which port the WebDAV Server is on.", Value="80", ID="Port", Arguments=(r"\d",), Required=True),
		TUI.Menu.Entry(11, "Username", "The username we should log on as.", Value="admin", ID="Username"),
		TUI.Menu.Entry(11, "Password", "The password we should use to login.", ID="Password"),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(20, "Mounting Settings", Bold=True, Indentation=1),
		TUI.Menu.Entry(11, "Remote Folder", "Specify the folder you'd like to access from the Server remotely.", Value="/", Indentation=1, ID="Folder_Remote", Required=True),
		TUI.Menu.Entry(11, "Local Folder", "Specify a place in your filesystem where you would like to mount the remote folder.", Value="/media/WebDAV", Indentation=1, ID="Folder_Local", Required=True),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(20, "Caching", Bold=True),
		TUI.Menu.Entry(10, "Enable VFS Cache", "This settings allows the WebDAV Client to store certain files for faster file access at the cost of increased disk usage on the client side.", Value=True, ID="Cache_VFS"),
			TUI.Menu.Entry(12, "Cache Mode", "Specify which VFS Caching Mode we should use.", Value="full", Arguments=("off", "writes", "full", "writeback"), ID="Cache_VFS_Type"),
		TUI.Menu.Entry(10, "Enable Directory Cache", "This settings allows the WebDAV Client to store the contents of folders. Useful if you're frequently accessing repeatedly the same folder.", Value=True, ID="Cache_DIR"),
			TUI.Menu.Entry(11, "Cache Duration", "Specify how long the directory cache should last before expiring.", Value="1h", ID="Cache_DIR_Value"),
		TUI.Menu.Entry(20, ""),
		TUI.Menu.Entry(20, "Miscellaneous", Bold=True),
		TUI.Menu.Entry(11, "Pacer Minimum Sleep", "Specify the minimum time in milliseconds the WebDAV client should wait before sending a new request.", Value="0.01", Arguments=(r"[\d\.]",), ID="Misc_Pace", Required=True),
	]
);





def Actions(Address: str, Profile_Name: str) -> TUI.Menu.Entries:
	Profile: Type.uJSON_WebDAV = cast(Type.uJSON_WebDAV, Tachibana["Servers"]["WebDAV"][Address]["Profiles"][Profile_Name]);
	
	Binary: str = Safe.Nested_Dict(
		cast(dict[str, Any], Tachibana["Config"]), 
		["Servers", "WebDAV", "Binary"], None
	);
	hasRClone: bool = File.Exists(Binary) if (Binary) else False;

	if (not os.path.ismount(Profile["Folder_Local"]) or (len(File.List(Profile["Folder_Local"])[0]) == 0 and len(File.List(Profile["Folder_Local"])[1]) == 0)):
		Mount_Entry = TUI.Menu.Entry(0, f"Mount \"{Profile['Folder_Remote']}\" Locally", f"Mount {Address}{Profile['Folder_Remote']} to {Profile['Folder_Local']}", Function=Mount, Arguments=(Profile, ), Unavailable=not hasRClone);
	else: Mount_Entry = TUI.Menu.Entry(0, f"Unmount \"{Profile['Folder_Remote']}\"", f"Unmount {Address}{Profile['Folder_Remote']} which is currently mounted at {Profile['Folder_Local']}", Function=Unmount, Arguments=(Profile, ), Unavailable=not hasRClone);

	return cast(TUI.Menu.Entries, [
		Mount_Entry
	]); # os.path.ismount does not work with sshfs, don't ask me why I have no clue.





def Mount(Profile: Type.uJSON_WebDAV) -> bool:
	TUI.Exit();

	RClone: str = Safe.Nested_Dict(cast(dict[str, Any], Tachibana["Config"]), ["Servers", "WebDAV", "Binary"], "/bin/rclone");
	Command: str= RClone + " ";

	Command += f"config create {Profile['WebDAV_Name']} webdav ";
	Command += f"url={'https://' if (Profile['Encryption']) else 'http://'}{Profile['Address']}:{Profile['Port']} ";
	Command += f"pacer_min_sleep={Profile['Misc_Pace']} ";

	if (Profile["Username"] != ""): Command += f"user={Profile['Username']} ";
	if (Profile["Password"] != ""): Command += f"pass={Profile['Password']} ";

	Command += "&& ";

	Command += RClone + f" mount ";
	if (Profile["Cache_VFS"]): Command += f"--vfs-cache-mode {Profile['Cache_VFS_Type']} ";
	if (Profile["Cache_DIR"]): Command += f"--dir-cache-time {Profile['Cache_DIR_Value']} ";

	Command += f"{Profile['WebDAV_Name']}: {Profile['Folder_Local']} ";
	Command += "--daemon ";

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





def Unmount(Profile: Type.uJSON_WebDAV) -> bool:
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