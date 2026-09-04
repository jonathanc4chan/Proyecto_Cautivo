#!/bin/bash
sudo pkill -f "python3.*portal.py" 2>/dev/null || true
sudo pkill hostapd 2>/dev/null || true
sudo pkill dnsmasq 2>/dev/null || true
sudo nft flush ruleset
sudo nmcli device set wlo1 managed yes 2>/dev/null || true
echo "[OK] Portal detenido."
