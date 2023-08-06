"""
DisabilitySupport: this is a benefit for disability support.

https://schema.org/DisabilitySupport
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DisabilitySupportInheritedProperties(TypedDict):
    """DisabilitySupport: this is a benefit for disability support.

    References:
        https://schema.org/DisabilitySupport
    Note:
        Model Depth 5
    Attributes:
    """

    


class DisabilitySupportProperties(TypedDict):
    """DisabilitySupport: this is a benefit for disability support.

    References:
        https://schema.org/DisabilitySupport
    Note:
        Model Depth 5
    Attributes:
    """

    

#DisabilitySupportInheritedPropertiesTd = DisabilitySupportInheritedProperties()
#DisabilitySupportPropertiesTd = DisabilitySupportProperties()


class AllProperties(DisabilitySupportInheritedProperties , DisabilitySupportProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DisabilitySupportProperties, DisabilitySupportInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DisabilitySupport"
    return model
    

DisabilitySupport = create_schema_org_model()