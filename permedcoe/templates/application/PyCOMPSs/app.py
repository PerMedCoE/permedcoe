#!/usr/bin/python3

# To set building block debug mode
from permedcoe import set_debug
# Import building block entry points
from BUILDINGBLOCK import invoke
from BUILDINGBLOCK import personalize_model


# TODO: Import the desired building blocks and use invoke or any other function.

def main():
    # SAMPLE:
    set_debug(False)
    print("Sample python application using sample BB")
    conf = {"suffix": "META_mutations_CNA_asMutant",
            "model": "Fumia2013"}
    invoke("/path/to/dataset",
           "output",
           conf)
    # personalize_model(...)


if __name__ == "__main__":
    main()
