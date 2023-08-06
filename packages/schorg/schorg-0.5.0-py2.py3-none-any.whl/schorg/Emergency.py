"""
A specific branch of medical science that deals with the evaluation and initial treatment of medical conditions caused by trauma or sudden illness.

https://schema.org/Emergency
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class EmergencyInheritedProperties(TypedDict):
    """A specific branch of medical science that deals with the evaluation and initial treatment of medical conditions caused by trauma or sudden illness.

    References:
        https://schema.org/Emergency
    Note:
        Model Depth 5
    Attributes:
    """

    


class EmergencyProperties(TypedDict):
    """A specific branch of medical science that deals with the evaluation and initial treatment of medical conditions caused by trauma or sudden illness.

    References:
        https://schema.org/Emergency
    Note:
        Model Depth 5
    Attributes:
    """

    

#EmergencyInheritedPropertiesTd = EmergencyInheritedProperties()
#EmergencyPropertiesTd = EmergencyProperties()


class AllProperties(EmergencyInheritedProperties , EmergencyProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[EmergencyProperties, EmergencyInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Emergency"
    return model
    

Emergency = create_schema_org_model()