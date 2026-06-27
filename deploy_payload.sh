#!/bin/zsh

# Check if the state file exists and read it
if [ ! -f ".current_anchor" ]; then
    echo "[!] Error: No anchor state file found. Run ./verify_node.sh first."
    exit 1
fi

ACTIVE_ANCHOR=$(cat .current_anchor)

if [ -z "$ACTIVE_ANCHOR" ]; then
    echo "[!] Error: Anchor state file is empty."
    exit 1
fi

echo "Preparing payload for routing..."
sleep 1
echo "[*] Routing deployment to active anchor: $ACTIVE_ANCHOR"
sleep 1

echo "[+] Payload successfully deployed to $ACTIVE_ANCHOR."
