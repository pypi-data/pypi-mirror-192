"""
A stage of a medical condition, such as 'Stage IIIa'.

https://schema.org/MedicalConditionStage
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MedicalConditionStageInheritedProperties(TypedDict):
    """A stage of a medical condition, such as 'Stage IIIa'.

    References:
        https://schema.org/MedicalConditionStage
    Note:
        Model Depth 4
    Attributes:
    """

    


class MedicalConditionStageProperties(TypedDict):
    """A stage of a medical condition, such as 'Stage IIIa'.

    References:
        https://schema.org/MedicalConditionStage
    Note:
        Model Depth 4
    Attributes:
        subStageSuffix: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The substage, e.g. 'a' for Stage IIIa.
        stageAsNumber: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): The stage represented as a number, e.g. 3.
    """

    subStageSuffix: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    stageAsNumber: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    

#MedicalConditionStageInheritedPropertiesTd = MedicalConditionStageInheritedProperties()
#MedicalConditionStagePropertiesTd = MedicalConditionStageProperties()


class AllProperties(MedicalConditionStageInheritedProperties , MedicalConditionStageProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MedicalConditionStageProperties, MedicalConditionStageInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MedicalConditionStage"
    return model
    

MedicalConditionStage = create_schema_org_model()