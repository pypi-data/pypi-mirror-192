"""
Properties that take Mass as values are of the form '&lt;Number&gt; &lt;Mass unit of measure&gt;'. E.g., '7 kg'.

https://schema.org/Mass
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MassInheritedProperties(TypedDict):
    """Properties that take Mass as values are of the form '&lt;Number&gt; &lt;Mass unit of measure&gt;'. E.g., '7 kg'.

    References:
        https://schema.org/Mass
    Note:
        Model Depth 4
    Attributes:
    """

    


class MassProperties(TypedDict):
    """Properties that take Mass as values are of the form '&lt;Number&gt; &lt;Mass unit of measure&gt;'. E.g., '7 kg'.

    References:
        https://schema.org/Mass
    Note:
        Model Depth 4
    Attributes:
    """

    

#MassInheritedPropertiesTd = MassInheritedProperties()
#MassPropertiesTd = MassProperties()


class AllProperties(MassInheritedProperties , MassProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MassProperties, MassInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Mass"
    return model
    

Mass = create_schema_org_model()