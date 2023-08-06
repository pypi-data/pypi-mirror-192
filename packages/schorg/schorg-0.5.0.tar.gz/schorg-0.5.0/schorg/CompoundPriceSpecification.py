"""
A compound price specification is one that bundles multiple prices that all apply in combination for different dimensions of consumption. Use the name property of the attached unit price specification for indicating the dimension of a price component (e.g. "electricity" or "final cleaning").

https://schema.org/CompoundPriceSpecification
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class CompoundPriceSpecificationInheritedProperties(TypedDict):
    """A compound price specification is one that bundles multiple prices that all apply in combination for different dimensions of consumption. Use the name property of the attached unit price specification for indicating the dimension of a price component (e.g. "electricity" or "final cleaning").

    References:
        https://schema.org/CompoundPriceSpecification
    Note:
        Model Depth 5
    Attributes:
        eligibleQuantity: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The interval and unit of measurement of ordering quantities for which the offer or price specification is valid. This allows e.g. specifying that a certain freight charge is valid only for a certain quantity.
        valueAddedTaxIncluded: (Optional[Union[List[Union[StrictBool, SchemaOrgObj, str]], StrictBool, SchemaOrgObj, str]]): Specifies whether the applicable value-added tax (VAT) is included in the price specification or not.
        minPrice: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): The lowest price if the price is a range.
        price: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): The offer price of a product, or of a price component when attached to PriceSpecification and its subtypes.Usage guidelines:* Use the [[priceCurrency]] property (with standard formats: [ISO 4217 currency format](http://en.wikipedia.org/wiki/ISO_4217), e.g. "USD"; [Ticker symbol](https://en.wikipedia.org/wiki/List_of_cryptocurrencies) for cryptocurrencies, e.g. "BTC"; well known names for [Local Exchange Trading Systems](https://en.wikipedia.org/wiki/Local_exchange_trading_system) (LETS) and other currency types, e.g. "Ithaca HOUR") instead of including [ambiguous symbols](http://en.wikipedia.org/wiki/Dollar_sign#Currencies_that_use_the_dollar_or_peso_sign) such as '$' in the value.* Use '.' (Unicode 'FULL STOP' (U+002E)) rather than ',' to indicate a decimal point. Avoid using these symbols as a readability separator.* Note that both [RDFa](http://www.w3.org/TR/xhtml-rdfa-primer/#using-the-content-attribute) and Microdata syntax allow the use of a "content=" attribute for publishing simple machine-readable values alongside more human-friendly formatting.* Use values from 0123456789 (Unicode 'DIGIT ZERO' (U+0030) to 'DIGIT NINE' (U+0039)) rather than superficially similar Unicode symbols.      
        validThrough: (Optional[Union[List[Union[datetime, SchemaOrgObj, str, date]], datetime, SchemaOrgObj, str, date]]): The date after when the item is not valid. For example the end of an offer, salary period, or a period of opening hours.
        maxPrice: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): The highest price if the price is a range.
        validFrom: (Optional[Union[List[Union[datetime, SchemaOrgObj, str, date]], datetime, SchemaOrgObj, str, date]]): The date when the item becomes valid.
        eligibleTransactionVolume: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The transaction volume, in a monetary unit, for which the offer or price specification is valid, e.g. for indicating a minimal purchasing volume, to express free shipping above a certain order volume, or to limit the acceptance of credit cards to purchases to a certain minimal amount.
        priceCurrency: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The currency of the price, or a price component when attached to [[PriceSpecification]] and its subtypes.Use standard formats: [ISO 4217 currency format](http://en.wikipedia.org/wiki/ISO_4217), e.g. "USD"; [Ticker symbol](https://en.wikipedia.org/wiki/List_of_cryptocurrencies) for cryptocurrencies, e.g. "BTC"; well known names for [Local Exchange Trading Systems](https://en.wikipedia.org/wiki/Local_exchange_trading_system) (LETS) and other currency types, e.g. "Ithaca HOUR".
    """

    eligibleQuantity: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    valueAddedTaxIncluded: NotRequired[Union[List[Union[StrictBool, SchemaOrgObj, str]], StrictBool, SchemaOrgObj, str]]
    minPrice: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    price: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    validThrough: NotRequired[Union[List[Union[datetime, SchemaOrgObj, str, date]], datetime, SchemaOrgObj, str, date]]
    maxPrice: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    validFrom: NotRequired[Union[List[Union[datetime, SchemaOrgObj, str, date]], datetime, SchemaOrgObj, str, date]]
    eligibleTransactionVolume: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    priceCurrency: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    


class CompoundPriceSpecificationProperties(TypedDict):
    """A compound price specification is one that bundles multiple prices that all apply in combination for different dimensions of consumption. Use the name property of the attached unit price specification for indicating the dimension of a price component (e.g. "electricity" or "final cleaning").

    References:
        https://schema.org/CompoundPriceSpecification
    Note:
        Model Depth 5
    Attributes:
        priceType: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): Defines the type of a price specified for an offered product, for example a list price, a (temporary) sale price or a manufacturer suggested retail price. If multiple prices are specified for an offer the [[priceType]] property can be used to identify the type of each such specified price. The value of priceType can be specified as a value from enumeration PriceTypeEnumeration or as a free form text string for price types that are not already predefined in PriceTypeEnumeration.
        priceComponent: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): This property links to all [[UnitPriceSpecification]] nodes that apply in parallel for the [[CompoundPriceSpecification]] node.
    """

    priceType: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    priceComponent: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#CompoundPriceSpecificationInheritedPropertiesTd = CompoundPriceSpecificationInheritedProperties()
#CompoundPriceSpecificationPropertiesTd = CompoundPriceSpecificationProperties()


class AllProperties(CompoundPriceSpecificationInheritedProperties , CompoundPriceSpecificationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[CompoundPriceSpecificationProperties, CompoundPriceSpecificationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "CompoundPriceSpecification"
    return model
    

CompoundPriceSpecification = create_schema_org_model()