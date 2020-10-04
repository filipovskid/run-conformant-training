from drboson.drboson import DRBoson
import pathlib

from example import train_example


def run(drboson=DRBoson(), dataset_location=None):
    train_example(drboson, dataset_location=dataset_location)
