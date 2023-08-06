"""Client and server classes corresponding to protobuf-defined services."""
import grpc
from ....dfuse.bstream.v1 import bstream_pb2 as dfuse_dot_bstream_dot_v1_dot_bstream__pb2

class BlockStreamStub(object):
	"""Missing associated documentation comment in .proto file."""

	def __init__(self, channel):
		"""Constructor.

		Args:
			channel: A grpc.Channel.
		"""
		self.Blocks = channel.unary_stream('/dfuse.bstream.v1.BlockStream/Blocks', request_serializer=dfuse_dot_bstream_dot_v1_dot_bstream__pb2.BlockRequest.SerializeToString, response_deserializer=dfuse_dot_bstream_dot_v1_dot_bstream__pb2.Block.FromString)

class BlockStreamServicer(object):
	"""Missing associated documentation comment in .proto file."""

	def Blocks(self, request, context):
		"""Missing associated documentation comment in .proto file."""
		context.set_code(grpc.StatusCode.UNIMPLEMENTED)
		context.set_details('Method not implemented!')
		raise NotImplementedError('Method not implemented!')

def add_BlockStreamServicer_to_server(servicer, server):
	rpc_method_handlers = {'Blocks': grpc.unary_stream_rpc_method_handler(servicer.Blocks, request_deserializer=dfuse_dot_bstream_dot_v1_dot_bstream__pb2.BlockRequest.FromString, response_serializer=dfuse_dot_bstream_dot_v1_dot_bstream__pb2.Block.SerializeToString)}
	generic_handler = grpc.method_handlers_generic_handler('dfuse.bstream.v1.BlockStream', rpc_method_handlers)
	server.add_generic_rpc_handlers((generic_handler,))

class BlockStream(object):
	"""Missing associated documentation comment in .proto file."""

	@staticmethod
	def Blocks(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
		return grpc.experimental.unary_stream(request, target, '/dfuse.bstream.v1.BlockStream/Blocks', dfuse_dot_bstream_dot_v1_dot_bstream__pb2.BlockRequest.SerializeToString, dfuse_dot_bstream_dot_v1_dot_bstream__pb2.Block.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

class BlockStreamV2Stub(object):
	"""Missing associated documentation comment in .proto file."""

	def __init__(self, channel):
		"""Constructor.

		Args:
			channel: A grpc.Channel.
		"""
		self.Blocks = channel.unary_stream('/dfuse.bstream.v1.BlockStreamV2/Blocks', request_serializer=dfuse_dot_bstream_dot_v1_dot_bstream__pb2.BlocksRequestV2.SerializeToString, response_deserializer=dfuse_dot_bstream_dot_v1_dot_bstream__pb2.BlockResponseV2.FromString)

class BlockStreamV2Servicer(object):
	"""Missing associated documentation comment in .proto file."""

	def Blocks(self, request, context):
		"""Missing associated documentation comment in .proto file."""
		context.set_code(grpc.StatusCode.UNIMPLEMENTED)
		context.set_details('Method not implemented!')
		raise NotImplementedError('Method not implemented!')

def add_BlockStreamV2Servicer_to_server(servicer, server):
	rpc_method_handlers = {'Blocks': grpc.unary_stream_rpc_method_handler(servicer.Blocks, request_deserializer=dfuse_dot_bstream_dot_v1_dot_bstream__pb2.BlocksRequestV2.FromString, response_serializer=dfuse_dot_bstream_dot_v1_dot_bstream__pb2.BlockResponseV2.SerializeToString)}
	generic_handler = grpc.method_handlers_generic_handler('dfuse.bstream.v1.BlockStreamV2', rpc_method_handlers)
	server.add_generic_rpc_handlers((generic_handler,))

class BlockStreamV2(object):
	"""Missing associated documentation comment in .proto file."""

	@staticmethod
	def Blocks(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
		return grpc.experimental.unary_stream(request, target, '/dfuse.bstream.v1.BlockStreamV2/Blocks', dfuse_dot_bstream_dot_v1_dot_bstream__pb2.BlocksRequestV2.SerializeToString, dfuse_dot_bstream_dot_v1_dot_bstream__pb2.BlockResponseV2.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)