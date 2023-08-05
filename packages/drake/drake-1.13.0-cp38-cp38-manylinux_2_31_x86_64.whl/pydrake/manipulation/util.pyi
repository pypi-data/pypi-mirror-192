from typing import ClassVar, Dict

import pydrake.multibody.parsing
import pydrake.multibody.plant
import pydrake.systems.framework
import pydrake.systems.lcm

class ZeroForceDriver:
    __fields__: ClassVar[tuple] = ...  # read-only
    def __init__(self, **kwargs) -> None: ...
    def __copy__(self) -> ZeroForceDriver: ...
    def __deepcopy__(self, arg0: dict) -> ZeroForceDriver: ...

def ApplyDriverConfig(driver_config: ZeroForceDriver, model_instance_name: str, sim_plant: pydrake.multibody.plant.MultibodyPlant_𝓣float𝓤, models_from_directives: Dict[str,pydrake.multibody.parsing.ModelInstanceInfo], lcms: pydrake.systems.lcm.LcmBuses, builder: pydrake.systems.framework.DiagramBuilder_𝓣float𝓤) -> None: ...
