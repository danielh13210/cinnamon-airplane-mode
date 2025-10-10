#!/usr/bin/env python3
import gi
import subprocess
import time

gi.require_version('XApp', '1.0')
from gi.repository import XApp, GLib

ICON_ON = "airplane-mode-on-symbolic"
CHECK_INTERVAL = 5  # seconds

# Create the status applet (but don't show it yet)
applet = XApp.StatusIcon()
applet.set_title("Airplane Mode Indicator")

def is_airplane_mode():
    """Check if airplane mode is active using nmcli."""
    try:
        output = subprocess.check_output(["nmcli", "radio", "all"], text=True)
        return "disabled" in output.lower()
    except Exception as e:
        print(f"Error checking airplane mode: {e}")
        return False

def update_icon():
    """Show or hide the applet based on airplane mode status."""
    if is_airplane_mode():
        applet.set_icon_name(ICON_ON)
        applet.set_tooltip_text("Airplane Mode: ON")
        applet.set_visible(True)
    else:
        applet.set_visible(False)
    return True  # Keep the timeout running

# Initial check
update_icon()

# Refresh every few seconds
GLib.timeout_add_seconds(CHECK_INTERVAL, update_icon)

# Start the GTK main loop
GLib.MainLoop().run()
