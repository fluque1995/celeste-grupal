import numpy as np
import utils
import scipy.special as sp


class Planet:
    def __init__(self, name, epsilon, a, period, mass, i, omega, bar_omega):
        self.name = name
        self.epsilon = epsilon
        self.a = a
        self.period = period
        self.orbit = None
        self.orbit_2d = None
        self.orbit_2bodies = None
        self.mass = mass

        self.mu = 4*np.pi**2*self.a**3/self.period**2
        self.c = np.sqrt(self.mu*self.a*(1-epsilon**2))
        self.i = np.deg2rad(i)
        self.omega = np.deg2rad(omega)
        self.bar_omega = np.deg2rad(bar_omega)
        ux = np.cos(self.omega)
        uy = np.sin(self.omega)

        self.rot_mat = np.dot(
            np.array(
                [np.cos(self.i) + ux**2*(1-np.cos(self.i)),
                 ux*uy*(1-np.cos(self.i)),
                 uy*np.sin(self.i),
                 ux*uy*(1-np.cos(self.i)),
                 np.cos(self.i) + uy**2*(1-np.cos(self.i)),
                 -ux*np.sin(self.i),
                 -uy*np.sin(self.i),
                 ux*np.sin(self.i),
                 np.cos(self.i)]
            ).reshape(3, 3),
            np.array(
                [np.cos(self.bar_omega), -np.sin(self.bar_omega), 0,
                 np.sin(self.bar_omega), np.cos(self.bar_omega), 0,
                 0, 0, 1]
            ).reshape(3, 3)
        )

    def __str__(self):
        return self.name

    def __gt__(self, planet):
        return self.a > planet.a

    def get_time_in_period(self, time):
        return time % self.period

    def position(self, time):

        time = self.get_time_in_period(time)
        eccentric_annomaly = utils.eccentric_annomaly(
            self.period,
            self.epsilon,
            time
        )

        position = np.dot(self.rot_mat, [
            self.a*(np.cos(eccentric_annomaly) - self.epsilon)[0],
            self.a*np.sqrt(1-self.epsilon**2)*np.sin(eccentric_annomaly)[0],
            0
        ])

        return position

    def position_2d(self, time):

        time = self.get_time_in_period(time)
        eccentric_annomaly = utils.eccentric_annomaly(
            self.period,
            self.epsilon,
            time
        )

        position = [
            self.a*(np.cos(eccentric_annomaly) - self.epsilon)[0],
            self.a*np.sqrt(1-self.epsilon**2)*np.sin(eccentric_annomaly)[0]
        ]

        return position

    def distance_to_sun(self, time):
        return np.linalg.norm(self.position(time))

    def speed(self, time):

        time = self.get_time_in_period(time)
        eccentric_annomaly = utils.eccentric_annomaly(
            self.period,
            self.epsilon,
            time
        )

        denom = self.period*(1-self.epsilon*np.cos(eccentric_annomaly))
        quotient = 2*np.pi*self.a/denom

        speed = np.dot(self.rot_mat, [
            (-quotient*np.sin(eccentric_annomaly))[0],
            (quotient *
             np.sqrt(1 - self.epsilon**2)*np.cos(eccentric_annomaly))[0],
            0
        ])

        return speed

    def speed_2d(self, time):

        time = self.get_time_in_period(time)
        eccentric_annomaly = utils.eccentric_annomaly(
            self.period,
            self.epsilon,
            time
        )

        denom = self.period*(1-self.epsilon*np.cos(eccentric_annomaly))
        quotient = 2*np.pi*self.a/denom

        speed = [
            (-quotient*np.sin(eccentric_annomaly))[0],
            (quotient *
             np.sqrt(1 - self.epsilon**2)*np.cos(eccentric_annomaly))[0]
        ]

        return speed

    def speed_2bodies(self, time):
        G = 6.674*10**(-11)
        sun_mass = 1.989*10**30
        mu = 8.9546188*10**(-25)*G*sun_mass**3/(self.mass + sun_mass)**2
        period = np.sqrt(4*np.pi**2*self.a**3/mu)

        time = self.get_time_in_period(time)
        eccentric_annomaly = utils.eccentric_annomaly(
            period,
            self.epsilon,
            time
        )

        denom = period*(1-self.epsilon*np.cos(eccentric_annomaly))
        quotient = 2*np.pi*self.a/denom

        speed = [
            (-quotient*np.sin(eccentric_annomaly))[0],
            (quotient *
             np.sqrt(1 - self.epsilon**2)*np.cos(eccentric_annomaly))[0]
        ]

        return speed

    def speed_module(self, time):
        return np.linalg.norm(self.speed(time))

    def real_annomaly_deriv(self, t, theta):
        num = self.c*(1 + self.epsilon*np.cos(theta))**2
        denom = (self.a**2*(1 - self.epsilon**2)**2)
        return num/denom

    def real_annomaly_2bodies_deriv(self, t, theta):
        G = 6.674*10**(-11)
        sun_mass = 1.989*10**30
        mu = 8.9546188*10**(-25)*G*sun_mass**3/(self.mass + sun_mass)**2
        c = np.sqrt(mu*self.a*(1-self.epsilon**2))
        num = c*(1 + self.epsilon*np.cos(theta))**2
        denom = (self.a**2*(1 - self.epsilon**2)**2)
        return num/denom

    def position_2bodies(self, time):
        theta = utils.runge_kutta(self.real_annomaly_2bodies_deriv,
                                  0, 0, time, 4000)

        constant = self.a*(1 - self.epsilon**2)/(1 + self.epsilon*np.cos(theta))
        return [constant*np.cos(theta), constant*np.sin(theta)]

    def real_annomaly(self, time):
        time = self.get_time_in_period(time)
        return utils.runge_kutta(self.real_annomaly_deriv, 0, 0, time, 5000)

    def energy(self):
        return -self.c**2/(2*self.a**2*(1-self.epsilon**2))

    def energy_from_time(self, time):
        return (self.speed_module(time)**2/2 -
                self.mu/self.distance_to_sun(time))

    def angular_moment_from_time(self, time):
        time = self.get_time_in_period(time)
        real_annomaly = self.real_annomaly(time)
        return np.dot(self.rot_mat,
                      [0, 0, (self.distance_to_sun(time)**2 *
                              self.real_annomaly_deriv(time, real_annomaly))])

    def real_annomaly_from_eccentric(self, time):
        ecc_an = utils.eccentric_annomaly(self.period,
                                          self.epsilon,
                                          time)
        real_an = np.arccos((np.cos(ecc_an)[0] - self.epsilon) /
                            (1 - self.epsilon*np.cos(ecc_an)[0]))
        real_an = real_an if 2*time < self.period else 2*np.pi - real_an
        return real_an

    def get_orbit(self, npoints):
        if self.orbit is None:
            ts = list(np.arange(0, self.period, self.period/npoints))
            self.orbit = [self.position(t) for t in ts]
            self.orbit.append(self.orbit[0])
            self.orbit = np.asarray(self.orbit)
        return self.orbit

    def get_orbit_2d(self, npoints):
        if self.orbit_2d is None:
            ts = list(np.arange(0, self.period, self.period/npoints))
            self.orbit_2d = [self.position(t) for t in ts]
            self.orbit_2d.append(self.orbit_2d[0])
            self.orbit_2d = np.asarray(self.orbit_2d)
        return self.orbit_2d

    def get_orbit_2bodies(self, npoints):
        
        if self.orbit_2bodies is None:
            G = 6.674*10**(-11)
            sun_mass = 1.989*10**30
            mu = 8.9546188*10**(-25)*G*sun_mass**3/(self.mass + sun_mass)**2
            period = np.sqrt(4*np.pi**2*self.a**3/mu)
            ts = list(np.arange(0, period, period/npoints))
            self.orbit_2bodies = [self.position_2bodies(t) for t in ts]
            self.orbit_2bodies.append(self.orbit_2bodies[0])
            self.orbit_2bodies = np.asarray(self.orbit_2bodies)
        return self.orbit_2bodies

    def mass_center(self, time):
        sun_mass = 1.989*10**30
        quotient = self.mass/(self.mass + sun_mass)
        pos = np.array(self.position_2bodies(0))
        speed = np.array(self.speed_2bodies(0))
        alpha = quotient*pos
        beta = quotient*speed
        return alpha + beta*time

    def get_positions_2bodies(self, time):
        planet_pos = self.position_2bodies(time)
        sun_pos = np.array([0, 0])
        mass_center = self.mass_center(time)
        return np.array([planet_pos + mass_center,
                         sun_pos + mass_center])

    def eccentric_annomaly(self, time):
        time = self.get_time_in_period(time)
        return utils.eccentric_annomaly(self.period,
                                        self.epsilon,
                                        time)[0]

    def eccentric_annomaly_bessel(self, time, nfuncs):
        time = self.get_time_in_period(time)
        ji = 2*np.pi*time/self.period
        ecc_an = ji

        for i in range(nfuncs):
            bessel = sp.jv((i+1), (i+1)*self.epsilon)
            ecc_an += (2/(i+1))*bessel*np.sin((i+1)*ji)

        return ecc_an
