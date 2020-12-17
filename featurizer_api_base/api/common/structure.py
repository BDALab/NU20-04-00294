import os


# ##################### #
# Possible improvements #
# ##################### #
#
# Improvements:
#
#  1. read the paths from a configuration file
#  2. build the configuration file automatically
#
# State:
#
# @zgalaz (main developer): so far, the current state is suitable

# Prepare the base paths
THIS_PATH = os.path.realpath(__file__)
BASE_PATH = os.path.dirname(THIS_PATH)

# Prepare the specific paths:
#
#  1. configuration
#  2. dsp
#  3. resources
#  4. logging

# Prepare the configuration path
configuration_path = os.path.join(BASE_PATH, "..", "configuration", "configurations")

# Prepare the dsp folder path
dsp_path = os.path.join(BASE_PATH, "..", "dsp")

# Prepare the resources path
resources_path = os.path.join(BASE_PATH, "..", "resources")

# Prepare the logging path
logging_path = os.path.join(BASE_PATH, "..", "logs")
