"""
An [[Article]] that an external entity has paid to place or to produce to its specifications. Includes [advertorials](https://en.wikipedia.org/wiki/Advertorial), sponsored content, native advertising and other paid content.

https://schema.org/AdvertiserContentArticle
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class AdvertiserContentArticleInheritedProperties(TypedDict):
    """An [[Article]] that an external entity has paid to place or to produce to its specifications. Includes [advertorials](https://en.wikipedia.org/wiki/Advertorial), sponsored content, native advertising and other paid content.

    References:
        https://schema.org/AdvertiserContentArticle
    Note:
        Model Depth 4
    Attributes:
        pageEnd: (Optional[Union[List[Union[SchemaOrgObj, int, str]], SchemaOrgObj, int, str]]): The page on which the work ends; for example "138" or "xvi".
        wordCount: (Optional[Union[List[Union[SchemaOrgObj, int, str]], SchemaOrgObj, int, str]]): The number of words in the text of the Article.
        articleSection: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): Articles may belong to one or more 'sections' in a magazine or newspaper, such as Sports, Lifestyle, etc.
        articleBody: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The actual body of the article.
        speakable: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): Indicates sections of a Web page that are particularly 'speakable' in the sense of being highlighted as being especially appropriate for text-to-speech conversion. Other sections of a page may also be usefully spoken in particular circumstances; the 'speakable' property serves to indicate the parts most likely to be generally useful for speech.The *speakable* property can be repeated an arbitrary number of times, with three kinds of possible 'content-locator' values:1.) *id-value* URL references - uses *id-value* of an element in the page being annotated. The simplest use of *speakable* has (potentially relative) URL values, referencing identified sections of the document concerned.2.) CSS Selectors - addresses content in the annotated page, e.g. via class attribute. Use the [[cssSelector]] property.3.)  XPaths - addresses content via XPaths (assuming an XML view of the content). Use the [[xpath]] property.For more sophisticated markup of speakable sections beyond simple ID references, either CSS selectors or XPath expressions to pick out document section(s) as speakable. For thiswe define a supporting type, [[SpeakableSpecification]]  which is defined to be a possible value of the *speakable* property.         
        backstory: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): For an [[Article]], typically a [[NewsArticle]], the backstory property provides a textual summary giving a brief explanation of why and how an article was created. In a journalistic setting this could include information about reporting process, methods, interviews, data sources, etc.
        pagination: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): Any description of pages that is not separated into pageStart and pageEnd; for example, "1-6, 9, 55" or "10-12, 46-49".
        pageStart: (Optional[Union[List[Union[SchemaOrgObj, int, str]], SchemaOrgObj, int, str]]): The page on which the work starts; for example "135" or "xiii".
    """

    pageEnd: NotRequired[Union[List[Union[SchemaOrgObj, int, str]], SchemaOrgObj, int, str]]
    wordCount: NotRequired[Union[List[Union[SchemaOrgObj, int, str]], SchemaOrgObj, int, str]]
    articleSection: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    articleBody: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    speakable: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    backstory: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    pagination: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    pageStart: NotRequired[Union[List[Union[SchemaOrgObj, int, str]], SchemaOrgObj, int, str]]
    


class AdvertiserContentArticleProperties(TypedDict):
    """An [[Article]] that an external entity has paid to place or to produce to its specifications. Includes [advertorials](https://en.wikipedia.org/wiki/Advertorial), sponsored content, native advertising and other paid content.

    References:
        https://schema.org/AdvertiserContentArticle
    Note:
        Model Depth 4
    Attributes:
    """

    

#AdvertiserContentArticleInheritedPropertiesTd = AdvertiserContentArticleInheritedProperties()
#AdvertiserContentArticlePropertiesTd = AdvertiserContentArticleProperties()


class AllProperties(AdvertiserContentArticleInheritedProperties , AdvertiserContentArticleProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[AdvertiserContentArticleProperties, AdvertiserContentArticleInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "AdvertiserContentArticle"
    return model
    

AdvertiserContentArticle = create_schema_org_model()