#!/bin/bash
cd "$(dirname "$0")"
cp -r . ~/.local/share/cinnamon-airplane-mode
echo "Copied files to ~/.local/share/cinnamon-airplane-mode"
mkdir -p ~/.config/autostart
cp ./airplane-mode-daemon-autostart.desktop ~/.config/autostart/
echo "Installed autostart file to ~/.config/autostart/"