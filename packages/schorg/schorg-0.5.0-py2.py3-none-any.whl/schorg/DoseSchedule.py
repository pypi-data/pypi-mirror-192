"""
A specific dosing schedule for a drug or supplement.

https://schema.org/DoseSchedule
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DoseScheduleInheritedProperties(TypedDict):
    """A specific dosing schedule for a drug or supplement.

    References:
        https://schema.org/DoseSchedule
    Note:
        Model Depth 4
    Attributes:
    """

    


class DoseScheduleProperties(TypedDict):
    """A specific dosing schedule for a drug or supplement.

    References:
        https://schema.org/DoseSchedule
    Note:
        Model Depth 4
    Attributes:
        targetPopulation: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): Characteristics of the population for which this is intended, or which typically uses it, e.g. 'adults'.
        doseValue: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): The value of the dose, e.g. 500.
        doseUnit: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The unit of the dose, e.g. 'mg'.
        frequency: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): How often the dose is taken, e.g. 'daily'.
    """

    targetPopulation: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    doseValue: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    doseUnit: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    frequency: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    

#DoseScheduleInheritedPropertiesTd = DoseScheduleInheritedProperties()
#DoseSchedulePropertiesTd = DoseScheduleProperties()


class AllProperties(DoseScheduleInheritedProperties , DoseScheduleProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DoseScheduleProperties, DoseScheduleInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DoseSchedule"
    return model
    

DoseSchedule = create_schema_org_model()