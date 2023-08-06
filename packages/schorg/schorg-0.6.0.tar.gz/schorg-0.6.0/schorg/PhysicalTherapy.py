"""
A process of progressive physical care and rehabilitation aimed at improving a health condition.

https://schema.org/PhysicalTherapy
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PhysicalTherapyInheritedProperties(TypedDict):
    """A process of progressive physical care and rehabilitation aimed at improving a health condition.

    References:
        https://schema.org/PhysicalTherapy
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
    


class PhysicalTherapyProperties(TypedDict):
    """A process of progressive physical care and rehabilitation aimed at improving a health condition.

    References:
        https://schema.org/PhysicalTherapy
    Note:
        Model Depth 6
    Attributes:
    """

    

#PhysicalTherapyInheritedPropertiesTd = PhysicalTherapyInheritedProperties()
#PhysicalTherapyPropertiesTd = PhysicalTherapyProperties()


class AllProperties(PhysicalTherapyInheritedProperties , PhysicalTherapyProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PhysicalTherapyProperties, PhysicalTherapyInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "PhysicalTherapy"
    return model
    

PhysicalTherapy = create_schema_org_model()