from drboson.drboson import DRBoson
import pathlib

from example import train_example


def run(drboson=DRBoson(), dataset_location=None):
    data_dir = pathlib.Path('./data')
    train_example(drboson, data_dir=data_dir)

run()
