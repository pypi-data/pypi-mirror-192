"""
A word, name, acronym, phrase, etc. with a formal definition. Often used in the context of category or subject classification, glossaries or dictionaries, product or creative work types, etc. Use the name property for the term being defined, use termCode if the term has an alpha-numeric code allocated, use description to provide the definition of the term.

https://schema.org/DefinedTerm
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DefinedTermInheritedProperties(TypedDict):
    """A word, name, acronym, phrase, etc. with a formal definition. Often used in the context of category or subject classification, glossaries or dictionaries, product or creative work types, etc. Use the name property for the term being defined, use termCode if the term has an alpha-numeric code allocated, use description to provide the definition of the term.

    References:
        https://schema.org/DefinedTerm
    Note:
        Model Depth 3
    Attributes:
    """

    


class DefinedTermProperties(TypedDict):
    """A word, name, acronym, phrase, etc. with a formal definition. Often used in the context of category or subject classification, glossaries or dictionaries, product or creative work types, etc. Use the name property for the term being defined, use termCode if the term has an alpha-numeric code allocated, use description to provide the definition of the term.

    References:
        https://schema.org/DefinedTerm
    Note:
        Model Depth 3
    Attributes:
        inDefinedTermSet: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): A [[DefinedTermSet]] that contains this term.
        termCode: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): A code that identifies this [[DefinedTerm]] within a [[DefinedTermSet]]
    """

    inDefinedTermSet: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    termCode: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    

#DefinedTermInheritedPropertiesTd = DefinedTermInheritedProperties()
#DefinedTermPropertiesTd = DefinedTermProperties()


class AllProperties(DefinedTermInheritedProperties , DefinedTermProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DefinedTermProperties, DefinedTermInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DefinedTerm"
    return model
    

DefinedTerm = create_schema_org_model()