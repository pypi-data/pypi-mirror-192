from typing import Literal, Optional

import msgspec


class Connection(msgspec.Struct, tag_field="op", tag=str.lower):
    """
    Connection Message
    """

    connectionId: str


class Status(msgspec.Struct, tag_field="op", tag=str.lower):
    """
    Status Message
    """

    statusCode: Literal["SUCCESS", "FAILURE"]
    connectionClosed: bool
    errorCode: Optional[str] = None
    errorMessage: Optional[str] = None
    connectionsAvailable: Optional[int] = None
