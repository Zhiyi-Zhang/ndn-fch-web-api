# NDN Find Closest Hub (FCH) RESTful APIs

## Why we need this?

Find the closest hub near you to connect to the NDN testbed.

Compared with the existing FCH:
* The existing version uses KNN to decide the closest hubs but it can give wrong results when two coordinate points are remote in values but geographically close.
E.g., (179, 0) and (-179, 0) are geographically close to each other but their numeric distance is large.
* This FCH supports more types, including `udp`, `wss` for WebSocket, and `http3` for HTTP/3.
* This FCH allows requester to specify IPv4 and IPv6 at the time of query.
* This FCH allows real-time update of hub information with RESTful API `/routers`.

## Deployment with uWSGI

1 Create python virtual environment and activate it.
 
```bash
python3 -v venv venv
. venv/bin/activate
```

2 Install dependencies

```bash
pip install -r requirements.txt
```

3 Start running

```bash
FCH_HUB_PATH=. uwsgi --http 127.0.0.1:5000 --module wsgi-app
```

`FCH_HUB_PATH` is the directory to store the hub list file. The hub list file will be named as `hubs.txt`.

## RESTful APIs

### 1. Get closest hubs

#### GET Request

HTTP GET request containing the query parameters.
The URL is `/`.

Example:
```ascii
GET /?k=9&cap=wss&lon=-77&lat=39&ip=192.0.2.1
```

* k: number of routers to return, default 1
* cap: capability
    * options: udp, wss, http3
    * default: udp
* ipv4: 1 if client supports IPv4, 0 otherwise
* ipv6: 1 if client supports IPv6, 0 otherwise
* lon, lat: geo-coordinates, required

#### Response

A CSV format of file containing the udp/wss/https for NDN connectivity establishment.

Example:
```ascii
suns.cs.ucla.edu,example1.cs.ucla.edu,exmaple2.cs.ucla.edu
```

### 2. Update hub information

#### PUT Request

HTTP PUT request containing a JSON format list of hub information.
The URL is `/routers`.

Example:
```ascii
PUT /routers
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
  }
]
```
The position value follows GeoJSON, namely, `[lontitude, latitude]`.


#### Response

Success 200