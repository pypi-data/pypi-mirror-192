# isinstancex (version: 2.0.0)
#
# Copyright 2023. DuelitDev all rights reserved.
#
# This Library is distributed under the MIT License.


from isinstancex._version import python_version


requires = 3.8
if python_version >= requires:
    del python_version
    from isinstancex.isinstancex import *
else:
    raise OSError(f"Python version must be higher or equal to {requires}.")
