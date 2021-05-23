#! /bin/bash

curl -X PUT -H "Content-Type: application/json" -d '
[
  {
    "id": "ucla",
    "position": [-130, 36.5],
    "ipv4": true,
    "udp": "suns.cs.ucla.edu",
    "wss": "suns.cs.ucla.edu"
  },
  {
    "id": "yoursunny-dal",
    "position": [-96.797, 32.7767],
    "ipv4": true,
    "ipv6": true,
    "http3": "https://dal.quic.g.ndn.today/ndn"
  },
  {
    "id": "fake-1",
    "position": [100.797, 32.7767],
    "ipv4": true,
    "ipv6": true,
    "udp": "fake.cs.ucla.edu",
    "wss": "fake.cs.ucla.edu",
    "http3": "https://fake.cs.ucla.edu/ndn"
  },
  {
    "id": "fake-2",
    "position": [130.797, 32.7767],
    "ipv4": true,
    "ipv6": true,
    "udp": "fake2.cs.ucla.edu",
    "wss": "fake2.cs.ucla.edu",
    "http3": "https://fake2.cs.ucla.edu/ndn"
  }
]

' "http://127.0.0.1:5000/routers" -i