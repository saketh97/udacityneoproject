from collections import namedtuple
from enum import Enum
from datetime import datetime
from exceptions import UnsupportedFeature
from models import NearEarthObject
from models import OrbitPath
import operator


class Query(object):
    """
    Object representing the desired search query operation to build.
    The Query uses the Selectors to structure the query information
    into a format the NEOSearcher can use for date search.
    """

    Selectors = namedtuple('Selectors', ['date_search',
                           'number', 'filters', 'return_object'])
    DateSearch = namedtuple('DateSearch', ['type', 'values'])
    ReturnObjects = {'NEO': NearEarthObject, 'Path': OrbitPath}

    def __init__(self, **kwargs):
        """
        :param kwargs: dict of search query parameters to determine
        which SearchOperation query to use

        if any key kwargs does not have value
        it will show None so lets handle it.
        """

        self.kwargs = {}
        for key, value in kwargs.items():
            if kwargs[key] is not None:
                self.kwargs[key] = value

        self.number = 0
        self.to_return = 'NEO'
        self.dates = Query.DateSearch('e', 0)
        self.filters = {}

    def build_query(self):
        """
        Transforms the provided query options, set upon initialization,
        into a set of Selectors that the NEOSearcher
        can use to perform the appropriate search functionality

        :return: QueryBuild.Selectors namedtuple that translates
        the dict of query options into a SearchOperation
        """

        if('start_date' in self.kwargs.keys()):
            value = self.kwargs['start_date']+','+self.kwargs['end_date']
            self.dates = Query.DateSearch('between', value)

        else:
            self.dates = Query.DateSearch('equals', self.kwargs['date'])

        self.number = self.kwargs['number']
        self.to_return = self.kwargs['return_object']

        if('filter' in self.kwargs.keys()):
            self.filters = Filter.create_filter_options(self.kwargs['filter'])

        return Query.Selectors(self.dates, self.number,
                               self.filters, self.to_return)


class Filter(object):
    """
    Object representing optional filter options to be used
    in the date search for Near Earth Objects.

    Each filter is one of Filter.Operators provided
    with a field to filter on a value.
    """

    Options = {
        'distance': 'miss_distance_kilometers',
        'diameter': 'diameter_min_km',
        'is_hazardous': 'is_potentially_hazardous_asteroid'
    }

    Operators = {
        '<': operator.lt,
        '>': operator.gt,
        '=': operator.eq,
        '<=': operator.le,
        '>=': operator.ge
    }

    def __init__(self, field, object, operation, value):
        """
        :param field:  str representing field to filter on
        :param field:  str representing object to filter on
        :param operation: str representing filter operation to perform
        :param value: str representing value to filter for
        """

        self.field = field
        self.object = object
        self.operation = operation
        self.value = value

    @staticmethod
    def create_filter_options(filter_options):
        """
        Class function that transforms filter options raw input into filters

        :param input: list in format
        ["filter_option:operation:value_of_option", ...]

        :return: defaultdict with key of NearEarthObject or
        OrbitPath and value of empty list or list of Filters
        """

        filter_dict = {'NearEarthObject': [], 'OrbitPath': []}

        for filter in filter_options:
            elements_in_filter = filter.split(":")

            if(elements_in_filter[0] == 'diameter' or
               elements_in_filter[0] == 'is_hazardous'):

                filter_dict['NearEarthObject'].append(
                    Filter(elements_in_filter[0], 'NEO',
                           elements_in_filter[1], elements_in_filter[2]))

            elif (elements_in_filter[0] == 'distance'):
                filter_dict['OrbitPath'].append(Filter(elements_in_filter[0],
                                                       'orbit',
                                                       elements_in_filter[1],
                                                       elements_in_filter[2]))

        return filter_dict

    def apply(self, results):
        """
        Function that applies the filter operation onto a set of results

        :param results: List of Near Earth Object results
        :return: filtered list of Near Earth Object results
        """

        filtered_neos = []
        test = False

        for neo in results:

            if(self.object == 'NEO'):
                value = getattr(neo, self.Options[self.field])

                if(self.field == 'is_hazardous'):
                    self.value = bool(self.value)

                else:
                    self.value = float(self.value)
                test = self.Operators[self.operation](value, self.value)

            elif(self.object == 'orbit'):

                for orbit in neo.orbits:
                    value = getattr(orbit, self.Options[self.field])
                    self.value = float(self.value)
                    test = self.Operators[self.operation](value, self.value)

                    if(test):
                        break

            if(test):
                filtered_neos.append(neo)

        return filtered_neos
        # TODO: Takes a list of NearEarthObjects and applies
        # the value of its filter operation to the results


class NEOSearcher(object):
    """
    Object with date search functionality on Near Earth Objects
    exposed by a generic search interface get_objects, which,
     based on the query specifications, determines
    how to perform the search.
    """

    def __init__(self, db):
        """
        :param db: NEODatabase holding the NearEarthObject instances
        and their OrbitPath instances
        """

        self.db = db

    def get_objects(self, query):
        """
        Generic search interface that, depending on
        the details in the QueryBuilder (query) calls theappropriate instance
        search function, then applys any filters, with distance as
        the last filter.

        Once any filters provided are applied, return the number of requested
        objects in the query.return_object specified.

        :param query: Query.Selectors object with query information
        :return: Dataset of NearEarthObjects or OrbitalPaths
        """

        # TODO: This is a generic method that will need to understand,
        # using DateSearch, how to implement search

        # TODO: Write instance methods that get_objects can use
        # to implement the two types of DateSearch your project

        # TODO: needs to support that then your filters can be applied to.
        # Remember to return the number specified in

        # TODO: the Query.Selectors as well as in the return_type
        # from Query.Selectors

        date = query[0]
        count = query[1]
        filters = query[2]
        neos_list = []
        neo_names = []

        if('equals' in date[0]):

            try:
                neo_names = self.db.orbits[date[1]]
                neo_names = set(neo_names)
                for name in neo_names:
                    neos_list.append(self.db.neos[name])
                    if(count == 0):
                        break

            except Exception as e:
                neo_list = []

        elif('between' in date[0]):
            start = date[1].split(',')[0]
            end = date[1].split(',')[1]
            neo_names = []

            for key in self.db.orbits.keys():

                if((datetime.strptime(start, "%Y-%m-%d") <=
                    datetime.strptime(key, "%Y-%m-%d")) and
                    (datetime.strptime(end, "%Y-%m-%d") >=
                     datetime.strptime(key, "%Y-%m-%d"))):

                    for value in self.db.orbits[key]:
                        neo_names.append(value)

            neo_names = set(neo_names)

            for name in neo_names:
                neos_list.append(self.db.neos[name])

                if(count == 0):
                    break

        for key, value in filters.items():

            for filt in value:
                neos_list = filt.apply(neos_list)

        return neos_list[0:10]
