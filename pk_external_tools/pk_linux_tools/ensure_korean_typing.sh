#!/bin/bash

echo "Updating package list..."
sudo apt update

echo "Installing Korean language support..."
sudo apt install -y language-pack-ko language-pack-gnome-ko ibus ibus-hangul

echo "Configuring IBus environment variables..."
{
  echo 'export GTK_IM_MODULE=ibus'
  echo 'export QT_IM_MODULE=ibus'
  echo 'export XMODIFIERS=@im=ibus'
} >> ~/.profile
source ~/.profile

echo "Setting Korean input source..."
gsettings set org.gnome.desktop.input-sources sources "[('xkb', 'us'), ('ibus', 'hangul')]"

echo "Configuring keyboard shortcut (Super + Space)..."
gsettings set org.gnome.desktop.wm.keybindings switch-input-source "['<Super>space']"

echo "Restarting IBus..."
ibus restart

echo "Korean input setup complete. You can switch between English and Korean with Super + Space."

