from models import OrbitPath, NearEarthObject


class NEODatabase(object):
    """
    Object to hold Near Earth Objects and their orbits.

    To support optimized date searching, a dict mapping of all orbit date paths
    to the Near Earth Objectsrecorded on a given day is maintained.
    Additionally, all unique instances of a Near Earth Object are contained in
    a dict mapping the Near Earth Object name to the NearEarthObject instance.
    """

    def __init__(self, filename):
        """
        :param filename: str representing the pathway of the filename
        containing the Near Earth Object data
        """
        self.filename = filename
        self.orbits = {}
        self.neos = {}

    def load_data(self, filename=None):
        """
        Loads data from a .csv file, instantiating Near Earth Objects
        and their OrbitPaths by:
           - Storing a dict of orbit date to list of NearEarthObject instances
           - Storing a dict of the Near Earth Object name to
           the single instance of NearEarthObject

        :param filename:
        :return:
        """

        if not (filename or self.filename):
            raise Exception('Cannot load data, no filename provided')

        filename = filename or self.filename
        try:
            neo_data_file = open(filename, 'r')
            columns_in_data = neo_data_file.readline().split(',')
            line_by_line = neo_data_file.readlines()
            for line in line_by_line:
                data = line.split(',')
                data_dict = {columns_in_data[i]: data[i] for i in range(
                                                        len(columns_in_data))}
                if(data_dict['name'] in self.neos.keys()):
                    orbit = OrbitPath(**data_dict)
                    self.neos[orbit.neo_name].update_orbits(orbit)
                    if(data_dict['close_approach_date'] in self.orbits.keys()):
                        self.orbits[data_dict['close_approach_date']].append(
                                                                orbit.neo_name)
                    else:
                        self.orbits[orbit.close_approach_date] = [
                                                                orbit.neo_name]
                else:
                    neo = NearEarthObject(**data_dict)
                    self.neos[neo.name] = neo
                    if(data_dict['close_approach_date'] in self.orbits.keys()):
                        self.orbits[data_dict['close_approach_date']].append(
                                                                      neo.name)
                    else:
                        self.orbits[data_dict['close_approach_date']] = [
                                                                    neo.name]
        finally:
            neo_data_file.close()
            # Next step to create dicts to store orbits,neo objects

        # TODO: Load data from csv file.
        # TODO: Where will the data be stored?

        return None
