"""
All the documents published by an official publisher should have at least the legal value level "OfficialLegalValue". This indicates that the document was published by an organisation with the public task of making it available (e.g. a consolidated version of an EU directive published by the EU Office of Publications).

https://schema.org/OfficialLegalValue
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class OfficialLegalValueInheritedProperties(TypedDict):
    """All the documents published by an official publisher should have at least the legal value level "OfficialLegalValue". This indicates that the document was published by an organisation with the public task of making it available (e.g. a consolidated version of an EU directive published by the EU Office of Publications).

    References:
        https://schema.org/OfficialLegalValue
    Note:
        Model Depth 5
    Attributes:
    """

    


class OfficialLegalValueProperties(TypedDict):
    """All the documents published by an official publisher should have at least the legal value level "OfficialLegalValue". This indicates that the document was published by an organisation with the public task of making it available (e.g. a consolidated version of an EU directive published by the EU Office of Publications).

    References:
        https://schema.org/OfficialLegalValue
    Note:
        Model Depth 5
    Attributes:
    """

    

#OfficialLegalValueInheritedPropertiesTd = OfficialLegalValueInheritedProperties()
#OfficialLegalValuePropertiesTd = OfficialLegalValueProperties()


class AllProperties(OfficialLegalValueInheritedProperties , OfficialLegalValueProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[OfficialLegalValueProperties, OfficialLegalValueInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "OfficialLegalValue"
    return model
    

OfficialLegalValue = create_schema_org_model()