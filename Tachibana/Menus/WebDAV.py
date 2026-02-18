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