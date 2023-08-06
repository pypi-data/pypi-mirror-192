"""
A set of organisms asserted to represent a natural cohesive biological unit.

https://schema.org/Taxon
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class TaxonInheritedProperties(TypedDict):
    """A set of organisms asserted to represent a natural cohesive biological unit.

    References:
        https://schema.org/Taxon
    Note:
        Model Depth 2
    Attributes:
        potentialAction: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Indicates a potential Action, which describes an idealized action in which this thing would play an 'object' role.
        mainEntityOfPage: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): Indicates a page (or other CreativeWork) for which this thing is the main entity being described. See [background notes](/docs/datamodel.html#mainEntityBackground) for details.
        subjectOf: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A CreativeWork or Event about this Thing.
        url: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): URL of the item.
        alternateName: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): An alias for the item.
        sameAs: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): URL of a reference Web page that unambiguously indicates the item's identity. E.g. the URL of the item's Wikipedia page, Wikidata entry, or official website.
        description: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): A description of the item.
        disambiguatingDescription: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): A sub property of description. A short description of the item used to disambiguate from other, similar items. Information from other properties (in particular, name) may be necessary for the description to be useful for disambiguation.
        identifier: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): The identifier property represents any kind of identifier for any kind of [[Thing]], such as ISBNs, GTIN codes, UUIDs etc. Schema.org provides dedicated properties for representing many of these, either as textual strings or as URL (URI) links. See [background notes](/docs/datamodel.html#identifierBg) for more details.        
        image: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): An image of the item. This can be a [[URL]] or a fully described [[ImageObject]].
        name: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The name of the item.
        additionalType: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): An additional type for the item, typically used for adding more specific types from external vocabularies in microdata syntax. This is a relationship between something and a class that the thing is in. In RDFa syntax, it is better to use the native RDFa syntax - the 'typeof' attribute - for multiple types. Schema.org tools may have only weaker understanding of extra types, in particular those defined externally.
    """

    potentialAction: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    mainEntityOfPage: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    subjectOf: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    url: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    alternateName: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    sameAs: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    description: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    disambiguatingDescription: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    identifier: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    image: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    name: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    additionalType: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    


class TaxonProperties(TypedDict):
    """A set of organisms asserted to represent a natural cohesive biological unit.

    References:
        https://schema.org/Taxon
    Note:
        Model Depth 2
    Attributes:
        parentTaxon: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): Closest parent taxon of the taxon in question.
        taxonRank: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): The taxonomic rank of this taxon given preferably as a URI from a controlled vocabulary – typically the ranks from TDWG TaxonRank ontology or equivalent Wikidata URIs.
        childTaxon: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): Closest child taxa of the taxon in question.
        hasDefinedTerm: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A Defined Term contained in this term set.
    """

    parentTaxon: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    taxonRank: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    childTaxon: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    hasDefinedTerm: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#TaxonInheritedPropertiesTd = TaxonInheritedProperties()
#TaxonPropertiesTd = TaxonProperties()


class AllProperties(TaxonInheritedProperties , TaxonProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[TaxonProperties, TaxonInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Taxon"
    return model
    

Taxon = create_schema_org_model()