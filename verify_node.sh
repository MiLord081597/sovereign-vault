#!/bin/zsh

NODES=("Destiny_Howard_1999" "Node_02_Standby")
ACTIVE_ANCHOR=""
FORCE_OVERRIDE=$1

echo "Initiating node verification sequence..."

for NODE in "${NODES[@]}"; do
    echo "[*] Pinging $NODE..."
    sleep 1
    
    if [ "$NODE" = "Destiny_Howard_1999" ]; then
        if [ "$FORCE_OVERRIDE" = "--force" ]; then
            echo "[!] FORCE FLAG DETECTED. Bypassing timeout protocols..."
            sleep 1
            echo "[+] $NODE connection forced and established."
            ACTIVE_ANCHOR=$NODE
            break
        else
            echo "[-] $NODE unreachable. Connection timeout. (Use --force to override)"
        fi
    else
        echo "[+] $NODE verified and active."
        ACTIVE_ANCHOR=$NODE
        break
    fi
done

if [ -z "$ACTIVE_ANCHOR" ]; then
    echo "[!] CRITICAL: All nodes unreachable. Network unfounded."
    rm -f .current_anchor
    exit 1
fi

echo "$ACTIVE_ANCHOR" > .current_anchor
echo "Verification complete. Active anchor state saved: $ACTIVE_ANCHOR"
