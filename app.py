from flask import Flask, request, abort
from geopy import distance
from enum import Enum

app = Flask(__name__, template_folder="_templates")
router_list = []


class Cap(Enum):
    UDP = 1
    WSS = 2
    HTTP3 = 3


def measure_distance(hub_json, requester_point, support_v4, support_v6):
    hub_v4 = hub_v6 = available = False
    if hub_json['ipv4'] is not None:
        hub_v4 = hub_json['ipv4']
    if hub_json['ipv6'] is not None:
        hub_v6 = hub_json['ipv4']

    if support_v4 is True and hub_v4 is True:
        available = True
    if support_v6 is True and hub_v6 is True:
        available = True

    if not available:
        # longest distance on earth
        return 7590
    hub_point = (float(hub_json['position'][1]), float(hub_json['position'][0]))
    return distance.distance(requester_point, hub_point).kilometers


def find_k_nearest_hubs(k, requester_point, support_v4, support_v6):
    sorted_routers = sorted(router_list, key=lambda x: measure_distance(x, requester_point, support_v4, support_v6))
    return sorted_routers[:k]


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

    k = 1
    try:
        k = int(request.args.get("k"))
    except ValueError:
        k = 1
    if k < 1:
        k = 1
    elif k > 10:
        k = 10

    support_v4 = False
    support_v6 = False
    if int(request.args.get("ipv4", 0)) == 1:
        support_v4 = True
    if int(request.args.get("ipv6", 0)) == 1:
        support_v6 = True
    if support_v4 is not True and support_v6 is not True:
        abort(403)

    if ""

    find_k_nearest_hubs(k, requester_point, support_v4, support_v6)


@app.route("/routers", methods=['PUT'])
def update_router_list():
    global router_list
    router_list = request.json