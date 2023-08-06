"""
A treatment of people with physical, emotional, or social problems, using purposeful activity to help them overcome or learn to deal with their problems.

https://schema.org/OccupationalTherapy
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class OccupationalTherapyInheritedProperties(TypedDict):
    """A treatment of people with physical, emotional, or social problems, using purposeful activity to help them overcome or learn to deal with their problems.

    References:
        https://schema.org/OccupationalTherapy
    Note:
        Model Depth 6
    Attributes:
        seriousAdverseOutcome: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A possible serious complication and/or serious side effect of this therapy. Serious adverse outcomes include those that are life-threatening; result in death, disability, or permanent damage; require hospitalization or prolong existing hospitalization; cause congenital anomalies or birth defects; or jeopardize the patient and may require medical or surgical intervention to prevent one of the outcomes in this definition.
        duplicateTherapy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A therapy that duplicates or overlaps this one.
        contraindication: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): A contraindication for this therapy.
    """

    seriousAdverseOutcome: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    duplicateTherapy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    contraindication: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    


class OccupationalTherapyProperties(TypedDict):
    """A treatment of people with physical, emotional, or social problems, using purposeful activity to help them overcome or learn to deal with their problems.

    References:
        https://schema.org/OccupationalTherapy
    Note:
        Model Depth 6
    Attributes:
    """

    

#OccupationalTherapyInheritedPropertiesTd = OccupationalTherapyInheritedProperties()
#OccupationalTherapyPropertiesTd = OccupationalTherapyProperties()


class AllProperties(OccupationalTherapyInheritedProperties , OccupationalTherapyProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[OccupationalTherapyProperties, OccupationalTherapyInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "OccupationalTherapy"
    return model
    

OccupationalTherapy = create_schema_org_model()