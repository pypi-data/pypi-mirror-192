"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1esf/substreams/v1/modules.proto\x12\x10sf.substreams.v1"`\n\x07Modules\x12)\n\x07modules\x18\x01 \x03(\x0b2\x18.sf.substreams.v1.Module\x12*\n\x08binaries\x18\x02 \x03(\x0b2\x18.sf.substreams.v1.Binary"\'\n\x06Binary\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\x0f\n\x07content\x18\x02 \x01(\x0c"\x87\x08\n\x06Module\x12\x0c\n\x04name\x18\x01 \x01(\t\x124\n\x08kind_map\x18\x02 \x01(\x0b2 .sf.substreams.v1.Module.KindMapH\x00\x128\n\nkind_store\x18\x03 \x01(\x0b2".sf.substreams.v1.Module.KindStoreH\x00\x12\x14\n\x0cbinary_index\x18\x04 \x01(\r\x12\x19\n\x11binary_entrypoint\x18\x05 \x01(\t\x12.\n\x06inputs\x18\x06 \x03(\x0b2\x1e.sf.substreams.v1.Module.Input\x12/\n\x06output\x18\x07 \x01(\x0b2\x1f.sf.substreams.v1.Module.Output\x12\x15\n\rinitial_block\x18\x08 \x01(\x04\x1a\x1e\n\x07KindMap\x12\x13\n\x0boutput_type\x18\x01 \x01(\t\x1a\xac\x02\n\tKindStore\x12F\n\rupdate_policy\x18\x01 \x01(\x0e2/.sf.substreams.v1.Module.KindStore.UpdatePolicy\x12\x12\n\nvalue_type\x18\x02 \x01(\t"\xc2\x01\n\x0cUpdatePolicy\x12\x17\n\x13UPDATE_POLICY_UNSET\x10\x00\x12\x15\n\x11UPDATE_POLICY_SET\x10\x01\x12#\n\x1fUPDATE_POLICY_SET_IF_NOT_EXISTS\x10\x02\x12\x15\n\x11UPDATE_POLICY_ADD\x10\x03\x12\x15\n\x11UPDATE_POLICY_MIN\x10\x04\x12\x15\n\x11UPDATE_POLICY_MAX\x10\x05\x12\x18\n\x14UPDATE_POLICY_APPEND\x10\x06\x1a\xe6\x02\n\x05Input\x127\n\x06source\x18\x01 \x01(\x0b2%.sf.substreams.v1.Module.Input.SourceH\x00\x121\n\x03map\x18\x02 \x01(\x0b2".sf.substreams.v1.Module.Input.MapH\x00\x125\n\x05store\x18\x03 \x01(\x0b2$.sf.substreams.v1.Module.Input.StoreH\x00\x1a\x16\n\x06Source\x12\x0c\n\x04type\x18\x01 \x01(\t\x1a\x1a\n\x03Map\x12\x13\n\x0bmodule_name\x18\x01 \x01(\t\x1a}\n\x05Store\x12\x13\n\x0bmodule_name\x18\x01 \x01(\t\x127\n\x04mode\x18\x02 \x01(\x0e2).sf.substreams.v1.Module.Input.Store.Mode"&\n\x04Mode\x12\t\n\x05UNSET\x10\x00\x12\x07\n\x03GET\x10\x01\x12\n\n\x06DELTAS\x10\x02B\x07\n\x05input\x1a\x16\n\x06Output\x12\x0c\n\x04type\x18\x01 \x01(\tB\x06\n\x04kindBFZDgithub.com/streamingfast/substreams/pb/sf/substreams/v1;pbsubstreamsb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sf.substreams.v1.modules_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
	DESCRIPTOR._options = None
	DESCRIPTOR._serialized_options = b'ZDgithub.com/streamingfast/substreams/pb/sf/substreams/v1;pbsubstreams'
	_MODULES._serialized_start = 52
	_MODULES._serialized_end = 148
	_BINARY._serialized_start = 150
	_BINARY._serialized_end = 189
	_MODULE._serialized_start = 192
	_MODULE._serialized_end = 1223
	_MODULE_KINDMAP._serialized_start = 497
	_MODULE_KINDMAP._serialized_end = 527
	_MODULE_KINDSTORE._serialized_start = 530
	_MODULE_KINDSTORE._serialized_end = 830
	_MODULE_KINDSTORE_UPDATEPOLICY._serialized_start = 636
	_MODULE_KINDSTORE_UPDATEPOLICY._serialized_end = 830
	_MODULE_INPUT._serialized_start = 833
	_MODULE_INPUT._serialized_end = 1191
	_MODULE_INPUT_SOURCE._serialized_start = 1005
	_MODULE_INPUT_SOURCE._serialized_end = 1027
	_MODULE_INPUT_MAP._serialized_start = 1029
	_MODULE_INPUT_MAP._serialized_end = 1055
	_MODULE_INPUT_STORE._serialized_start = 1057
	_MODULE_INPUT_STORE._serialized_end = 1182
	_MODULE_INPUT_STORE_MODE._serialized_start = 1144
	_MODULE_INPUT_STORE_MODE._serialized_end = 1182
	_MODULE_OUTPUT._serialized_start = 1193
	_MODULE_OUTPUT._serialized_end = 1215