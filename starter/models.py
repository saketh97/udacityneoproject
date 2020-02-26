class NearEarthObject(object):
    """
    Object containing data describing a Near Earth Object and it's orbits.

    # TODO: You may be adding instance methods to NearEarthObject
    to help you implement search and output data.
    """

    def __init__(self, **kwargs):
        """
        :param kwargs:    dict of attributes about a given Near Earth Object,
        only a subset of attributes used
        """

        self.orbits = []
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.diameter_min_km = float(kwargs['estimated_diameter_min_kilometers'
                                            ])
        if (kwargs['is_potentially_hazardous_asteroid'] == 'False'):
            self.is_potentially_hazardous_asteroid = bool(0)
        else:
            self.is_potentially_hazardous_asteroid = bool(1)
        self.orbits.append(OrbitPath(**kwargs))

    def update_orbits(self, orbit):
        """
        Adds an orbit path information to a Near Earth Object list of orbits.
        Before adding the orbit it will check if the orbit already exists in
        orbits list for that we use eq function of the orbit class.

        :param orbit: OrbitPath
        :return: None
        """
        orbit_exists = 0
        for orbit_list_elem in self.orbits:
            if(orbit_list_elem.__eq__(orbit)):
                orbit_exists = 1
                break
        if(orbit_exists == 0):
            self.orbits.append(orbit)

    def __str__(self):
        return "id:%s=>name:%s=>orbits:%s=>orbitdates:%s" % (
                self.id, self.name,
                ", ".join(str(orbit) for orbit in self.orbits),
                ", ".join(str(orbit.close_approach_date)
                          for orbit in self.orbits)
                )


class OrbitPath(object):
    """
    Object containing data describing a Near Earth Object orbit.

    # TODO: You may be adding instance methods to OrbitPath to help you
    implement search and output data.
    """

    def __init__(self, **kwargs):
        """
        :param kwargs:    dict of attributes about a given orbit,
        only a subset of attributes used
        """
        self.neo_name = kwargs['name']
        self.miss_distance_kilometers = float(
                                             kwargs['miss_distance_kilometers']
                                                )

        self.close_approach_date = kwargs['close_approach_date']

    def __eq__(self, other):
        """
        equals method returns true if the close approach date
        and miss distance is same for two orbits of same neo.
        Else it will return false
        """
        return ((self.close_approach_date == other.close_approach_date)
                and (self.miss_distance_kilometers ==
                     other.miss_distance_kilometers))

    def __str__(self):
        return ("neo_name =%s / distance=%s / date=%s" % (
                self.neo_name, str(self.miss_distance_kilometers),
                str(self.close_approach_date)))
