"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1csf/solana/type/v2/type.proto\x12\x11sf.solana.type.v2"\xce\x02\n\x05Block\x12\n\n\x02id\x18\x01 \x01(\x0c\x12\x0e\n\x06number\x18\x02 \x01(\x04\x12\x0f\n\x07version\x18\x03 \x01(\r\x12\x13\n\x0bprevious_id\x18\x04 \x01(\x0c\x12\x16\n\x0eprevious_block\x18\x05 \x01(\x04\x12\x1e\n\x16genesis_unix_timestamp\x18\x06 \x01(\x04\x12\x1c\n\x14clock_unix_timestamp\x18\x07 \x01(\x04\x12\x17\n\x0flast_entry_hash\x18\x08 \x01(\x0c\x124\n\x0ctransactions\x18\t \x03(\x0b2\x1e.sf.solana.type.v2.Transaction\x12\x19\n\x11transaction_count\x18\n \x01(\r\x12!\n\x19has_split_account_changes\x18\x0b \x01(\x08\x12 \n\x18account_changes_file_ref\x18\x0c \x01(\t"=\n\x05Batch\x124\n\x0ctransactions\x18\x01 \x03(\x0b2\x1e.sf.solana.type.v2.Transaction"\xcf\x02\n\x0bTransaction\x12\n\n\x02id\x18\x01 \x01(\x0c\x12\r\n\x05index\x18\x02 \x01(\x04\x12\x1d\n\x15additional_signatures\x18\x03 \x03(\x0c\x120\n\x06header\x18\x04 \x01(\x0b2 .sf.solana.type.v2.MessageHeader\x12\x14\n\x0caccount_keys\x18\x05 \x03(\x0c\x12\x18\n\x10recent_blockhash\x18\x06 \x01(\x0c\x124\n\x0cinstructions\x18\x07 \x03(\x0b2\x1e.sf.solana.type.v2.Instruction\x12\x0e\n\x06failed\x18\x08 \x01(\x08\x122\n\x05error\x18\t \x01(\x0b2#.sf.solana.type.v2.TransactionError\x12\x15\n\rbegin_ordinal\x18\n \x01(\x04\x12\x13\n\x0bend_ordinal\x18\x0b \x01(\x04"~\n\rMessageHeader\x12\x1f\n\x17num_required_signatures\x18\x01 \x01(\r\x12$\n\x1cnum_readonly_signed_accounts\x18\x02 \x01(\r\x12&\n\x1enum_readonly_unsigned_accounts\x18\x03 \x01(\r"\x85\x03\n\x0bInstruction\x12\x12\n\nprogram_id\x18\x03 \x01(\x0c\x12\x14\n\x0caccount_keys\x18\x04 \x03(\x0c\x12\x0c\n\x04data\x18\x05 \x01(\x0c\x12\r\n\x05index\x18\x06 \x01(\r\x12\x14\n\x0cparent_index\x18\x07 \x01(\r\x12\r\n\x05depth\x18\x08 \x01(\r\x129\n\x0fbalance_changes\x18\t \x03(\x0b2 .sf.solana.type.v2.BalanceChange\x129\n\x0faccount_changes\x18\n \x03(\x0b2 .sf.solana.type.v2.AccountChange\x12$\n\x04logs\x18\x0b \x03(\x0b2\x16.sf.solana.type.v2.Log\x12\x0e\n\x06failed\x18\x0f \x01(\x08\x122\n\x05error\x18\x10 \x01(\x0b2#.sf.solana.type.v2.InstructionError\x12\x15\n\rbegin_ordinal\x18\x11 \x01(\x04\x12\x13\n\x0bend_ordinal\x18\x12 \x01(\x04"L\n\rBalanceChange\x12\x0e\n\x06pubkey\x18\x01 \x01(\x0c\x12\x15\n\rprev_lamports\x18\x02 \x01(\x04\x12\x14\n\x0cnew_lamports\x18\x03 \x01(\x04"]\n\rAccountChange\x12\x0e\n\x06pubkey\x18\x01 \x01(\x0c\x12\x11\n\tprev_data\x18\x02 \x01(\x0c\x12\x10\n\x08new_data\x18\x03 \x01(\x0c\x12\x17\n\x0fnew_data_length\x18\x04 \x01(\x04"\'\n\x03Log\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\x0f\n\x07ordinal\x18\x02 \x01(\x04"!\n\x10TransactionError\x12\r\n\x05error\x18\x02 \x01(\t",\n\x1bTransactionInstructionError\x12\r\n\x05error\x18\x02 \x01(\t"!\n\x10InstructionError\x12\r\n\x05error\x18\x02 \x01(\t"\'\n\x16InstructionErrorCustom\x12\r\n\x05error\x18\x02 \x01(\tBKZIgithub.com/streamingfast/firehose-solana/types/pb/sf/solana/type/v2;pbsolb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sf.solana.type.v2.type_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
	DESCRIPTOR._options = None
	DESCRIPTOR._serialized_options = b'ZIgithub.com/streamingfast/firehose-solana/types/pb/sf/solana/type/v2;pbsol'
	_BLOCK._serialized_start = 52
	_BLOCK._serialized_end = 386
	_BATCH._serialized_start = 388
	_BATCH._serialized_end = 449
	_TRANSACTION._serialized_start = 452
	_TRANSACTION._serialized_end = 787
	_MESSAGEHEADER._serialized_start = 789
	_MESSAGEHEADER._serialized_end = 915
	_INSTRUCTION._serialized_start = 918
	_INSTRUCTION._serialized_end = 1307
	_BALANCECHANGE._serialized_start = 1309
	_BALANCECHANGE._serialized_end = 1385
	_ACCOUNTCHANGE._serialized_start = 1387
	_ACCOUNTCHANGE._serialized_end = 1480
	_LOG._serialized_start = 1482
	_LOG._serialized_end = 1521
	_TRANSACTIONERROR._serialized_start = 1523
	_TRANSACTIONERROR._serialized_end = 1556
	_TRANSACTIONINSTRUCTIONERROR._serialized_start = 1558
	_TRANSACTIONINSTRUCTIONERROR._serialized_end = 1602
	_INSTRUCTIONERROR._serialized_start = 1604
	_INSTRUCTIONERROR._serialized_end = 1637
	_INSTRUCTIONERRORCUSTOM._serialized_start = 1639
	_INSTRUCTIONERRORCUSTOM._serialized_end = 1678