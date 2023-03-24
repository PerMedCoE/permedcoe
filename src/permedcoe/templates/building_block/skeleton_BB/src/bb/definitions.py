import os
from permedcoe.bb import CONTAINER_PATH
from permedcoe.bb import COMPUTING_UNITS

# Do not change this line
BB_SOURCE_PATH=os.path.dirname(os.path.abspath(__file__))

# Update the following lines:
#  - Assets folder within the NEW_NAME Building Block
NEW_NAME_ASSETS_PATH = os.path.join(BB_SOURCE_PATH, "assets")
#  - Container definition for NEW_NAME Building Block
CONTAINER = "NEW_NAME.sif"  # TODO: Define your container.
NEW_NAME_CONTAINER = os.path.join(CONTAINER_PATH, CONTAINER)
