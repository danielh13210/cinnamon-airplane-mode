#!/usr/bin/env python3
import gi
import subprocess
import time

gi.require_version('XApp', '1.0')
from gi.repository import XApp, GLib

ICON_ON = "airplane-mode-symbolic"
CHECK_INTERVAL = 2  # seconds

# Create the status applet (but don't show it yet)
applet = XApp.StatusIcon()
applet.set_tooltip_text("Airplane Mode Indicator")

def is_airplane_mode():
    """Check if airplane mode is active using nmcli."""
    try:
        output = subprocess.check_output("nmcli radio all | tail -n +2 | xargs | tr ' ' '\n'",shell=True, text=True)
        output=output.lower()
        #Modulo check to get odd lines only (software block state)
        #This line means that it returns True if any radio is effectively enabled
        return not any(map(lambda x:True if 'enabled' in x[1] else False,filter(lambda x:x[0]%2==1,enumerate(output.splitlines()))))
    except Exception as e:
        print(f"Error checking airplane mode: {e}")
        return False

def update_icon():
    """Show or hide the applet based on airplane mode status."""
    if enabled:=is_airplane_mode():
        applet.set_icon_name(ICON_ON)
        applet.set_tooltip_text("Airplane Mode: ON")
        applet.set_visible(True)
    else:
        applet.set_visible(False)
    print(enabled)
    return True  # Keep the timeout running

# Initial check
update_icon()

# Refresh every few seconds
GLib.timeout_add_seconds(CHECK_INTERVAL, update_icon)

# Start the GTK main loop
GLib.MainLoop().run()
