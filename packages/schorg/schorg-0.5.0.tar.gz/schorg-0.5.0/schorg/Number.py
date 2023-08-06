"""
Data type: Number.Usage guidelines:* Use values from 0123456789 (Unicode 'DIGIT ZERO' (U+0030) to 'DIGIT NINE' (U+0039)) rather than superficially similar Unicode symbols.* Use '.' (Unicode 'FULL STOP' (U+002E)) rather than ',' to indicate a decimal point. Avoid using these symbols as a readability separator.

https://schema.org/Number
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class NumberInheritedProperties(TypedDict):
    """Data type: Number.Usage guidelines:* Use values from 0123456789 (Unicode 'DIGIT ZERO' (U+0030) to 'DIGIT NINE' (U+0039)) rather than superficially similar Unicode symbols.* Use '.' (Unicode 'FULL STOP' (U+002E)) rather than ',' to indicate a decimal point. Avoid using these symbols as a readability separator.

    References:
        https://schema.org/Number
    Note:
        Model Depth 5
    Attributes:
    """

    


class NumberProperties(TypedDict):
    """Data type: Number.Usage guidelines:* Use values from 0123456789 (Unicode 'DIGIT ZERO' (U+0030) to 'DIGIT NINE' (U+0039)) rather than superficially similar Unicode symbols.* Use '.' (Unicode 'FULL STOP' (U+002E)) rather than ',' to indicate a decimal point. Avoid using these symbols as a readability separator.

    References:
        https://schema.org/Number
    Note:
        Model Depth 5
    Attributes:
    """

    

#NumberInheritedPropertiesTd = NumberInheritedProperties()
#NumberPropertiesTd = NumberProperties()


class AllProperties(NumberInheritedProperties , NumberProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[NumberProperties, NumberInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Number"
    return model
    

Number = create_schema_org_model()