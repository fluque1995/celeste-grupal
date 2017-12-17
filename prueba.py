from planet import Planet
import plotly.offline as plt
from plotly.graph_objs import Scattergl

earth = Planet("La tierra", 0.017, 1, 365.26, 5.9742*10**24, 0, 0, 101.22)

orbit = earth.get_orbit_2bodies(200)

plt.plot(
    {'data': [
        Scattergl(x=orbit[:, 0],
                  y=orbit[:, 1])
        ]
     }
)
