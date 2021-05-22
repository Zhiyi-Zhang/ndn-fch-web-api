from flask import Flask, request, abort
from geopy import distance
import math

app = Flask(__name__)
router_list = []


def measure_distance(hub_json, requester_point, support_v4, support_v6, cap):
    try:
        hub_v4 = hub_json['ipv4']
    except KeyError:
        hub_v4 = False
    try:
        hub_v6 = hub_json['ipv6']
    except KeyError:
        hub_v6 = False

    available = False
    if support_v4 is True and hub_v4 is True:
        available = True
    if support_v6 is True and hub_v6 is True:
        available = True

    # 7590 is the longest distance on earth
    if not available:
        return math.inf
    try:
        hub_cap = hub_json[cap]
    except KeyError:
        return math.inf
    hub_point = (float(hub_json['position'][1]), float(hub_json['position'][0]))
    return distance.distance(requester_point, hub_point).kilometers


# Query: GET /?k=9&cap=wss&lon=-77&lat=39&ip=192.0.2.1
# k: number of routers to return, default 1
# cap: capability
# * options: udp, wss, http3
# * default: udp
# ipv4: 1 if client supports IPv4, 0 otherwise
# ipv6: 1 if client supports IPv6, 0 otherwise
# lon, lat: geo-coordinates, required
@app.route("/", methods=['GET'])
def get_closest_hub():
    global router_list
    if len(router_list) == 0:
        abort(403)

    if "lat" not in request.args or "lon" not in request.args:
        abort(403)
    lat = lon = 0.0
    try:
        lat = float(request.args["lat"])
        lon = float(request.args["lon"])
    except ValueError:
        abort(403)
    if lat < -90. or lat > 90. or lon < -180. or lon > 180.:
        abort(403)
    requester_point = (lat, lon)

    try:
        k = max(1, int(request.args.get("k", "")))
    except ValueError:
        k = 1

    support_v4 = False
    support_v6 = False
    if int(request.args.get("ipv4", 0)) == 1:
        support_v4 = True
    if int(request.args.get("ipv6", 0)) == 1:
        support_v6 = True
    if support_v4 is not True and support_v6 is not True:
        abort(403)

    cap = request.args.get("cap", "udp")
    result = sorted(router_list, key=lambda x: measure_distance(x, requester_point, support_v4, support_v6, cap))[:k]
    return ",".join(hub[cap] for hub in result if cap in hub)


@app.route("/routers", methods=['PUT'])
def update_router_list():
    global router_list
    router_list = request.get_json()
    print(router_list)
    return "success", 200
