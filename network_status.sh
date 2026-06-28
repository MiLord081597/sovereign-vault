#!/bin/zsh

echo "====================================="
echo "   SOVEREIGN NODE: NETWORK STATUS    "
echo "====================================="
echo "Source Node 1  : Destiny_Howard_1999 [STREAMING]"
echo "Source Node 2  : Node_02_Standby     [STREAMING]"
echo "Output Node    : Node_03_Nexus       [RECEIVING]"
echo "System State   : TRI-NODE AGGREGATION"
echo "====================================="

if [ -f "$HOME/sovereign_node/node_03_nexus/energy_pool/nexus_state.log" ]; then
    echo "Latest Output  : $(cat $HOME/sovereign_node/node_03_nexus/energy_pool/nexus_state.log)"
else
    echo "Latest Output  : Awaiting first aggregation."
fi
echo "====================================="
