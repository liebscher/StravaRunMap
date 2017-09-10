from os import listdir
from os.path import join
import matplotlib.pyplot as plt
import gpxpy
import fnmatch
from math import radians, sin, cos, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 3959.274 # Radius of earth in kilometers. Use 3956 for miles
    return c * r


data_path = '../../Downloads/activities/'

data = [f for f in listdir(data_path) if fnmatch.fnmatch(f, '*-Run.gpx')]

#data = data[-50:]

lat = []
lon = []

fig = plt.figure(facecolor = 'black')
ax = plt.Axes(fig, [0., 0., 1., 1.])
ax.set_aspect('equal')
ax.set_axis_off()
fig.add_axes(ax)

distance = 0
prevLatitude = 0
prevLongitude = 0

for activity in data:
    gpx_filename = join(data_path, activity)
    gpx_file = open(gpx_filename, 'r')
    gpx = gpxpy.parse(gpx_file)

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                #top left: 33.149497, -117.345333
                #bottom right: 32.536444, -116.804265
                if point.latitude > 32.536444 and point.latitude < 33.1 and point.longitude < -116.804265 and point.longitude > -117.33:
                    lat.append(point.latitude)
                    lon.append(point.longitude)
                    if prevLatitude != 0:
                        distance += haversine(point.latitude, point.longitude, prevLatitude, prevLongitude)

                    prevLatitude = point.latitude
                    prevLongitude = point.longitude
    plt.plot(lon, lat, color = 'coral', lw = 0.3, alpha = 0.3)
    lat = []
    lon = []

filename = 'map.png'
fig.text(0.90, 0.95, str(round(distance, 1)) + "mi", fontsize=10, color="coral", alpha=0.75, ha="right", va="top")
#plt.show()
plt.savefig(filename, facecolor = fig.get_facecolor(), pad_inches=0, dpi=300)