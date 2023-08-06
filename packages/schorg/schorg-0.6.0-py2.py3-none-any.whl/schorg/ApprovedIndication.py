"""
An indication for a medical therapy that has been formally specified or approved by a regulatory body that regulates use of the therapy; for example, the US FDA approves indications for most drugs in the US.

https://schema.org/ApprovedIndication
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ApprovedIndicationInheritedProperties(TypedDict):
    """An indication for a medical therapy that has been formally specified or approved by a regulatory body that regulates use of the therapy; for example, the US FDA approves indications for most drugs in the US.

    References:
        https://schema.org/ApprovedIndication
    Note:
        Model Depth 4
    Attributes:
    """

    


class ApprovedIndicationProperties(TypedDict):
    """An indication for a medical therapy that has been formally specified or approved by a regulatory body that regulates use of the therapy; for example, the US FDA approves indications for most drugs in the US.

    References:
        https://schema.org/ApprovedIndication
    Note:
        Model Depth 4
    Attributes:
    """

    

#ApprovedIndicationInheritedPropertiesTd = ApprovedIndicationInheritedProperties()
#ApprovedIndicationPropertiesTd = ApprovedIndicationProperties()


class AllProperties(ApprovedIndicationInheritedProperties , ApprovedIndicationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ApprovedIndicationProperties, ApprovedIndicationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ApprovedIndication"
    return model
    

ApprovedIndication = create_schema_org_model()