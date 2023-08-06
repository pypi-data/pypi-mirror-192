"""
SPARTNReader class.

The SPARTNReader class will parse individual SPARTN messages
from any binary stream containing *solely* SPARTN data e.g. an
MQTT `/pp/ip` topic.

Information sourced from https://www.spartnformat.org/download/
(available in the public domain)
© 2021 u-blox AG. All rights reserved.

SPARTN 1X transport layer bit format:
+-----------+------------+-------------+------------+-----------+----------+
| preamble  | framestart |   payload   |  payload   | embedded  |   crc    |
| 0x73  's' |            |  descriptor |            | auth data |          |
+-----------+------------+-------------+------------+-----------+----------+
|<--- 8 --->|<--- 24 --->|<-- 32-64 -->|<- 8-8192 ->|<- 0-512 ->|<- 8-32 ->|


Created on 10 Feb 2023

:author: semuadmin
:copyright: SEMU Consulting © 2023
:license: BSD 3-Clause
"""
# pylint: disable=invalid-name too-many-instance-attributes


from socket import socket
from pyspartn.socket_stream import SocketStream
from pyspartn.spartnhelpers import bitsval, valid_crc
from pyspartn.exceptions import SPARTNMessageError, SPARTNParseError, SPARTNStreamError
from pyspartn.spartntypes_core import SPARTN_PREB, VALCRC, VALNONE
from pyspartn.spartnmessage import SPARTNMessage


class SPARTNReader:
    """
    SPARTNReader class.
    """

    def __init__(self, datastream, **kwargs):
        """Constructor.

        :param datastream stream: input data stream
        :param int quitonerror: (kwarg) 0 = ignore,  1 = log and continue, 2 = (re)raise (1)
        :param int validate: (kwarg) 0 = ignore invalid CRC, 1 = validate CRC (1)
        :param bool scaling: (kwarg) apply attribute scaling True/False (True)
        :param int bufsize: (kwarg) socket recv buffer size (4096)
        :raises: SPARTNStreamError (if mode is invalid)
        """

        bufsize = int(kwargs.get("bufsize", 4096))
        if isinstance(datastream, socket):
            self._stream = SocketStream(datastream, bufsize=bufsize)
        else:
            self._stream = datastream
        self._validate = int(kwargs.get("validate", VALCRC))
        self._quitonerror = int(kwargs.get("quitonerror", 1))

    def __iter__(self):
        """Iterator."""

        return self

    def __next__(self) -> tuple:
        """
        Return next item in iteration.

        :return: tuple of (raw_data as bytes, parsed_data as SPARTNessage)
        :rtype: tuple
        :raises: StopIteration
        """

        (raw_data, parsed_data) = self.read()
        if raw_data is not None:
            return (raw_data, parsed_data)
        raise StopIteration

    def read(self) -> tuple:
        """
        Read a single SPARTN message from the stream buffer
        and return both raw and parsed data.
        'quitonerror' determines whether to raise, log or ignore parsing errors.

        :return: tuple of (raw_data as bytes, parsed_data as SPARTNMessage)
        :rtype: tuple
        :raises: SPARTNStreamError (if unrecognised protocol in data stream)
        """

        parsing = True

        try:
            while parsing:  # loop until end of valid message or EOF
                raw_data = None
                parsed_data = None
                byte1 = self._read_bytes(1)  # read the first byte
                # if not SPARTN, discard and continue
                if byte1 == SPARTN_PREB:
                    (raw_data, parsed_data) = self._parse_spartn(byte1)
                    parsing = False
                # unrecognised protocol header
                else:
                    if self._quitonerror == 2:
                        raise SPARTNStreamError(f"Unknown protocol {byte1}.")
                    if self._quitonerror == 1:
                        return (byte1, f"<UNKNOWN PROTOCOL(header={byte1})>")
                    continue

        except EOFError:
            return (None, None)

        return (raw_data, parsed_data)

    def _parse_spartn(self, preamble: bytes) -> tuple:
        """
        Parse any SPARTN data in the stream. The structure of the transport layer
        depends on encryption type, GNSS timetag format and CRC format.

        :param preamble hdr: preamble of SPARTN message
        :return: tuple of (raw_data as bytes, parsed_stub as SPARTNMessage)
        :rtype: tuple
        :raises: SPARTNParseError if CRC invalid; EOFError if premature end of file
        """
        # pylint: disable=unused-variable

        framestart = self._read_bytes(3)
        # msgType = bitsval(framestart, 0, 7)
        nData = bitsval(framestart, 7, 10)
        eaf = bitsval(framestart, 17, 1)
        crcType = bitsval(framestart, 18, 2)
        # frameCrc = bitsval(framestart, 20, 4)

        payDesc = self._read_bytes(4)
        # msgSubtype = bitsval(payDesc, 0, 4)
        timeTagtype = bitsval(payDesc, 4, 1)
        if timeTagtype:
            payDesc += self._read_bytes(2)
        gtlen = 32 if timeTagtype else 16
        # gnssTimeTag = bitsval(payDesc, 5, gtlen)
        # solutionId = bitsval(payDesc, gtlen + 5, 7)
        # solutionProcId = bitsval(payDesc, gtlen + 12, 4)
        authInd = 0
        if eaf:
            payDesc += self._read_bytes(2)
            # encryptionId = bitsval(payDesc, gtlen + 16, 4)
            # encryptionSeq = bitsval(payDesc, gtlen + 20, 6)
            authInd = bitsval(payDesc, gtlen + 26, 3)
            embAuthLen = bitsval(payDesc, gtlen + 29, 3)
        payload = self._read_bytes(nData)
        embAuth = b""
        if authInd > 1:
            if embAuthLen == 0:
                aln = 8
            elif embAuthLen == 1:
                aln = 12
            elif embAuthLen == 2:
                aln = 16
            elif embAuthLen == 3:
                aln = 32
            elif embAuthLen == 4:
                aln = 64
            else:
                aln = 0
            embAuth = self._read_bytes(aln)
        crcb = self._read_bytes(crcType + 1)
        crc = int.from_bytes(crcb, "big")

        # validate CRC
        core = framestart + payDesc + payload + embAuth
        if self._validate & VALCRC:
            if not valid_crc(core, crc, crcType):
                raise SPARTNParseError(f"Invalid CRC {crc}")

        raw_data = preamble + core + crcb
        parsed_data = self.parse(raw_data, validate=VALNONE)

        return (raw_data, parsed_data)

    def _read_bytes(self, size: int) -> bytes:
        """
        Read a specified number of bytes from stream.

        :param int size: number of bytes to read
        :return: bytes
        :rtype: bytes
        :raises: EOFError if stream ends prematurely
        """

        data = self._stream.read(size)
        if len(data) < size:  # EOF
            raise EOFError()
        return data

    def iterate(self, **kwargs) -> tuple:
        """
        Invoke the iterator within an exception handling framework.

        :param int quitonerror: (kwarg) 0 = ignore,  1 = log and continue, 2 = (re)raise (1)
        :param object errorhandler: (kwarg) Optional error handler (None)
        :return: tuple of (raw_data as bytes, parsed_data as SPARTNMessage)
        :rtype: tuple
        :raises: SPARTN...Error (if quitonerror is set and stream is invalid)
        """

        quitonerror = kwargs.get("quitonerror", self._quitonerror)
        errorhandler = kwargs.get("errorhandler", None)

        while True:
            try:
                yield next(self)  # invoke the iterator
            except StopIteration:
                break
            except (
                SPARTNMessageError,
                SPARTNParseError,
                SPARTNStreamError,
            ) as err:
                # raise, log or ignore any error depending
                # on the quitonerror setting
                if quitonerror == 2:
                    raise err
                if quitonerror == 1:
                    # pass to error handler if there is one
                    if errorhandler is None:
                        print(err)
                    else:
                        errorhandler(err)
                # continue

    @property
    def datastream(self) -> object:
        """
        Getter for stream.

        :return: data stream
        :rtype: object
        """

        return self._stream

    @staticmethod
    def parse(message: bytes, **kwargs) -> SPARTNMessage:
        """
        Parse SPARTN message to SPARTNMessage object.

        :param bytes message: SPARTN raw message bytes
        :param int validate: (kwarg) 0 = ignore invalid CRC, 1 = validate CRC (1)
        :return: SPARTNMessage object
        :rtype: SPARTNMessage
        :raises: SPARTN...Error (if data stream contains invalid data or unknown message type)
        """
        # pylint: disable=unused-argument

        validate = int(kwargs.get("validate", VALCRC))
        return SPARTNMessage(transport=message, validate=validate)
