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
        for key,value in kwargs.items():
            if(key in ['id','name','estimated_diameter_min_kilometers','is_potentially_hazardous_asteroid']):
                self.key = value
        self.list_of_orbits.append(OrbitPath(kwargs))

    def update_orbits(self, orbit):
        """
        Adds an orbit path information to a Near Earth Object list of orbits

        :param orbit: OrbitPath
        :return: None
        """

        self.list_of_orbits.append(orbit)

    def __str__(self):
        return ("id:"+self.id+" name:"+self.name+" diameter:"+self.estimated_diameter_min_kilometers+" is hazardous:"+self.is_potentially_hazardous_asteroid)


class OrbitPath(object):
    """
    Object containing data describing a Near Earth Object orbit.

    # TODO: You may be adding instance methods to OrbitPath to help you implement search and output data.
    """

    def __init__(self, **kwargs):
        """
        :param kwargs:    dict of attributes about a given orbit, only a subset of attributes used
        """

        for key,value in kwargs.items():
            if(key in ['name','miss_distance_kilometers','close_approach_date']):
                self.key = value


    def __str__(self):
        return ("neo_name:"+self.name+" distance:"+self.miss_distance_kilometers+" date:"+self.close_approach_date)
