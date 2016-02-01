#!/bin/sh
cd ..

# Get the user input:
read -p "Username: " ttiUsername
read -p "Gameserver (DEFAULT:  192.168.1.19): " TTI_GAMESERVER
TTI_GAMESERVER=${TTI_GAMESERVER:-"192.168.1.19"}

# Export the environment variables:
export ttiUsername=$ttiUsername
export ttiPassword="password"
export TTI_PLAYCOOKIE=$ttiUsername
export TTI_GAMESERVER=$TTI_GAMESERVER

echo "==============================="
echo "Starting Toontown Infinite..."
echo "Username: $ttiUsername"
echo "Gameserver: $TTI_GAMESERVER"
echo "==============================="

/usr/bin/python2 -m toontown.toonbase.ClientStart
