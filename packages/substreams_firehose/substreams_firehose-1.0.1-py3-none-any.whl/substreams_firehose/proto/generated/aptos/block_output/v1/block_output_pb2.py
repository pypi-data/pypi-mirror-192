"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....aptos.util.timestamp import timestamp_pb2 as aptos_dot_util_dot_timestamp_dot_timestamp__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n(aptos/block_output/v1/block_output.proto\x12\x15aptos.block_output.v1\x1a$aptos/util/timestamp/timestamp.proto"o\n\x0bBlockOutput\x12\x0e\n\x06height\x18\x01 \x01(\x04\x12>\n\x0ctransactions\x18\x02 \x03(\x0b2(.aptos.block_output.v1.TransactionOutput\x12\x10\n\x08chain_id\x18\x03 \x01(\r"\xbd\x03\n\x11TransactionOutput\x12M\n\x17transaction_info_output\x18\x01 \x01(\x0b2,.aptos.block_output.v1.TransactionInfoOutput\x12O\n\x0eblock_metadata\x18\x02 \x01(\x0b25.aptos.block_output.v1.BlockMetadataTransactionOutputH\x00\x12<\n\x04user\x18\x03 \x01(\x0b2,.aptos.block_output.v1.UserTransactionOutputH\x00\x12B\n\x07genesis\x18\x04 \x01(\x0b2/.aptos.block_output.v1.GenesisTransactionOutputH\x00\x122\n\x06events\x18\x05 \x03(\x0b2".aptos.block_output.v1.EventOutput\x12F\n\x11write_set_changes\x18\x06 \x03(\x0b2+.aptos.block_output.v1.WriteSetChangeOutputB\n\n\x08txn_data"\xe4\x02\n\x15TransactionInfoOutput\x12\x0c\n\x04hash\x18\x01 \x01(\x0c\x12\x0c\n\x04type\x18\x02 \x01(\t\x12\x0f\n\x07version\x18\x03 \x01(\x04\x12\x19\n\x11state_change_hash\x18\x04 \x01(\x0c\x12\x17\n\x0fevent_root_hash\x18\x05 \x01(\x0c\x12"\n\x15state_checkpoint_hash\x18\r \x01(\x0cH\x00\x88\x01\x01\x12\x10\n\x08gas_used\x18\x06 \x01(\x04\x12\x0f\n\x07success\x18\x07 \x01(\x08\x12\r\n\x05epoch\x18\x08 \x01(\x04\x12\x14\n\x0cblock_height\x18\t \x01(\x04\x12\x11\n\tvm_status\x18\n \x01(\t\x12\x1d\n\x15accumulator_root_hash\x18\x0b \x01(\x0c\x122\n\ttimestamp\x18\x0c \x01(\x0b2\x1f.aptos.util.timestamp.TimestampB\x18\n\x16_state_checkpoint_hash"\xe7\x01\n\x1eBlockMetadataTransactionOutput\x12\x0f\n\x07version\x18\x01 \x01(\x04\x12\n\n\x02id\x18\x02 \x01(\t\x12\r\n\x05round\x18\x03 \x01(\x04\x12#\n\x1bprevious_block_votes_bitvec\x18\x04 \x01(\x0c\x12\x10\n\x08proposer\x18\x05 \x01(\t\x12\x1f\n\x17failed_proposer_indices\x18\x06 \x03(\r\x122\n\ttimestamp\x18\x07 \x01(\x0b2\x1f.aptos.util.timestamp.Timestamp\x12\r\n\x05epoch\x18\x08 \x01(\x04"\x84\x03\n\x15UserTransactionOutput\x12\x0f\n\x07version\x18\x01 \x01(\x04\x12\x1d\n\x15parent_signature_type\x18\x02 \x01(\t\x12\x0e\n\x06sender\x18\x03 \x01(\t\x12\x17\n\x0fsequence_number\x18\x04 \x01(\x04\x12\x16\n\x0emax_gas_amount\x18\x05 \x01(\x04\x12B\n\x19expiration_timestamp_secs\x18\x06 \x01(\x0b2\x1f.aptos.util.timestamp.Timestamp\x12\x16\n\x0egas_unit_price\x18\x07 \x01(\x04\x122\n\ttimestamp\x18\x08 \x01(\x0b2\x1f.aptos.util.timestamp.Timestamp\x12:\n\nsignatures\x18\t \x03(\x0b2&.aptos.block_output.v1.SignatureOutput\x12\x0f\n\x07payload\x18\n \x01(\t\x12\x1d\n\x15entry_function_id_str\x18\x0b \x01(\t"+\n\x18GenesisTransactionOutput\x12\x0f\n\x07payload\x18\x01 \x01(\t"\xef\x01\n\x0fSignatureOutput\x12\x0f\n\x07version\x18\x01 \x01(\x04\x12\x0e\n\x06signer\x18\x02 \x01(\t\x12\x19\n\x11is_sender_primary\x18\x03 \x01(\x08\x12\x16\n\x0esignature_type\x18\x04 \x01(\t\x12\x12\n\npublic_key\x18\x05 \x01(\x0c\x12\x11\n\tsignature\x18\x06 \x01(\x0c\x12\x11\n\tthreshold\x18\x07 \x01(\r\x12\x1a\n\x12public_key_indices\x18\x08 \x03(\r\x12\x19\n\x11multi_agent_index\x18\t \x01(\r\x12\x17\n\x0fmulti_sig_index\x18\n \x01(\r"\x99\x01\n\x0bEventOutput\x12\x0f\n\x07version\x18\x01 \x01(\x04\x122\n\x03key\x18\x02 \x01(\x0b2%.aptos.block_output.v1.EventKeyOutput\x12\x17\n\x0fsequence_number\x18\x03 \x01(\x04\x12\x0c\n\x04type\x18\x04 \x01(\t\x12\x10\n\x08type_str\x18\x05 \x01(\t\x12\x0c\n\x04data\x18\x06 \x01(\t"B\n\x0eEventKeyOutput\x12\x17\n\x0fcreation_number\x18\x01 \x01(\x04\x12\x17\n\x0faccount_address\x18\x02 \x01(\t"\x8f\x02\n\x14WriteSetChangeOutput\x12\x0f\n\x07version\x18\x01 \x01(\x04\x12\x0c\n\x04hash\x18\x02 \x01(\x0c\x12\x0c\n\x04type\x18\x03 \x01(\t\x12>\n\x0bmove_module\x18\x04 \x01(\x0b2\'.aptos.block_output.v1.MoveModuleOutputH\x00\x12B\n\rmove_resource\x18\x05 \x01(\x0b2).aptos.block_output.v1.MoveResourceOutputH\x00\x12<\n\ntable_item\x18\x06 \x01(\x0b2&.aptos.block_output.v1.TableItemOutputH\x00B\x08\n\x06change"\xa7\x01\n\x10MoveModuleOutput\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07address\x18\x02 \x01(\t\x12\x10\n\x08bytecode\x18\x03 \x01(\x0c\x12\x0f\n\x07friends\x18\x04 \x03(\t\x12\x19\n\x11exposed_functions\x18\x05 \x03(\t\x12\x0f\n\x07structs\x18\x06 \x03(\t\x12\x12\n\nis_deleted\x18\x07 \x01(\x08\x12\x11\n\twsc_index\x18\x08 \x01(\x04"\xa7\x01\n\x12MoveResourceOutput\x12\x0f\n\x07address\x18\x01 \x01(\t\x12\x0e\n\x06module\x18\x02 \x01(\t\x12\x10\n\x08type_str\x18\x03 \x01(\t\x12\x0c\n\x04name\x18\x04 \x01(\t\x12\x1b\n\x13generic_type_params\x18\x05 \x03(\t\x12\x0c\n\x04data\x18\x06 \x01(\t\x12\x12\n\nis_deleted\x18\x07 \x01(\x08\x12\x11\n\twsc_index\x18\x08 \x01(\x04"\xa7\x01\n\x0fTableItemOutput\x12\x0e\n\x06handle\x18\x01 \x01(\t\x12\x0b\n\x03key\x18\x02 \x01(\t\x12\x13\n\x0bdecoded_key\x18\x03 \x01(\t\x12\x10\n\x08key_type\x18\x04 \x01(\t\x12\x15\n\rdecoded_value\x18\x05 \x01(\t\x12\x12\n\nvalue_type\x18\x06 \x01(\t\x12\x12\n\nis_deleted\x18\x07 \x01(\x08\x12\x11\n\twsc_index\x18\x08 \x01(\x04BPZNgithub.com/streamingfast/firehose-aptos/types/pb/aptos/block_output/v1;pbaptosb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'aptos.block_output.v1.block_output_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
	DESCRIPTOR._options = None
	DESCRIPTOR._serialized_options = b'ZNgithub.com/streamingfast/firehose-aptos/types/pb/aptos/block_output/v1;pbaptos'
	_BLOCKOUTPUT._serialized_start = 105
	_BLOCKOUTPUT._serialized_end = 216
	_TRANSACTIONOUTPUT._serialized_start = 219
	_TRANSACTIONOUTPUT._serialized_end = 664
	_TRANSACTIONINFOOUTPUT._serialized_start = 667
	_TRANSACTIONINFOOUTPUT._serialized_end = 1023
	_BLOCKMETADATATRANSACTIONOUTPUT._serialized_start = 1026
	_BLOCKMETADATATRANSACTIONOUTPUT._serialized_end = 1257
	_USERTRANSACTIONOUTPUT._serialized_start = 1260
	_USERTRANSACTIONOUTPUT._serialized_end = 1648
	_GENESISTRANSACTIONOUTPUT._serialized_start = 1650
	_GENESISTRANSACTIONOUTPUT._serialized_end = 1693
	_SIGNATUREOUTPUT._serialized_start = 1696
	_SIGNATUREOUTPUT._serialized_end = 1935
	_EVENTOUTPUT._serialized_start = 1938
	_EVENTOUTPUT._serialized_end = 2091
	_EVENTKEYOUTPUT._serialized_start = 2093
	_EVENTKEYOUTPUT._serialized_end = 2159
	_WRITESETCHANGEOUTPUT._serialized_start = 2162
	_WRITESETCHANGEOUTPUT._serialized_end = 2433
	_MOVEMODULEOUTPUT._serialized_start = 2436
	_MOVEMODULEOUTPUT._serialized_end = 2603
	_MOVERESOURCEOUTPUT._serialized_start = 2606
	_MOVERESOURCEOUTPUT._serialized_end = 2773
	_TABLEITEMOUTPUT._serialized_start = 2776
	_TABLEITEMOUTPUT._serialized_end = 2943