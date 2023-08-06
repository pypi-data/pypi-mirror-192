"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1csf/solana/type/v1/type.proto\x12\x11sf.solana.type.v1"\xb0\x02\n\x05Block\x12\x1a\n\x12previous_blockhash\x18\x01 \x01(\t\x12\x11\n\tblockhash\x18\x02 \x01(\t\x12\x13\n\x0bparent_slot\x18\x03 \x01(\x04\x12=\n\x0ctransactions\x18\x04 \x03(\x0b2\'.sf.solana.type.v1.ConfirmedTransaction\x12*\n\x07rewards\x18\x05 \x03(\x0b2\x19.sf.solana.type.v1.Reward\x124\n\nblock_time\x18\x06 \x01(\x0b2 .sf.solana.type.v1.UnixTimestamp\x124\n\x0cblock_height\x18\x07 \x01(\x0b2\x1e.sf.solana.type.v1.BlockHeight\x12\x0c\n\x04slot\x18\x14 \x01(\x04"\x83\x01\n\x14ConfirmedTransaction\x123\n\x0btransaction\x18\x01 \x01(\x0b2\x1e.sf.solana.type.v1.Transaction\x126\n\x04meta\x18\x02 \x01(\x0b2(.sf.solana.type.v1.TransactionStatusMeta"N\n\x0bTransaction\x12\x12\n\nsignatures\x18\x01 \x03(\x0c\x12+\n\x07message\x18\x02 \x01(\x0b2\x1a.sf.solana.type.v1.Message"\x89\x02\n\x07Message\x120\n\x06header\x18\x01 \x01(\x0b2 .sf.solana.type.v1.MessageHeader\x12\x14\n\x0caccount_keys\x18\x02 \x03(\x0c\x12\x18\n\x10recent_blockhash\x18\x03 \x01(\x0c\x12<\n\x0cinstructions\x18\x04 \x03(\x0b2&.sf.solana.type.v1.CompiledInstruction\x12\x11\n\tversioned\x18\x05 \x01(\x08\x12K\n\x15address_table_lookups\x18\x06 \x03(\x0b2,.sf.solana.type.v1.MessageAddressTableLookup"~\n\rMessageHeader\x12\x1f\n\x17num_required_signatures\x18\x01 \x01(\r\x12$\n\x1cnum_readonly_signed_accounts\x18\x02 \x01(\r\x12&\n\x1enum_readonly_unsigned_accounts\x18\x03 \x01(\r"d\n\x19MessageAddressTableLookup\x12\x13\n\x0baccount_key\x18\x01 \x01(\x0c\x12\x18\n\x10writable_indexes\x18\x02 \x01(\x0c\x12\x18\n\x10readonly_indexes\x18\x03 \x01(\x0c"\x92\x05\n\x15TransactionStatusMeta\x120\n\x03err\x18\x01 \x01(\x0b2#.sf.solana.type.v1.TransactionError\x12\x0b\n\x03fee\x18\x02 \x01(\x04\x12\x14\n\x0cpre_balances\x18\x03 \x03(\x04\x12\x15\n\rpost_balances\x18\x04 \x03(\x04\x12@\n\x12inner_instructions\x18\x05 \x03(\x0b2$.sf.solana.type.v1.InnerInstructions\x12\x1f\n\x17inner_instructions_none\x18\n \x01(\x08\x12\x14\n\x0clog_messages\x18\x06 \x03(\t\x12\x19\n\x11log_messages_none\x18\x0b \x01(\x08\x12;\n\x12pre_token_balances\x18\x07 \x03(\x0b2\x1f.sf.solana.type.v1.TokenBalance\x12<\n\x13post_token_balances\x18\x08 \x03(\x0b2\x1f.sf.solana.type.v1.TokenBalance\x12*\n\x07rewards\x18\t \x03(\x0b2\x19.sf.solana.type.v1.Reward\x12!\n\x19loaded_writable_addresses\x18\x0c \x03(\x0c\x12!\n\x19loaded_readonly_addresses\x18\r \x03(\x0c\x122\n\x0breturn_data\x18\x0e \x01(\x0b2\x1d.sf.solana.type.v1.ReturnData\x12\x18\n\x10return_data_none\x18\x0f \x01(\x08\x12#\n\x16compute_units_consumed\x18\x10 \x01(\x04H\x00\x88\x01\x01B\x19\n\x17_compute_units_consumed"\x1f\n\x10TransactionError\x12\x0b\n\x03err\x18\x01 \x01(\x0c"`\n\x11InnerInstructions\x12\r\n\x05index\x18\x01 \x01(\r\x12<\n\x0cinstructions\x18\x02 \x03(\x0b2&.sf.solana.type.v1.CompiledInstruction"O\n\x13CompiledInstruction\x12\x18\n\x10program_id_index\x18\x01 \x01(\r\x12\x10\n\x08accounts\x18\x02 \x01(\x0c\x12\x0c\n\x04data\x18\x03 \x01(\x0c"\x91\x01\n\x0cTokenBalance\x12\x15\n\raccount_index\x18\x01 \x01(\r\x12\x0c\n\x04mint\x18\x02 \x01(\t\x129\n\x0fui_token_amount\x18\x03 \x01(\x0b2 .sf.solana.type.v1.UiTokenAmount\x12\r\n\x05owner\x18\x04 \x01(\t\x12\x12\n\nprogram_id\x18\x05 \x01(\t"^\n\rUiTokenAmount\x12\x11\n\tui_amount\x18\x01 \x01(\x01\x12\x10\n\x08decimals\x18\x02 \x01(\r\x12\x0e\n\x06amount\x18\x03 \x01(\t\x12\x18\n\x10ui_amount_string\x18\x04 \x01(\t".\n\nReturnData\x12\x12\n\nprogram_id\x18\x01 \x01(\x0c\x12\x0c\n\x04data\x18\x02 \x01(\x0c"\x88\x01\n\x06Reward\x12\x0e\n\x06pubkey\x18\x01 \x01(\t\x12\x10\n\x08lamports\x18\x02 \x01(\x03\x12\x14\n\x0cpost_balance\x18\x03 \x01(\x04\x122\n\x0breward_type\x18\x04 \x01(\x0e2\x1d.sf.solana.type.v1.RewardType\x12\x12\n\ncommission\x18\x05 \x01(\t"5\n\x07Rewards\x12*\n\x07rewards\x18\x01 \x03(\x0b2\x19.sf.solana.type.v1.Reward""\n\rUnixTimestamp\x12\x11\n\ttimestamp\x18\x01 \x01(\x03"#\n\x0bBlockHeight\x12\x14\n\x0cblock_height\x18\x01 \x01(\x04*I\n\nRewardType\x12\x0f\n\x0bUnspecified\x10\x00\x12\x07\n\x03Fee\x10\x01\x12\x08\n\x04Rent\x10\x02\x12\x0b\n\x07Staking\x10\x03\x12\n\n\x06Voting\x10\x04BKZIgithub.com/streamingfast/firehose-solana/types/pb/sf/solana/type/v1;pbsolb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sf.solana.type.v1.type_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
	DESCRIPTOR._options = None
	DESCRIPTOR._serialized_options = b'ZIgithub.com/streamingfast/firehose-solana/types/pb/sf/solana/type/v1;pbsol'
	_REWARDTYPE._serialized_start = 2502
	_REWARDTYPE._serialized_end = 2575
	_BLOCK._serialized_start = 52
	_BLOCK._serialized_end = 356
	_CONFIRMEDTRANSACTION._serialized_start = 359
	_CONFIRMEDTRANSACTION._serialized_end = 490
	_TRANSACTION._serialized_start = 492
	_TRANSACTION._serialized_end = 570
	_MESSAGE._serialized_start = 573
	_MESSAGE._serialized_end = 838
	_MESSAGEHEADER._serialized_start = 840
	_MESSAGEHEADER._serialized_end = 966
	_MESSAGEADDRESSTABLELOOKUP._serialized_start = 968
	_MESSAGEADDRESSTABLELOOKUP._serialized_end = 1068
	_TRANSACTIONSTATUSMETA._serialized_start = 1071
	_TRANSACTIONSTATUSMETA._serialized_end = 1729
	_TRANSACTIONERROR._serialized_start = 1731
	_TRANSACTIONERROR._serialized_end = 1762
	_INNERINSTRUCTIONS._serialized_start = 1764
	_INNERINSTRUCTIONS._serialized_end = 1860
	_COMPILEDINSTRUCTION._serialized_start = 1862
	_COMPILEDINSTRUCTION._serialized_end = 1941
	_TOKENBALANCE._serialized_start = 1944
	_TOKENBALANCE._serialized_end = 2089
	_UITOKENAMOUNT._serialized_start = 2091
	_UITOKENAMOUNT._serialized_end = 2185
	_RETURNDATA._serialized_start = 2187
	_RETURNDATA._serialized_end = 2233
	_REWARD._serialized_start = 2236
	_REWARD._serialized_end = 2372
	_REWARDS._serialized_start = 2374
	_REWARDS._serialized_end = 2427
	_UNIXTIMESTAMP._serialized_start = 2429
	_UNIXTIMESTAMP._serialized_end = 2463
	_BLOCKHEIGHT._serialized_start = 2465
	_BLOCKHEIGHT._serialized_end = 2500