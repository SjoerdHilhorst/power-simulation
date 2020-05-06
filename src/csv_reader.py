from os.path import normpath, join, dirname

import pandas as pd

"""
This class is responsible for manipulations of csv files. It contains lists of historic data for all fields specified
in env.
"""


class CSVReader:
    def __init__(self, from_csv):
        lists = [None]
        fields = [None]
        for field in from_csv:
            # open csv corresponding to the field which should be taken from the csv
            csv_file = self.open_csv(from_csv[field])
            # create a list containing the column of the field
            field_list = csv_file[field].tolist()[0:]
            # append the list to all others
            lists.append(field_list)
            # append the field name
            fields.append(field)
        # zip a dictionary with pairs (field_name: list)
        self.lists = dict(zip(fields, lists))

    def open_csv(self, csv_name):
        """
        Opens csv from the folder csvs
        :param csv_name: name of the csv file
        :return: csv file
        """
        dirpath = normpath(join(dirname(__file__), "../csvs"))
        csv_name = csv_name + ".csv"
        filepath = join(dirpath, csv_name)
        try:
            file = pd.read_csv(filepath)
            return file
        except FileNotFoundError:
            print("FileNotFoundError: file %s not found in %s" % (csv_name, dirpath))
            exit(1)

    def get_from_csv(self, field):
        """
        Gets next value from csv file. Since the class keeps track of all lists, 0th element is always popped.
        :param field: name of field to be retrieved
        :return: next value from csv file
        """
        if len(self.lists[field]) > 0:
            return self.lists[field].pop(0)
        else:
            print("End of file for %s" % field)
            exit(1)