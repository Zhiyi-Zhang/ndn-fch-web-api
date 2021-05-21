#! /bin/bash

curl -X PUT -H "Content-Type: application/json" -d '[{"id": "ucla","position": [-130, 36.5],"ipv4": true,"udp": "suns.cs.ucla.edu","wss": "suns.cs.ucla.edu"},{"id": "yoursunny-dal","position": [-96.797, 32.7767],"ipv4": true,"ipv6": true,"http3": "https://dal.quic.g.ndn.today/ndn"}]' "http://127.0.0.1:5000/routers"