from flask import Flask, request, abort, make_response
from geopy import distance
import math
import json
import os
import sys

app = Flask(__name__)
router_list = []
hub_path = os.getenv("FCH_HUB_PATH")
if not hub_path:
    print("FCH_HUB_PATH is not specified for hub file storage")
    sys.exit()
hub_file_path = os.path.join(hub_path, "hubs.txt")


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


def load_hubs_from_file():
    global router_list
    with open(hub_file_path) as hubs_file:
        router_list = json.load(hubs_file)


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
        load_hubs_from_file()
        if len(router_list) == 0:
            abort(500)
    local_router_list = router_list

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
    for hub in local_router_list:
        hub.update({"distance": measure_distance(hub, requester_point, support_v4, support_v6, cap)})
    result = sorted(local_router_list, key=lambda x: x["distance"])[:k]
    response = make_response(",".join(hub[cap] for hub in result if cap in hub and hub["distance"] != math.inf), 200)
    response.headers["Content-Type"] = "text/plain"
    return response


# update the hub list
# will write the hub list into a file called hubs.txt under environment var FCH_HUB_PATH
@app.route("/routers", methods=['PUT'])
def update_router_list():
    global router_list
    router_list = request.get_json()
    with open(hub_file_path, 'w') as hubs_file:
        json.dump(router_list, hubs_file)
    return "success", 200
