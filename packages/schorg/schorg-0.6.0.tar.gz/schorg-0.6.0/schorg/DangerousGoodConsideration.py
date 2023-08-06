"""
The item is dangerous and requires careful handling and/or special training of the user. See also the [UN Model Classification](https://unece.org/DAM/trans/danger/publi/unrec/rev17/English/02EREv17_Part2.pdf) defining the 9 classes of dangerous goods such as explosives, gases, flammables, and more.

https://schema.org/DangerousGoodConsideration
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DangerousGoodConsiderationInheritedProperties(TypedDict):
    """The item is dangerous and requires careful handling and/or special training of the user. See also the [UN Model Classification](https://unece.org/DAM/trans/danger/publi/unrec/rev17/English/02EREv17_Part2.pdf) defining the 9 classes of dangerous goods such as explosives, gases, flammables, and more.

    References:
        https://schema.org/DangerousGoodConsideration
    Note:
        Model Depth 5
    Attributes:
    """

    


class DangerousGoodConsiderationProperties(TypedDict):
    """The item is dangerous and requires careful handling and/or special training of the user. See also the [UN Model Classification](https://unece.org/DAM/trans/danger/publi/unrec/rev17/English/02EREv17_Part2.pdf) defining the 9 classes of dangerous goods such as explosives, gases, flammables, and more.

    References:
        https://schema.org/DangerousGoodConsideration
    Note:
        Model Depth 5
    Attributes:
    """

    

#DangerousGoodConsiderationInheritedPropertiesTd = DangerousGoodConsiderationInheritedProperties()
#DangerousGoodConsiderationPropertiesTd = DangerousGoodConsiderationProperties()


class AllProperties(DangerousGoodConsiderationInheritedProperties , DangerousGoodConsiderationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DangerousGoodConsiderationProperties, DangerousGoodConsiderationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DangerousGoodConsideration"
    return model
    

DangerousGoodConsideration = create_schema_org_model()