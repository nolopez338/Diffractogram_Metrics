"""
Program: pread_file.py
Project: Reads sample from csv format
Author: Nicolas Lopez
"""

# ==================================================
# Basic Libraries
# ==================================================


from preprocessing.read_file import DiffractogramRead


dr = DiffractogramRead()

dr.add_all_data_sources()
