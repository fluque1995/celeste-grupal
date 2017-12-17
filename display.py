import plotly.offline as py
import plotly.graph_objs as go
from planet import Planet
import numpy as np


class SolarSystem:

    def __init__(self):
        self.inner_planets = [
            Planet("Mercurio", 0.206, 0.387, 87.97,
                   3.301e23, 7, 47.14, 75.9),
            Planet("Venus", 0.007, 0.723, 224.7,
                   4.867e24, 3.59, 75.78, 130.15),
            Planet("La tierra", 0.017, 1, 365.26,
                   6.046e24, 0, 0, 101.22),
            Planet("Marte", 0.093, 1.524, 686.98,
                   6.417e23, 1.85, 48.78, 101.22)
        ]

        self.outer_planets = [
            Planet("Júpiter", 0.048, 5.203, 4332.6,
                   1.899e27, 1.31, 99.44, 12.72),
            Planet("Saturno", 0.056, 9.546, 10759,
                   5.685e26, 2.5, 112.79, 91.09),
            Planet("Urano", 0.047, 19.2, 30687,
                   8.682e25, 0.77, 73.48, 169.05),
            Planet("Neptuno", 0.009, 30.09, 60784,
                   1.024e26, 1.78, 130.68, 43.83)
        ]

    def display_inner_planets(self):

        steps = 10
        orbits = [planet.get_orbit(60) for planet in self.inner_planets]
        planets = [[planet.position(i) for i in range(0, 700, steps)]
                   for planet in self.inner_planets]

        rng = int(1.2*self.inner_planets[-1].a) + 1

        axis3d = dict(
            showbackground=True,
            backgroundcolor="rgb(230, 230,230)",
            gridcolor="rgb(255, 255, 255)",
            zerolinecolor="rgb(255, 255, 255)",
        )
        
        layout = dict(
            width=600, height=500,
            scene=dict(xaxis=(axis3d),
                       yaxis=(axis3d),
                       zaxis=dict(axis3d,
                                  **dict(range=[-rng, rng],
                                         autorange=False)),
                       aspectratio=dict(x=1, y=1, z=1)),
            title='Movimiento orbital de los planetas interiores',
            hovermode='closest',
            updatemenus=[
                {
                    'type': 'buttons',
                    'buttons': [
                        {
                            'label': 'Iniciar',
                            'method': 'animate',
                            'args': [None, dict(
                                frame=dict(duration=0),
                                transition=dict(duration=100),
                                fromcurrent=True,
                            )],
                        }
                    ]
                }
            ]
        )
        data = [
            dict(x=[0], y=[0], z=[0],
                 type='scatter3d',
                 mode='markers',
                 marker=dict(
                     size=10,
                     color='rgba(230, 230, 0, .9)',
                     line=dict(width=1, color='rgb(100,100,0)')
                 ),
                 name='Sol'),
            dict(x=orbits[0][:, 0],
                 y=orbits[0][:, 1],
                 z=orbits[0][:, 2],
                 type='scatter3d',
                 mode='lines',
                 line=dict(width=2, color='blue'),
                 name="Órbita de Mercurio"),
            dict(x=orbits[1][:, 0],
                 y=orbits[1][:, 1],
                 z=orbits[1][:, 2],
                 type='scatter3d',
                 mode='lines',
                 line=dict(width=2, color='orange'),
                 name="Órbita de Venus"),
            dict(x=orbits[2][:, 0],
                 y=orbits[2][:, 1],
                 z=orbits[2][:, 2],
                 type='scatter3d',
                 mode='lines',
                 line=dict(width=2, color='green'),
                 name="Órbita de La Tierra"),
            dict(x=orbits[3][:, 0],
                 y=orbits[3][:, 1],
                 z=orbits[3][:, 2],
                 type='scatter3d',
                 mode='lines',
                 line=dict(width=2, color='red'),
                 name="Órbita de Marte"),
            dict(x=[planets[0][0][0]],
                 y=[planets[0][0][1]],
                 z=[planets[0][0][2]],
                 type='scatter3d',
                 mode='markers',
                 marker=dict(
                     size=5,
                     color='rgba(0, 0, 150, .8)',
                     line=dict(
                         width=1,
                         color='rgb(0, 0, 0)')),
                 name="Mercurio: día 0"),
            dict(x=[planets[1][0][0]],
                 y=[planets[1][0][1]],
                 z=[planets[1][0][2]],
                 type='scatter3d',
                 mode='markers',
                 marker=dict(
                     size=5,
                     color='rgba(255, 140, 0, .8)',
                     line=dict(
                         width=1,
                         color='rgb(0, 0, 0)')),
                 name="Venus: día 0"),
            dict(x=[planets[2][0][0]],
                 y=[planets[2][0][1]],
                 z=[planets[2][0][2]],
                 type='scatter3d',
                 mode='markers',
                 marker=dict(
                     size=5,
                     color='rgba(0, 250, 0, .8)',
                     line=dict(
                         width=1,
                         color='rgb(0, 0, 0)')),
                 name="La Tierra: día 0"),
            dict(x=[planets[3][0][0]],
                 y=[planets[3][0][1]],
                 z=[planets[3][0][2]],
                 type='scatter3d',
                 mode='markers',
                 marker=dict(
                     size=5,
                     color='rgba(250, 0, 0, .8)',
                     line=dict(
                         width=1,
                         color='rgb(0, 0, 0)')),
                 name="Marte: día 0")
        ]

        frames = [
            dict(data=[
                dict(x=[0], y=[0], z=[0],
                     type='scatter3d',
                     mode='markers',
                     marker=dict(
                         size=10,
                         color='rgba(230, 230, 0, .9)',
                         line=dict(width=1, color='rgb(100,100,0)')
                     ),
                     name='Sol'),
                dict(x=orbits[0][:, 0],
                     y=orbits[0][:, 1],
                     z=orbits[0][:, 2],
                     type='scatter3d',
                     mode='lines',
                     line=dict(width=2, color='blue'),
                     name="Órbita de Mercurio"),
                dict(x=orbits[1][:, 0],
                     y=orbits[1][:, 1],
                     z=orbits[1][:, 2],
                     type='scatter3d',
                     mode='lines',
                     line=dict(width=2, color='orange'),
                     name="Órbita de Venus"),
                dict(x=orbits[2][:, 0],
                     y=orbits[2][:, 1],
                     z=orbits[2][:, 2],
                     type='scatter3d',
                     mode='lines',
                     line=dict(width=2, color='green'),
                     name="Órbita de La Tierra"),
                dict(x=orbits[3][:, 0],
                     y=orbits[3][:, 1],
                     z=orbits[3][:, 2],
                     type='scatter3d',
                     mode='lines',
                     line=dict(width=2, color='red'),
                     name="Órbita de Marte"),
                dict(x=[planets[0][i][0]],
                     y=[planets[0][i][1]],
                     z=[planets[0][i][2]],
                     type='scatter3d',
                     mode='markers',
                     marker=dict(
                         size=5,
                         color='rgba(0, 0, 150, .8)',
                         line=dict(
                             width=1,
                             color='rgb(0, 0, 0)')),
                     name="Mercurio: día {}".format(steps*i)),
                dict(x=[planets[1][i][0]],
                     y=[planets[1][i][1]],
                     z=[planets[1][i][2]],
                     type='scatter3d',
                     mode='markers',
                     marker=dict(
                         size=5,
                         color='rgba(255, 140, 0, .8)',
                         line=dict(
                             width=1,
                             color='rgb(0, 0, 0)')),
                     name="Venus: día {}".format(steps*i)),
                dict(x=[planets[2][i][0]],
                     y=[planets[2][i][1]],
                     z=[planets[2][i][2]],
                     type='scatter3d',
                     mode='markers',
                     marker=dict(
                         size=5,
                         color='rgba(0, 250, 0, .8)',
                         line=dict(
                             width=1,
                             color='rgb(0, 0, 0)')),
                     name="La Tierra: día {}".format(steps*i)),
                dict(x=[planets[3][i][0]],
                     y=[planets[3][i][1]],
                     z=[planets[3][i][2]],
                     type='scatter3d',
                     mode='markers',
                     marker=dict(
                         size=5,
                         color='rgba(250, 0, 0, .8)',
                         line=dict(
                             width=1,
                             color='rgb(0, 0, 0)')),
                     name="Marte: día {}".format(steps*i)),
                ]) for i in range(len(planets[0]))]
        
        fig = dict(data=data, layout=layout, frames=frames)
        py.iplot(fig, filename='plots/inner_planets_plot')

    def display_outer_planets(self):

        steps = 1000
        orbits = [planet.get_orbit(60) for planet in self.outer_planets]
        planets = [[planet.position(i) for i in range(0, 61000, steps)]
                   for planet in self.outer_planets]

        rng = int(1.2*self.outer_planets[-1].a) + 1

        axis3d = dict(
            showbackground=True,
            backgroundcolor="rgb(230, 230, 230)",
            gridcolor="rgb(255, 255, 255)",
            zerolinecolor="rgb(255, 255, 255)",
        )

        layout = dict(
            width=600, height=500,
            scene=dict(xaxis=(axis3d),
                       yaxis=(axis3d),
                       zaxis=dict(axis3d,
                                  **dict(range=[-rng, rng],
                                         autorange=False)),
                       aspectratio=dict(x=1, y=1, z=1)),
            title='Movimiento orbital de los planetas exteriores',
            hovermode='closest',
            updatemenus=[
                {
                    'type': 'buttons',
                    'buttons': [
                        {
                            'label': 'Iniciar',
                            'method': 'animate',
                            'args': [None, dict(
                                frame=dict(duration=0),
                                transition=dict(duration=100),
                                fromcurrent=True,
                            )],
                        }
                    ]
                }
            ]
        )
        
        data = [
            dict(x=[0], y=[0], z=[0],
                 type='scatter3d',
                 mode='markers',
                 marker=dict(
                     size=10,
                     color='rgba(230, 230, 0, .9)',
                     line=dict(width=1, color='rgb(100,100,0)')
                 ),
                 name='Sol'),
            dict(x=orbits[0][:, 0],
                 y=orbits[0][:, 1],
                 z=orbits[0][:, 2],
                 type='scatter3d',
                 mode='lines',
                 line=dict(width=2, color='blue'),
                 name="Órbita de Júpiter"),
            dict(x=orbits[1][:, 0],
                 y=orbits[1][:, 1],
                 z=orbits[1][:, 2],
                 type='scatter3d',
                 mode='lines',
                 line=dict(width=2, color='orange'),
                 name="Órbita de Saturno"),
            dict(x=orbits[2][:, 0],
                 y=orbits[2][:, 1],
                 z=orbits[2][:, 2],
                 type='scatter3d',
                 mode='lines',
                 line=dict(width=2, color='green'),
                 name="Órbita de Urano"),
            dict(x=orbits[3][:, 0],
                 y=orbits[3][:, 1],
                 z=orbits[3][:, 2],
                 type='scatter3d',
                 mode='lines',
                 line=dict(width=2, color='red'),
                 name="Órbita de Neptuno"),
            dict(x=[planets[0][0][0]],
                 y=[planets[0][0][1]],
                 z=[planets[0][0][2]],
                 type='scatter3d',
                 mode='markers',
                 marker=dict(
                     size=5,
                     color='rgba(0, 0, 150, .8)',
                     line=dict(
                         width=1,
                         color='rgb(0, 0, 0)')),
                 name="Júpiter: día 0"),
            dict(x=[planets[1][0][0]],
                 y=[planets[1][0][1]],
                 z=[planets[1][0][2]],
                 type='scatter3d',
                 mode='markers',
                 marker=dict(
                     size=5,
                     color='rgba(255, 140, 0, .8)',
                     line=dict(
                         width=1,
                         color='rgb(0, 0, 0)')),
                 name="Saturno: día 0"),
            dict(x=[planets[2][0][0]],
                 y=[planets[2][0][1]],
                 z=[planets[2][0][2]],
                 type='scatter3d',
                 mode='markers',
                 marker=dict(
                     size=5,
                     color='rgba(0, 250, 0, .8)',
                     line=dict(
                         width=1,
                         color='rgb(0, 0, 0)')),
                 name="Urano: día 0"),
            dict(x=[planets[3][0][0]],
                 y=[planets[3][0][1]],
                 z=[planets[3][0][2]],
                 type='scatter3d',
                 mode='markers',
                 marker=dict(
                     size=5,
                     color='rgba(250, 0, 0, .8)',
                     line=dict(
                         width=1,
                         color='rgb(0, 0, 0)')),
                 name="Neptuno: día 0")
        ]

        frames = [
            dict(data=[
                dict(x=[0], y=[0], z=[0],
                     type='scatter3d',
                     mode='markers',
                     marker=dict(
                         size=10,
                         color='rgba(230, 230, 0, .9)',
                         line=dict(width=1, color='rgb(100,100,0)')
                     ),
                     name='Sol'),
                dict(x=orbits[0][:, 0],
                     y=orbits[0][:, 1],
                     z=orbits[0][:, 2],
                     type='scatter3d',
                     mode='lines',
                     line=dict(width=2, color='blue'),
                     name="Órbita de Júpiter"),
                dict(x=orbits[1][:, 0],
                     y=orbits[1][:, 1],
                     z=orbits[1][:, 2],
                     type='scatter3d',
                     mode='lines',
                     line=dict(width=2, color='orange'),
                     name="Órbita de Saturno"),
                dict(x=orbits[2][:, 0],
                     y=orbits[2][:, 1],
                     z=orbits[2][:, 2],
                     type='scatter3d',
                     mode='lines',
                     line=dict(width=2, color='green'),
                     name="Órbita de Urano"),
                dict(x=orbits[3][:, 0],
                     y=orbits[3][:, 1],
                     z=orbits[3][:, 2],
                     type='scatter3d',
                     mode='lines',
                     line=dict(width=2, color='red'),
                     name="Órbita de Neptuno"),
                dict(x=[planets[0][i][0]],
                     y=[planets[0][i][1]],
                     z=[planets[0][i][2]],
                     type='scatter3d',
                     mode='markers',
                     marker=dict(
                         size=5,
                         color='rgba(0, 0, 150, .8)',
                         line=dict(
                             width=1,
                             color='rgb(0, 0, 0)')),
                     name="Júpiter: día {}".format(steps*i)),
                dict(x=[planets[1][i][0]],
                     y=[planets[1][i][1]],
                     z=[planets[1][i][2]],
                     type='scatter3d',
                     mode='markers',
                     marker=dict(
                         size=5,
                         color='rgba(255, 140, 0, .8)',
                         line=dict(
                             width=1,
                             color='rgb(0, 0, 0)')),
                     name="Saturno: día {}".format(steps*i)),
                dict(x=[planets[2][i][0]],
                     y=[planets[2][i][1]],
                     z=[planets[2][i][2]],
                     type='scatter3d',
                     mode='markers',
                     marker=dict(
                         size=5,
                         color='rgba(0, 250, 0, .8)',
                         line=dict(
                             width=1,
                             color='rgb(0, 0, 0)')),
                     name="Urano: día {}".format(steps*i)),
                dict(x=[planets[3][i][0]],
                     y=[planets[3][i][1]],
                     z=[planets[3][i][2]],
                     type='scatter3d',
                     mode='markers',
                     marker=dict(
                         size=5,
                         color='rgba(250, 0, 0, .8)',
                         line=dict(
                             width=1,
                             color='rgb(0, 0, 0)')),
                     name="Neptuno: día {}".format(steps*i)),
                ]) for i in range(len(planets[0]))]
        
        fig = dict(data=data, layout=layout, frames=frames)
        py.iplot(fig, filename='plots/outer_planets_plot')


class Displayer:

    def compare_eccentric_anomalies(self, planet, time):
        print("Anomalía excéntrica de {} el día {},"
              .format(planet.name, time) +
              "calculada usando funciones de Bessel: {}"
              .format(planet.eccentric_annomaly_bessel(time, 20)))

        print("Anomalía excéntrica de {} el día {},"
              .format(planet.name, time) +
              "calculada por el método de Newton: {}"
              .format(planet.eccentric_annomaly(time)))

        print("Diferencia entre ambos valores: {}"
              .format(abs(planet.eccentric_annomaly_bessel(time, 20) -
                          planet.eccentric_annomaly(time))))

    def print_information(self, planet, time):

        print("Posición de {} en el día {}: {}"
              .format(planet.name, time, planet.position(time)))

        print("Distancia al sol de {} en el día {}: {}\n"
              .format(planet.name, time, planet.distance_to_sun(time)))

        print("Velocidad de {} en el día {}: {}"
              .format(planet.name, time, planet.speed(time)))

        print("Módulo de la velocidad de {} en el día {}: {}\n"
              .format(planet.name, time, planet.speed_module(time)))

        print("Anomalía real de {} en el día {}: {}"
              .format(planet.name, time, planet.real_annomaly(time)))

        print("Anomalía real de {} en el día {}"
              .format(planet.name, time) +
              " (cálculo a partir de la anomalía excéntrica): {}\n"
              .format(planet.real_annomaly_from_eccentric(time)))

        print("Energía de {} en el día {}: {}"
              .format(planet.name, time, planet.energy_from_time(time)))

        print("Energía (constante) de {}: {}\n"
              .format(planet.name, planet.energy()))

        print("Momento angular de {} en el día {}: {}"
              .format(planet.name, time,
                      planet.angular_moment_from_time(time)))
        print("Módulo del momento angular de {} en el día {}: {}"
              .format(planet.name, time,
                      np.linalg.norm(planet.angular_moment_from_time(time))))
        print("Módulo del momento angular de {} (constante): {}\n"
              .format(planet.name, planet.c))

        self.compare_eccentric_anomalies(planet, time)

    def display_orbit(self, planet, time):

        xs = planet.get_orbit(200)

        orbit = go.Scattergl(x=xs[:, 0], y=xs[:, 1],
                             name='órbita')

        position = planet.position(time)
        planet_pos = go.Scattergl(x=[position[0]], y=[position[1]],
                                  mode='markers',
                                  marker=dict(
                                      size=15,
                                      color='rgba(152, 0, 0, .8)',
                                      line=dict(
                                          width=2,
                                          color='rgb(0, 0, 0)'
                                      )
                                  ),
                                  name='{}: día {}'
                                  .format(planet.name, time))

        sun = go.Scattergl(x=[0], y=[0],
                           mode='markers',
                           marker=dict(
                               size=20,
                               color='rgba(230, 230, 0, .9)',
                               line=dict(width=1, color='rgb(100,100,0)')
                           ),
                           name='Sol')

        rng = int(1.2*planet.a) + 1

        layout = go.Layout(
            width=600, height=500,
            xaxis=dict(
                anchor='y',
                range=[-rng, rng]
            ),
            yaxis=dict(
                anchor='x',
                autorange=False,
                range=[-rng, rng],
            )
        )
        data = [orbit, planet_pos, sun]
        fig = go.Figure(data=data, layout=layout)
        py.iplot(fig, filename='plots/orbit_plot')
