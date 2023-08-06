"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from ....sf.substreams.v1 import modules_pb2 as sf_dot_substreams_dot_v1_dot_modules__pb2
from ....sf.substreams.v1 import clock_pb2 as sf_dot_substreams_dot_v1_dot_clock__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n!sf/substreams/v1/substreams.proto\x12\x10sf.substreams.v1\x1a\x19google/protobuf/any.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1esf/substreams/v1/modules.proto\x1a\x1csf/substreams/v1/clock.proto"\xc9\x02\n\x07Request\x12\x17\n\x0fstart_block_num\x18\x01 \x01(\x03\x12\x14\n\x0cstart_cursor\x18\x02 \x01(\t\x12\x16\n\x0estop_block_num\x18\x03 \x01(\x04\x12.\n\nfork_steps\x18\x04 \x03(\x0e2\x1a.sf.substreams.v1.ForkStep\x12!\n\x19irreversibility_condition\x18\x05 \x01(\t\x12\x17\n\x0fproduction_mode\x18\t \x01(\x08\x12*\n\x07modules\x18\x06 \x01(\x0b2\x19.sf.substreams.v1.Modules\x12\x16\n\x0eoutput_modules\x18\x07 \x03(\t\x120\n(debug_initial_store_snapshot_for_modules\x18\x08 \x03(\t\x12\x15\n\routput_module\x18\n \x01(\t"\xc5\x02\n\x08Response\x120\n\x07session\x18\x05 \x01(\x0b2\x1d.sf.substreams.v1.SessionInitH\x00\x125\n\x08progress\x18\x01 \x01(\x0b2!.sf.substreams.v1.ModulesProgressH\x00\x12D\n\x13debug_snapshot_data\x18\x02 \x01(\x0b2%.sf.substreams.v1.InitialSnapshotDataH\x00\x12L\n\x17debug_snapshot_complete\x18\x03 \x01(\x0b2).sf.substreams.v1.InitialSnapshotCompleteH\x00\x121\n\x04data\x18\x04 \x01(\x0b2!.sf.substreams.v1.BlockScopedDataH\x00B\t\n\x07message"\x1f\n\x0bSessionInit\x12\x10\n\x08trace_id\x18\x01 \x01(\t")\n\x17InitialSnapshotComplete\x12\x0e\n\x06cursor\x18\x01 \x01(\t"\x80\x01\n\x13InitialSnapshotData\x12\x13\n\x0bmodule_name\x18\x01 \x01(\t\x12-\n\x06deltas\x18\x02 \x01(\x0b2\x1d.sf.substreams.v1.StoreDeltas\x12\x11\n\tsent_keys\x18\x04 \x01(\x04\x12\x12\n\ntotal_keys\x18\x03 \x01(\x04"\xa4\x01\n\x0fBlockScopedData\x12/\n\x07outputs\x18\x01 \x03(\x0b2\x1e.sf.substreams.v1.ModuleOutput\x12&\n\x05clock\x18\x03 \x01(\x0b2\x17.sf.substreams.v1.Clock\x12(\n\x04step\x18\x06 \x01(\x0e2\x1a.sf.substreams.v1.ForkStep\x12\x0e\n\x06cursor\x18\n \x01(\t"\xcf\x01\n\x0cModuleOutput\x12\x0c\n\x04name\x18\x01 \x01(\t\x12*\n\nmap_output\x18\x02 \x01(\x0b2\x14.google.protobuf.AnyH\x00\x12;\n\x12debug_store_deltas\x18\x03 \x01(\x0b2\x1d.sf.substreams.v1.StoreDeltasH\x00\x12\x12\n\ndebug_logs\x18\x04 \x03(\t\x12\x1c\n\x14debug_logs_truncated\x18\x05 \x01(\x08\x12\x0e\n\x06cached\x18\x06 \x01(\x08B\x06\n\x04data"D\n\x0fModulesProgress\x121\n\x07modules\x18\x01 \x03(\x0b2 .sf.substreams.v1.ModuleProgress"\x98\x05\n\x0eModuleProgress\x12\x0c\n\x04name\x18\x01 \x01(\t\x12K\n\x10processed_ranges\x18\x02 \x01(\x0b2/.sf.substreams.v1.ModuleProgress.ProcessedRangeH\x00\x12F\n\rinitial_state\x18\x03 \x01(\x0b2-.sf.substreams.v1.ModuleProgress.InitialStateH\x00\x12J\n\x0fprocessed_bytes\x18\x04 \x01(\x0b2/.sf.substreams.v1.ModuleProgress.ProcessedBytesH\x00\x129\n\x06failed\x18\x05 \x01(\x0b2\'.sf.substreams.v1.ModuleProgress.FailedH\x00\x1aH\n\x0eProcessedRange\x126\n\x10processed_ranges\x18\x01 \x03(\x0b2\x1c.sf.substreams.v1.BlockRange\x1a-\n\x0cInitialState\x12\x1d\n\x15available_up_to_block\x18\x02 \x01(\x04\x1a\x9a\x01\n\x0eProcessedBytes\x12\x18\n\x10total_bytes_read\x18\x01 \x01(\x04\x12\x1b\n\x13total_bytes_written\x18\x02 \x01(\x04\x12\x18\n\x10bytes_read_delta\x18\x03 \x01(\x04\x12\x1b\n\x13bytes_written_delta\x18\x04 \x01(\x04\x12\x1a\n\x12nano_seconds_delta\x18\x05 \x01(\x04\x1a>\n\x06Failed\x12\x0e\n\x06reason\x18\x01 \x01(\t\x12\x0c\n\x04logs\x18\x02 \x03(\t\x12\x16\n\x0elogs_truncated\x18\x03 \x01(\x08B\x06\n\x04type"4\n\nBlockRange\x12\x13\n\x0bstart_block\x18\x02 \x01(\x04\x12\x11\n\tend_block\x18\x03 \x01(\x04";\n\x0bStoreDeltas\x12,\n\x06deltas\x18\x01 \x03(\x0b2\x1c.sf.substreams.v1.StoreDelta"\xc7\x01\n\nStoreDelta\x129\n\toperation\x18\x01 \x01(\x0e2&.sf.substreams.v1.StoreDelta.Operation\x12\x0f\n\x07ordinal\x18\x02 \x01(\x04\x12\x0b\n\x03key\x18\x03 \x01(\t\x12\x11\n\told_value\x18\x04 \x01(\x0c\x12\x11\n\tnew_value\x18\x05 \x01(\x0c":\n\tOperation\x12\t\n\x05UNSET\x10\x00\x12\n\n\x06CREATE\x10\x01\x12\n\n\x06UPDATE\x10\x02\x12\n\n\x06DELETE\x10\x03"\x81\x01\n\x06Output\x12\x11\n\tblock_num\x18\x01 \x01(\x04\x12\x10\n\x08block_id\x18\x02 \x01(\t\x12-\n\ttimestamp\x18\x04 \x01(\x0b2\x1a.google.protobuf.Timestamp\x12#\n\x05value\x18\n \x01(\x0b2\x14.google.protobuf.Any*\\\n\x08ForkStep\x12\x10\n\x0cSTEP_UNKNOWN\x10\x00\x12\x0c\n\x08STEP_NEW\x10\x01\x12\r\n\tSTEP_UNDO\x10\x02\x12\x15\n\x11STEP_IRREVERSIBLE\x10\x04"\x04\x08\x03\x10\x03"\x04\x08\x05\x10\x052K\n\x06Stream\x12A\n\x06Blocks\x12\x19.sf.substreams.v1.Request\x1a\x1a.sf.substreams.v1.Response0\x01BFZDgithub.com/streamingfast/substreams/pb/sf/substreams/v1;pbsubstreamsb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sf.substreams.v1.substreams_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
	DESCRIPTOR._options = None
	DESCRIPTOR._serialized_options = b'ZDgithub.com/streamingfast/substreams/pb/sf/substreams/v1;pbsubstreams'
	_FORKSTEP._serialized_start = 2607
	_FORKSTEP._serialized_end = 2699
	_REQUEST._serialized_start = 178
	_REQUEST._serialized_end = 507
	_RESPONSE._serialized_start = 510
	_RESPONSE._serialized_end = 835
	_SESSIONINIT._serialized_start = 837
	_SESSIONINIT._serialized_end = 868
	_INITIALSNAPSHOTCOMPLETE._serialized_start = 870
	_INITIALSNAPSHOTCOMPLETE._serialized_end = 911
	_INITIALSNAPSHOTDATA._serialized_start = 914
	_INITIALSNAPSHOTDATA._serialized_end = 1042
	_BLOCKSCOPEDDATA._serialized_start = 1045
	_BLOCKSCOPEDDATA._serialized_end = 1209
	_MODULEOUTPUT._serialized_start = 1212
	_MODULEOUTPUT._serialized_end = 1419
	_MODULESPROGRESS._serialized_start = 1421
	_MODULESPROGRESS._serialized_end = 1489
	_MODULEPROGRESS._serialized_start = 1492
	_MODULEPROGRESS._serialized_end = 2156
	_MODULEPROGRESS_PROCESSEDRANGE._serialized_start = 1808
	_MODULEPROGRESS_PROCESSEDRANGE._serialized_end = 1880
	_MODULEPROGRESS_INITIALSTATE._serialized_start = 1882
	_MODULEPROGRESS_INITIALSTATE._serialized_end = 1927
	_MODULEPROGRESS_PROCESSEDBYTES._serialized_start = 1930
	_MODULEPROGRESS_PROCESSEDBYTES._serialized_end = 2084
	_MODULEPROGRESS_FAILED._serialized_start = 2086
	_MODULEPROGRESS_FAILED._serialized_end = 2148
	_BLOCKRANGE._serialized_start = 2158
	_BLOCKRANGE._serialized_end = 2210
	_STOREDELTAS._serialized_start = 2212
	_STOREDELTAS._serialized_end = 2271
	_STOREDELTA._serialized_start = 2274
	_STOREDELTA._serialized_end = 2473
	_STOREDELTA_OPERATION._serialized_start = 2415
	_STOREDELTA_OPERATION._serialized_end = 2473
	_OUTPUT._serialized_start = 2476
	_OUTPUT._serialized_end = 2605
	_STREAM._serialized_start = 2701
	_STREAM._serialized_end = 2776