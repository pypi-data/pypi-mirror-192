"""
A specific branch of medical science that specializes in the care of women during the prenatal and postnatal care and with the delivery of the child.

https://schema.org/Obstetric
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ObstetricInheritedProperties(TypedDict):
    """A specific branch of medical science that specializes in the care of women during the prenatal and postnatal care and with the delivery of the child.

    References:
        https://schema.org/Obstetric
    Note:
        Model Depth 5
    Attributes:
    """

    


class ObstetricProperties(TypedDict):
    """A specific branch of medical science that specializes in the care of women during the prenatal and postnatal care and with the delivery of the child.

    References:
        https://schema.org/Obstetric
    Note:
        Model Depth 5
    Attributes:
    """

    

#ObstetricInheritedPropertiesTd = ObstetricInheritedProperties()
#ObstetricPropertiesTd = ObstetricProperties()


class AllProperties(ObstetricInheritedProperties , ObstetricProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ObstetricProperties, ObstetricInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Obstetric"
    return model
    

Obstetric = create_schema_org_model()