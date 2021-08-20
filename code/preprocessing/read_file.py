"""
Program: pread_file.py
Project: Reads sample from csv format
Author: Nicolas Lopez
"""

# ==================================================
# Basic Libraries
# ==================================================

import os
import pandas as pd


# ==================================================
# Main Class
# ==================================================

class DiffractogramRead:
    """
    Reads diffractogram data from 'path_file' or in the cwd by default
    It reads directly inside this path or inside a 'data' subfolder
    """

    def __init__(self, path_files=None, data_list=[]):
        # Attributes
        self.data_list = data_list
        self.path_files = None
        self.data_sources = None

        self.__read_functions = {}
        self.__sample_columns = ['Angle', 'Intensity']

        # Initialize
        self.set_path_files(path_files)
        self.__set_data_sources_information()


    def set_path_files(self, path_files=None, data_folder=True):
        """
        :param path_files: Path where data files/folders are located
        :param data_folder: True if data is inside a "data" folder
        Changes self.path_files
        """

        self.path_files = os.getcwd() if path_files is None else path_files

        if data_folder and 'data' in os.listdir(self.path_files):
            self.path_files += '/data'


    def add_all_data_sources(self):
        for source in self.data_sources:
            self.add_data_source_to_data_list(source)


    def add_data_source_to_data_list(self, data_source):

        new_path = f"{self.path_files}/{data_source}"

        try:
            read_fun = self.__read_functions[data_source]
        except Exception:
            print(f"No existe una función registrada para leer los archivos en {data_source}")
            return

        for file in os.listdir(new_path):
            sample = {'title': file,
                      'class': file.split('_')[0],
                      'data': read_fun(f"{data_source}/{file}")}

            self.data_list.append(sample)


    def number_files_in_data_sources(self):
        for source in self.data_sources:
            n_tot = os.listdir(f"{self.path_files}/{source}")
            n_csv = [it for it in n_tot if '.csv' in it]
            print(f"{source}: {len(n_csv)}/{len(n_tot)}")


    def __set_data_sources_information(self):
        """
        Manually select read function for each data source
        """
        self.data_sources = os.listdir(self.path_files)

        try:
            self.__read_functions[self.data_sources[0]] = self.__read_csv1
            self.__read_functions[self.data_sources[1]] = self.__read_csv2
        except Exception:
            print("No se pudieron relacionar los recursos de datos con las funciones de lectura")


    def __read_csv1(self, file):
        sample = pd.read_csv(f"{self.path_files}/{file}")
        sample.columns = self.__sample_columns
        return sample


    def __read_csv2(self, file):
        sample = pd.read_csv(f"{self.path_files}/{file}", names=self.__sample_columns)

        # Selects index for new data Frame
        start_index = list(sample.loc[sample['Angle'] == 'Angle'].index)[0] + 1

        sample = sample.iloc[start_index:, :]
        sample = sample.astype('float')
        return sample




