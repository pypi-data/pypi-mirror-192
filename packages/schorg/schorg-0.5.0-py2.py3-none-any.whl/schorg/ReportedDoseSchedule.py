"""
A patient-reported or observed dosing schedule for a drug or supplement.

https://schema.org/ReportedDoseSchedule
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ReportedDoseScheduleInheritedProperties(TypedDict):
    """A patient-reported or observed dosing schedule for a drug or supplement.

    References:
        https://schema.org/ReportedDoseSchedule
    Note:
        Model Depth 5
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
    


class ReportedDoseScheduleProperties(TypedDict):
    """A patient-reported or observed dosing schedule for a drug or supplement.

    References:
        https://schema.org/ReportedDoseSchedule
    Note:
        Model Depth 5
    Attributes:
    """

    

#ReportedDoseScheduleInheritedPropertiesTd = ReportedDoseScheduleInheritedProperties()
#ReportedDoseSchedulePropertiesTd = ReportedDoseScheduleProperties()


class AllProperties(ReportedDoseScheduleInheritedProperties , ReportedDoseScheduleProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ReportedDoseScheduleProperties, ReportedDoseScheduleInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ReportedDoseSchedule"
    return model
    

ReportedDoseSchedule = create_schema_org_model()