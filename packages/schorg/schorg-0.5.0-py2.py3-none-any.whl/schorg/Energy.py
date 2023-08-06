"""
Properties that take Energy as values are of the form '&lt;Number&gt; &lt;Energy unit of measure&gt;'.

https://schema.org/Energy
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class EnergyInheritedProperties(TypedDict):
    """Properties that take Energy as values are of the form '&lt;Number&gt; &lt;Energy unit of measure&gt;'.

    References:
        https://schema.org/Energy
    Note:
        Model Depth 4
    Attributes:
    """

    


class EnergyProperties(TypedDict):
    """Properties that take Energy as values are of the form '&lt;Number&gt; &lt;Energy unit of measure&gt;'.

    References:
        https://schema.org/Energy
    Note:
        Model Depth 4
    Attributes:
    """

    

#EnergyInheritedPropertiesTd = EnergyInheritedProperties()
#EnergyPropertiesTd = EnergyProperties()


class AllProperties(EnergyInheritedProperties , EnergyProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[EnergyProperties, EnergyInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Energy"
    return model
    

Energy = create_schema_org_model()