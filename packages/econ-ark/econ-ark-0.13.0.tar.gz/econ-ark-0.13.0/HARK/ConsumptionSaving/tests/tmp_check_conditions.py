import unittest
from copy import copy, deepcopy

import numpy as np

from HARK.ConsumptionSaving.ConsIndShockModel import (
    ConsIndShockSolverBasic,
    IndShockConsumerType,
    init_idiosyncratic_shocks,
    init_lifecycle,
)
from HARK.tests import HARK_PRECISION


agent = IndShockConsumerType(AgentCount=2, T_sim=10)

agent.check_conditions()
