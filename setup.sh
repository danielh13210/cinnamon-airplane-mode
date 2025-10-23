#!/bin/bash
cd "$(dirname "$0")"
TARGET="$HOME/.local/share/cinnamon-airplane-mode"
mkdir -p "$TARGET"

# copy repository contents but exclude the .git directory
if command -v rsync >/dev/null 2>&1; then
    rsync -a --exclude='.git' ./ "$TARGET/"
else
    # fallback to tar if rsync isn't available
    tar --exclude='./.git' -C . -cf - . | tar -C "$TARGET" -xpf -
fi
mkdir -p ~/.config/autostart
cp ./airplane-mode-daemon-autostart.desktop ~/.config/autostart/
echo "Installed autostart file to ~/.config/autostart/"