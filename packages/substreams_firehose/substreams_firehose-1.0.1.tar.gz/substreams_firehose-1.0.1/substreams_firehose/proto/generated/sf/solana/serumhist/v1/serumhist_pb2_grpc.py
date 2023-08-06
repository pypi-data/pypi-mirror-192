"""Client and server classes corresponding to protobuf-defined services."""
import grpc
from .....sf.solana.serumhist.v1 import serumhist_pb2 as sf_dot_solana_dot_serumhist_dot_v1_dot_serumhist__pb2

class SerumOrderTrackerStub(object):
	"""Missing associated documentation comment in .proto file."""

	def __init__(self, channel):
		"""Constructor.

		Args:
			channel: A grpc.Channel.
		"""
		self.TrackOrder = channel.unary_stream('/sf.solana.serumhist.v1.SerumOrderTracker/TrackOrder', request_serializer=sf_dot_solana_dot_serumhist_dot_v1_dot_serumhist__pb2.TrackOrderRequest.SerializeToString, response_deserializer=sf_dot_solana_dot_serumhist_dot_v1_dot_serumhist__pb2.OrderTransition.FromString)

class SerumOrderTrackerServicer(object):
	"""Missing associated documentation comment in .proto file."""

	def TrackOrder(self, request, context):
		"""Missing associated documentation comment in .proto file."""
		context.set_code(grpc.StatusCode.UNIMPLEMENTED)
		context.set_details('Method not implemented!')
		raise NotImplementedError('Method not implemented!')

def add_SerumOrderTrackerServicer_to_server(servicer, server):
	rpc_method_handlers = {'TrackOrder': grpc.unary_stream_rpc_method_handler(servicer.TrackOrder, request_deserializer=sf_dot_solana_dot_serumhist_dot_v1_dot_serumhist__pb2.TrackOrderRequest.FromString, response_serializer=sf_dot_solana_dot_serumhist_dot_v1_dot_serumhist__pb2.OrderTransition.SerializeToString)}
	generic_handler = grpc.method_handlers_generic_handler('sf.solana.serumhist.v1.SerumOrderTracker', rpc_method_handlers)
	server.add_generic_rpc_handlers((generic_handler,))

class SerumOrderTracker(object):
	"""Missing associated documentation comment in .proto file."""

	@staticmethod
	def TrackOrder(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
		return grpc.experimental.unary_stream(request, target, '/sf.solana.serumhist.v1.SerumOrderTracker/TrackOrder', sf_dot_solana_dot_serumhist_dot_v1_dot_serumhist__pb2.TrackOrderRequest.SerializeToString, sf_dot_solana_dot_serumhist_dot_v1_dot_serumhist__pb2.OrderTransition.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

class SerumHistoryStub(object):
	"""Missing associated documentation comment in .proto file."""

	def __init__(self, channel):
		"""Constructor.

		Args:
			channel: A grpc.Channel.
		"""
		self.GetFills = channel.unary_unary('/sf.solana.serumhist.v1.SerumHistory/GetFills', request_serializer=sf_dot_solana_dot_serumhist_dot_v1_dot_serumhist__pb2.GetFillsRequest.SerializeToString, response_deserializer=sf_dot_solana_dot_serumhist_dot_v1_dot_serumhist__pb2.FillsResponse.FromString)

class SerumHistoryServicer(object):
	"""Missing associated documentation comment in .proto file."""

	def GetFills(self, request, context):
		"""Missing associated documentation comment in .proto file."""
		context.set_code(grpc.StatusCode.UNIMPLEMENTED)
		context.set_details('Method not implemented!')
		raise NotImplementedError('Method not implemented!')

def add_SerumHistoryServicer_to_server(servicer, server):
	rpc_method_handlers = {'GetFills': grpc.unary_unary_rpc_method_handler(servicer.GetFills, request_deserializer=sf_dot_solana_dot_serumhist_dot_v1_dot_serumhist__pb2.GetFillsRequest.FromString, response_serializer=sf_dot_solana_dot_serumhist_dot_v1_dot_serumhist__pb2.FillsResponse.SerializeToString)}
	generic_handler = grpc.method_handlers_generic_handler('sf.solana.serumhist.v1.SerumHistory', rpc_method_handlers)
	server.add_generic_rpc_handlers((generic_handler,))

class SerumHistory(object):
	"""Missing associated documentation comment in .proto file."""

	@staticmethod
	def GetFills(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
		return grpc.experimental.unary_unary(request, target, '/sf.solana.serumhist.v1.SerumHistory/GetFills', sf_dot_solana_dot_serumhist_dot_v1_dot_serumhist__pb2.GetFillsRequest.SerializeToString, sf_dot_solana_dot_serumhist_dot_v1_dot_serumhist__pb2.FillsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)