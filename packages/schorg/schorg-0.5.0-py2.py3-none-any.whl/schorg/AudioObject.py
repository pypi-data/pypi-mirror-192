"""
An audio file.

https://schema.org/AudioObject
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class AudioObjectInheritedProperties(TypedDict):
    """An audio file.

    References:
        https://schema.org/AudioObject
    Note:
        Model Depth 4
    Attributes:
        embedUrl: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): A URL pointing to a player for a specific video. In general, this is the information in the ```src``` element of an ```embed``` tag and should not be the same as the content of the ```loc``` tag.
        bitrate: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The bitrate of the media object.
        width: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The width of the item.
        sha256: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The [SHA-2](https://en.wikipedia.org/wiki/SHA-2) SHA256 hash of the content of the item. For example, a zero-length input has value 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
        endTime: (Optional[Union[List[Union[datetime, SchemaOrgObj, str]], datetime, SchemaOrgObj, str]]): The endTime of something. For a reserved event or service (e.g. FoodEstablishmentReservation), the time that it is expected to end. For actions that span a period of time, when the action was performed. E.g. John wrote a book from January to *December*. For media, including audio and video, it's the time offset of the end of a clip within a larger file.Note that Event uses startDate/endDate instead of startTime/endTime, even when describing dates with times. This situation may be clarified in future revisions.
        startTime: (Optional[Union[List[Union[datetime, SchemaOrgObj, str]], datetime, SchemaOrgObj, str]]): The startTime of something. For a reserved event or service (e.g. FoodEstablishmentReservation), the time that it is expected to start. For actions that span a period of time, when the action was performed. E.g. John wrote a book from *January* to December. For media, including audio and video, it's the time offset of the start of a clip within a larger file.Note that Event uses startDate/endDate instead of startTime/endTime, even when describing dates with times. This situation may be clarified in future revisions.
        contentSize: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): File size in (mega/kilo)bytes.
        height: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The height of the item.
        playerType: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): Player type required&#x2014;for example, Flash or Silverlight.
        associatedArticle: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A NewsArticle associated with the Media Object.
        interpretedAsClaim: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Used to indicate a specific claim contained, implied, translated or refined from the content of a [[MediaObject]] or other [[CreativeWork]]. The interpreting party can be indicated using [[claimInterpreter]].
        duration: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The duration of the item (movie, audio recording, event, etc.) in [ISO 8601 date format](http://en.wikipedia.org/wiki/ISO_8601).
        requiresSubscription: (Optional[Union[List[Union[StrictBool, SchemaOrgObj, str]], StrictBool, SchemaOrgObj, str]]): Indicates if use of the media require a subscription  (either paid or free). Allowed values are ```true``` or ```false``` (note that an earlier version had 'yes', 'no').
        regionsAllowed: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The regions where the media is allowed. If not specified, then it's assumed to be allowed everywhere. Specify the countries in [ISO 3166 format](http://en.wikipedia.org/wiki/ISO_3166).
        contentUrl: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): Actual bytes of the media object, for example the image file or video file.
        productionCompany: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The production company or studio responsible for the item, e.g. series, video game, episode etc.
        encodesCreativeWork: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The CreativeWork encoded by this media object.
        uploadDate: (Optional[Union[List[Union[SchemaOrgObj, str, date]], SchemaOrgObj, str, date]]): Date when this media object was uploaded to this site.
        ineligibleRegion: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The ISO 3166-1 (ISO 3166-1 alpha-2) or ISO 3166-2 code, the place, or the GeoShape for the geo-political region(s) for which the offer or delivery charge specification is not valid, e.g. a region where the transaction is not allowed.See also [[eligibleRegion]].      
        encodingFormat: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): Media type typically expressed using a MIME format (see [IANA site](http://www.iana.org/assignments/media-types/media-types.xhtml) and [MDN reference](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types)), e.g. application/zip for a SoftwareApplication binary, audio/mpeg for .mp3 etc.In cases where a [[CreativeWork]] has several media type representations, [[encoding]] can be used to indicate each [[MediaObject]] alongside particular [[encodingFormat]] information.Unregistered or niche encoding and file formats can be indicated instead via the most appropriate URL, e.g. defining Web page or a Wikipedia/Wikidata entry.
    """

    embedUrl: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    bitrate: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    width: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    sha256: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    endTime: NotRequired[Union[List[Union[datetime, SchemaOrgObj, str]], datetime, SchemaOrgObj, str]]
    startTime: NotRequired[Union[List[Union[datetime, SchemaOrgObj, str]], datetime, SchemaOrgObj, str]]
    contentSize: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    height: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    playerType: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    associatedArticle: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    interpretedAsClaim: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    duration: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    requiresSubscription: NotRequired[Union[List[Union[StrictBool, SchemaOrgObj, str]], StrictBool, SchemaOrgObj, str]]
    regionsAllowed: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    contentUrl: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    productionCompany: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    encodesCreativeWork: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    uploadDate: NotRequired[Union[List[Union[SchemaOrgObj, str, date]], SchemaOrgObj, str, date]]
    ineligibleRegion: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    encodingFormat: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    


class AudioObjectProperties(TypedDict):
    """An audio file.

    References:
        https://schema.org/AudioObject
    Note:
        Model Depth 4
    Attributes:
        caption: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The caption for this object. For downloadable machine formats (closed caption, subtitles etc.) use MediaObject and indicate the [[encodingFormat]].
        embeddedTextCaption: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): Represents textual captioning from a [[MediaObject]], e.g. text of a 'meme'.
        transcript: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): If this MediaObject is an AudioObject or VideoObject, the transcript of that object.
    """

    caption: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    embeddedTextCaption: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    transcript: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    

#AudioObjectInheritedPropertiesTd = AudioObjectInheritedProperties()
#AudioObjectPropertiesTd = AudioObjectProperties()


class AllProperties(AudioObjectInheritedProperties , AudioObjectProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[AudioObjectProperties, AudioObjectInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "AudioObject"
    return model
    

AudioObject = create_schema_org_model()