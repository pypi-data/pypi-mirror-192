"""
Indicates employment-related experience requirements, e.g. [[monthsOfExperience]].

https://schema.org/OccupationalExperienceRequirements
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class OccupationalExperienceRequirementsInheritedProperties(TypedDict):
    """Indicates employment-related experience requirements, e.g. [[monthsOfExperience]].

    References:
        https://schema.org/OccupationalExperienceRequirements
    Note:
        Model Depth 3
    Attributes:
    """

    


class OccupationalExperienceRequirementsProperties(TypedDict):
    """Indicates employment-related experience requirements, e.g. [[monthsOfExperience]].

    References:
        https://schema.org/OccupationalExperienceRequirements
    Note:
        Model Depth 3
    Attributes:
        monthsOfExperience: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): Indicates the minimal number of months of experience required for a position.
    """

    monthsOfExperience: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    

#OccupationalExperienceRequirementsInheritedPropertiesTd = OccupationalExperienceRequirementsInheritedProperties()
#OccupationalExperienceRequirementsPropertiesTd = OccupationalExperienceRequirementsProperties()


class AllProperties(OccupationalExperienceRequirementsInheritedProperties , OccupationalExperienceRequirementsProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[OccupationalExperienceRequirementsProperties, OccupationalExperienceRequirementsInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "OccupationalExperienceRequirements"
    return model
    

OccupationalExperienceRequirements = create_schema_org_model()