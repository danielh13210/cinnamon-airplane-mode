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

def get_radio_status() -> dict:
    """ return a dict for device statuses """
    output = subprocess.check_output(["env","LANG=\"\"","nmcli","radio","all"],text=True)
    devices,statuses_raw=tuple(map(str.split,output.splitlines()))
    statuses=map(lambda s:'enabled' in s,statuses_raw)
    return dict(zip(devices,statuses))

def is_airplane_mode():
    """Check if airplane mode is active using nmcli."""
    try:
        statuses=get_radio_status()
        for device_type in filter(lambda dev:not dev.endswith('-HW'),statuses.keys()):
             hw_on=statuses[device_type+'-HW']
             sw_on=statuses[device_type]
             if hw_on and sw_on:
               return False
        return True
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

def main():
    # Initial check
    update_icon()

    # Refresh every few seconds
    GLib.timeout_add_seconds(CHECK_INTERVAL, update_icon)

    # Start the GTK main loop
    GLib.MainLoop().run()

if __name__ == "__main__":
    main()
