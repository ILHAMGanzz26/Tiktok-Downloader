#!/bin/bash
# =========================================
# Installer module Python untuk TikTok Downloader
# =========================================

echo ">>> Update & upgrade packages..."
pkg update -y && pkg upgrade -y

echo ">>> Install Python & pip..."
pkg install -y python python-pip

echo ">>> Install dependencies..."
pip install --upgrade pip
pip install requests beautifulsoup4 pyfiglet rich

echo ">>> Beri Akses Termux..."
termux-setup-storage

echo ">>> Semua module berhasil diinstall!"
echo "Menjalankan Script..."
echo "Menunggu Perintah..."
echo "Perintah Di Terima..."
echo "Script Di Jalankan..."
echo "1"
echo "2"
echo "3"
echo "4"
echo "5"
echo "Memuat Script........."
python ttdl.py