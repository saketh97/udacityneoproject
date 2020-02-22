class NearEarthObject(object):
    """
    Object containing data describing a Near Earth Object and it's orbits.

    # TODO: You may be adding instance methods to NearEarthObject to help you implement search and output data.
    """

    def __init__(self, **kwargs):
        """
        :param kwargs:    dict of attributes about a given Near Earth Object, only a subset of attributes used
        """

        self.list_of_orbits = []
        self.id = kwargs['id']
        self.name =kwargs['name']
        self.estimated_diameter_min_kilometers = kwargs['estimated_diameter_min_kilometers']
        self.is_potentially_hazardous_asteroid = kwargs['is_potentially_hazardous_asteroid']
        self.list_of_orbits.append(OrbitPath(**kwargs))

    def update_orbits(self, orbit):
        """
        Adds an orbit path information to a Near Earth Object list of orbits

        :param orbit: OrbitPath
        :return: None
        """

        self.list_of_orbits.append(orbit)

    def __repr__(self):
        return ('id:'+self.id+' name:'+self.name+' diameter:'+self.estimated_diameter_min_kilometers+' is hazardous:'+self.is_potentially_hazardous_asteroid)


class OrbitPath(object):
    """
    Object containing data describing a Near Earth Object orbit.

    # TODO: You may be adding instance methods to OrbitPath to help you implement search and output data.
    """

    def __init__(self, **kwargs):
        """
        :param kwargs:    dict of attributes about a given orbit, only a subset of attributes used
        """
        self.name = kwargs['name']
        self.miss_distance_kilometers = kwargs['miss_distance_kilometers']
        self.close_approach_date = kwargs['close_approach_date']


    def __repr__(self):
        return ('neo_name:'+self.name+' distance:'+self.miss_distance_kilometers+' date:'+self.close_approach_date)
