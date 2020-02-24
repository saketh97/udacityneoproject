from enum import Enum
import pandas as pd
import pathlib

class OutputFormat(Enum):
    """
    Enum representing supported output formatting options for search results.
    """
    display = 'display'
    csv_file = 'csv_file'

    @staticmethod
    def list():
        """
        :return: list of string representations of OutputFormat enums
        """
        return list(map(lambda output: output.value, OutputFormat))


class NEOWriter(object):
    """
    Python object use to write the results from supported output formatting options.
    """

    def __init__(self):
        # TODO: How can we use the OutputFormat in the NEOWriter?
        pass

    def write(self, format, data, **kwargs):
        """
        Generic write interface that, depending on the OutputFormat selected calls the
        appropriate instance write function

        :param format: str representing the OutputFormat
        :param data: collection of NearEarthObject or OrbitPath results
        :param kwargs: Additional attributes used for formatting output e.g. filename
        :return: bool representing if write successful or not
        """
        # TODO: Using the OutputFormat, how can we organize our 'write' logic for output to stdout vs to csvfile
        # TODO: into instance methods for NEOWriter? Write instance methods that write() can call to do the necessary
        # TODO: output format.
        PROJECT_ROOT = pathlib.Path(__file__).parent.absolute()

        result = data
        if(format == 'display'):
            for neo in result:
                stri = neo.__str__()
                stri = stri.replace("=>","\n").replace(" / "," ")
                stri = stri.replace(", ","\n")
                print(stri+"\n")
            return 1

        elif(format == 'csv_file'):
            neo_result_list=[['id','name','orbits','orbit dates']]
            for neo in result:
                stri = neo.__str__()
                stri = stri.replace("=>",":").split(':')
                neo_result_list.append(stri[1::2])

            column_names = neo_result_list.pop(0)
            df = pd.DataFrame(neo_result_list,columns=column_names)
            df.to_csv(f'{PROJECT_ROOT}/data/result.csv')
            return 1
