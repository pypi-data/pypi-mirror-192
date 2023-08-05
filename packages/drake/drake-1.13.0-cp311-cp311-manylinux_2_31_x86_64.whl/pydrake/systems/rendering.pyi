import pydrake.multibody.plant
import pydrake.systems.framework

class MultibodyPositionToGeometryPose(pydrake.systems.framework.LeafSystem_𝓣float𝓤):
    def __init__(self, plant: pydrake.multibody.plant.MultibodyPlant_𝓣float𝓤, input_multibody_state: bool = ...) -> None: ...
