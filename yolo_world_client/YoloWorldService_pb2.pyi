from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ObjectData(_message.Message):
    __slots__ = ("ClassId", "Confidence", "CenterX", "CenterY", "BoundingWidth", "BoundingHeight")
    CLASSID_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    CENTERX_FIELD_NUMBER: _ClassVar[int]
    CENTERY_FIELD_NUMBER: _ClassVar[int]
    BOUNDINGWIDTH_FIELD_NUMBER: _ClassVar[int]
    BOUNDINGHEIGHT_FIELD_NUMBER: _ClassVar[int]
    ClassId: int
    Confidence: float
    CenterX: float
    CenterY: float
    BoundingWidth: float
    BoundingHeight: float
    def __init__(self, ClassId: _Optional[int] = ..., Confidence: _Optional[float] = ..., CenterX: _Optional[float] = ..., CenterY: _Optional[float] = ..., BoundingWidth: _Optional[float] = ..., BoundingHeight: _Optional[float] = ...) -> None: ...

class DetectionRequest(_message.Message):
    __slots__ = ("ClientName", "ClassNames", "JpegImage")
    CLIENTNAME_FIELD_NUMBER: _ClassVar[int]
    CLASSNAMES_FIELD_NUMBER: _ClassVar[int]
    JPEGIMAGE_FIELD_NUMBER: _ClassVar[int]
    ClientName: str
    ClassNames: _containers.RepeatedScalarFieldContainer[str]
    JpegImage: bytes
    def __init__(self, ClientName: _Optional[str] = ..., ClassNames: _Optional[_Iterable[str]] = ..., JpegImage: _Optional[bytes] = ...) -> None: ...

class DetectionResponse(_message.Message):
    __slots__ = ("Objects",)
    OBJECTS_FIELD_NUMBER: _ClassVar[int]
    Objects: _containers.RepeatedCompositeFieldContainer[ObjectData]
    def __init__(self, Objects: _Optional[_Iterable[_Union[ObjectData, _Mapping]]] = ...) -> None: ...

class LabelRequest(_message.Message):
    __slots__ = ("ClientName", "ClassNames", "JpegImage")
    CLIENTNAME_FIELD_NUMBER: _ClassVar[int]
    CLASSNAMES_FIELD_NUMBER: _ClassVar[int]
    JPEGIMAGE_FIELD_NUMBER: _ClassVar[int]
    ClientName: str
    ClassNames: _containers.RepeatedScalarFieldContainer[str]
    JpegImage: bytes
    def __init__(self, ClientName: _Optional[str] = ..., ClassNames: _Optional[_Iterable[str]] = ..., JpegImage: _Optional[bytes] = ...) -> None: ...

class LabelResponse(_message.Message):
    __slots__ = ("JpegImage",)
    JPEGIMAGE_FIELD_NUMBER: _ClassVar[int]
    JpegImage: bytes
    def __init__(self, JpegImage: _Optional[bytes] = ...) -> None: ...
