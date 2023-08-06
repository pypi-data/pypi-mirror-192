import socket
import lz4.frame
import zstd
import xml.etree.ElementTree as ET
from deprecated import deprecated

import dv.fb.Frame
import dv.fb.Event
import dv.fb.IMU
import dv.fb.Trigger

import dv.fb.EventPacket
import dv.fb.FrameFormat
import dv.fb.IMUPacket
import dv.fb.TriggerPacket

from dv import Frame, Trigger, Event, IMU


class SocketInput:

    def __init__(self, path='/tmp/dv-runtime.sock', as_numpy=False):
        self._path = path
        self._socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._socket.connect(path)
        self._as_numpy = as_numpy
        self._parseIOHeader()
        self._packet = None
        self._packetIteratorPosition = -1

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._socket.close()

    def __del__(self):
        self._socket.close()

    def __iter__(self):
        return self

    def __next__(self):
        if self._packet is None:
            self._receive_next_packet()
            self._packetIteratorPosition = 0

        obj = self._construct_obj_from_packet()
        self._packetIteratorPosition += 1

        if self._reset_packet():
            self._packet = None
            self._packetIteratorPosition = -1

        return obj

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def source(self):
        if 'source' in self._stream_info:
            return self._stream_info['source']
        raise NameError('Source attribute not present for input')

    @property
    def id(self):
        return self._id

    @property
    def size_x(self):
        if 'sizeX' in self._stream_info:
            return self._stream_info['sizeX']
        raise NameError('SizeX attribute not present for input of type ' + self.type)

    @property
    def size_y(self):
        if 'sizeY' in self._stream_info:
            return self._stream_info['sizeY']
        raise NameError('SizeY attribute not present for input of type ' + self.type)

    @property
    def size(self):
        return self.size_y, self.size_x

    @property
    def tsOffset(self):
        if 'tsOffset' in self._stream_info:
            return self._stream_info['tsOffset']
        raise NameError('TsOffset attribute not present for input of type ' + self.type)

    def _parseIOHeader(self):
        header_size_raw = self._socket.recv(4, socket.MSG_WAITALL)
        if len(header_size_raw) != 4:
            raise RuntimeError("Socket read failure")

        header_size = int.from_bytes(header_size_raw, byteorder='little')
        io_header_raw = self._socket.recv(header_size, socket.MSG_WAITALL)
        if len(io_header_raw) != header_size:
            raise RuntimeError("Socket read failure")

        io_header = dv.fb.IOHeader.IOHeader.GetRootAsIOHeader(io_header_raw, 0)
        self._compression = io_header.Compression()
        info_node = io_header.InfoNode()

        xml_root = ET.fromstring(info_node)
        output_node = xml_root[0].find("node")

        child_attrs = {child.attrib['key']: child.text for child in output_node if child.tag == 'attr'}
        self._name = child_attrs['originalOutputName']

        self._id = int(output_node.attrib['name'])
        self._type = child_attrs['typeIdentifier']

        for c in output_node:
            if c.tag == 'node' and c.attrib['name'] == 'info':
                self._stream_info = {a.attrib['key']: a.text for a in c if a.tag == 'attr'}
                break

    def _receive_next_packet(self):
        packet_header = self._socket.recv(8, socket.MSG_WAITALL)
        if len(packet_header) != 8:
            raise RuntimeError("Socket read failure")

        length = int.from_bytes(packet_header[4:], byteorder='little')
        packet_data = self._socket.recv(length, socket.MSG_WAITALL)
        if len(packet_data) != length:
            raise RuntimeError("Socket read failure")

        if self._compression == dv.fb.CompressionType.CompressionType.NONE:
            packet_data = packet_data[4:]
        elif self._compression == dv.fb.CompressionType.CompressionType.LZ4 or self._compression == dv.fb.CompressionType.CompressionType.LZ4_HIGH:
            packet_data = lz4.frame.decompress(packet_data)[4:]
        elif self._compression == dv.fb.CompressionType.CompressionType.ZSTD or self._compression == dv.fb.CompressionType.CompressionType.ZSTD_HIGH:
            packet_data = zstd.decompress(packet_data)[4:]
        else:
            raise RuntimeError("File uses an unsupported type of data compression")

        self._parse_packet(packet_data)

    def _parse_packet(self, packet_data):
        if self.type == 'EVTS':
            self._packet = dv.fb.EventPacket.EventPacket.GetRootAsEventPacket(packet_data, 0)
        elif self.type == 'FRME':
            self._packet = dv.fb.Frame.Frame.GetRootAsFrame(packet_data, 0)
        elif self.type == 'IMUS':
            self._packet = dv.fb.IMUPacket.IMUPacket.GetRootAsIMUPacket(packet_data, 0)
        elif self.type == 'TRIG':
            self._packet = dv.fb.TriggerPacket.TriggerPacket.GetRootAsTriggerPacket(packet_data, 0)
        else:
            raise RuntimeError('Unknown datatype %s for stream with name %s' % self.type)

    def _construct_obj_from_packet(self):
        if self.type == 'EVTS':
            if self._as_numpy:
                return self._packet.EventsBufferAsNumpy()
            else:
                return Event.Event(self._packet.Events(self._packetIteratorPosition))
        elif self.type == 'FRME':
            return Frame.Frame(self._packet)
        elif self.type == 'IMUS':
            return IMU.IMUSample(self._packet.Samples(self._packetIteratorPosition))
        elif self.type == 'TRIG':
            return Trigger.Trigger(self._packet.Triggers(self._packetIteratorPosition))
        else:
            raise RuntimeError('Unknown datatype %s for stream with name %s' % self.type)

    def _reset_packet(self):
        if self.type == 'EVTS':
            if self._as_numpy:
                return True
            else:
                return self._packetIteratorPosition >= self._packet.EventsLength()
        elif self.type == 'FRME':
            return True
        elif self.type == 'IMUS':
            return self._packetIteratorPosition >= self._packet.SamplesLength()
        elif self.type == 'TRIG':
            return self._packetIteratorPosition >= self._packet.TriggersLength()
        else:
            raise RuntimeError('Unknown datatype %s for stream with name %s' % self.type)


@deprecated("Explicit creation of SocketEventInput will be removed in a future release, "
            "use SocketInput instead, which provides automatic type detection")
class SocketEventInput(SocketInput):

    def __init__(self, path='/tmp/dv-runtime.sock'):
        super().__init__(path)
        if self.type != 'EVTS':
            raise TypeError("Incoming stream is not of type 'EVTS', but " + self.type)


@deprecated(
    "Explicit creation of SocketNumpyEventPacketInput will be removed in a future release, "
    "use SocketInput instead, which provides automatic type detection, passing as_numpy=True to get events as Numpy arrays"
)
class SocketNumpyEventPacketInput(SocketInput):

    def __init__(self, path='/tmp/dv-runtime.sock'):
        super().__init__(path, as_numpy=True)
        if self.type != 'EVTS':
            raise TypeError("Incoming stream is not of type 'EVTS', but " + self.type)


@deprecated("Explicit creation of SocketFrameInput will be removed in a future release, "
            "use SocketInput instead, which provides automatic type detection")
class SocketFrameInput(SocketInput):

    def __init__(self, path='/tmp/dv-runtime.sock'):
        super().__init__(path)
        if self.type != 'FRME':
            raise TypeError("Incoming stream is not of type 'FRME', but " + self.type)


@deprecated("Explicit creation of SocketIMUInput will be removed in a future release, "
            "use SocketInput instead, which provides automatic type detection")
class SocketIMUInput(SocketInput):

    def __init__(self, path='/tmp/dv-runtime.sock'):
        super().__init__(path)
        if self.type != 'IMUS':
            raise TypeError("Incoming stream is not of type 'IMUS', but " + self.type)


@deprecated("Explicit creation of SocketTriggerInput will be removed in a future release, "
            "use SocketInput instead, which provides automatic type detection")
class SocketTriggerInput(SocketInput):

    def __init__(self, path='/tmp/dv-runtime.sock'):
        super().__init__(path)
        if self.type != 'TRIG':
            raise TypeError("Incoming stream is not of type 'TRIG', but " + self.type)
