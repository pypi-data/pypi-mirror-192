"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1captos/tokens/v1/tokens.proto\x12\x0faptos.tokens.v1"\xc4\x01\n\x06Tokens\x12\x14\n\x0cblock_height\x18\x01 \x01(\x04\x12\x10\n\x08chain_id\x18\x02 \x01(\r\x12&\n\x06tokens\x18\x03 \x03(\x0b2\x16.aptos.tokens.v1.Token\x12/\n\x0btoken_datas\x18\x04 \x03(\x0b2\x1a.aptos.tokens.v1.TokenData\x129\n\x10collection_datas\x18\x05 \x03(\x0b2\x1f.aptos.tokens.v1.CollectionData"\xe6\x01\n\x05Token\x12*\n\x08token_id\x18\x01 \x01(\x0b2\x18.aptos.tokens.v1.TokenId\x12\x1b\n\x13transaction_version\x18\x02 \x01(\x04\x12\x18\n\x10token_properties\x18\x03 \x01(\t\x12\x0e\n\x06amount\x18\x04 \x01(\x04\x12\x1a\n\rowner_address\x18\x05 \x01(\tH\x00\x88\x01\x01\x12\x14\n\x0ctable_handle\x18\x06 \x01(\t\x12\x17\n\ntable_type\x18\x07 \x01(\tH\x01\x88\x01\x01B\x10\n\x0e_owner_addressB\r\n\x0b_table_type"\xaf\x03\n\tTokenData\x123\n\rtoken_data_id\x18\x01 \x01(\x0b2\x1c.aptos.tokens.v1.TokenDataId\x12\x1b\n\x13transaction_version\x18\x02 \x01(\x04\x12\x0f\n\x07maximum\x18\x03 \x01(\x04\x12\x0e\n\x06supply\x18\x04 \x01(\x04\x12 \n\x18largest_property_version\x18\x05 \x01(\x04\x12\x14\n\x0cmetadata_uri\x18\x06 \x01(\t\x12\x15\n\rpayee_address\x18\x07 \x01(\t\x12 \n\x18royalty_points_numerator\x18\x08 \x01(\x04\x12"\n\x1aroyalty_points_denominator\x18\t \x01(\x04\x12\x17\n\x0fmaximum_mutable\x18\n \x01(\x08\x12\x13\n\x0buri_mutable\x18\x0b \x01(\x08\x12\x1b\n\x13description_mutable\x18\x0c \x01(\x08\x12\x1a\n\x12properties_mutable\x18\r \x01(\x08\x12\x17\n\x0froyalty_mutable\x18\x0e \x01(\x08\x12\x1a\n\x12default_properties\x18\x0f \x01(\t"X\n\x07TokenId\x123\n\rtoken_data_id\x18\x01 \x01(\x0b2\x1c.aptos.tokens.v1.TokenDataId\x12\x18\n\x10property_version\x18\x02 \x01(\x04"M\n\x0bTokenDataId\x12\x17\n\x0fcreator_address\x18\x01 \x01(\t\x12\x17\n\x0fcollection_name\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t"\xf6\x01\n\x0eCollectionData\x12\x17\n\x0fcreator_address\x18\x01 \x01(\t\x12\x17\n\x0fcollection_name\x18\x02 \x01(\t\x12\x13\n\x0bdescription\x18\x03 \x01(\t\x12\x1b\n\x13transaction_version\x18\x04 \x01(\x04\x12\x14\n\x0cmetadata_uri\x18\x05 \x01(\t\x12\x0e\n\x06supply\x18\x06 \x01(\x04\x12\x0f\n\x07maximum\x18\x07 \x01(\x04\x12\x17\n\x0fmaximum_mutable\x18\x08 \x01(\x08\x12\x13\n\x0buri_mutable\x18\t \x01(\x08\x12\x1b\n\x13description_mutable\x18\n \x01(\x08b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'aptos.tokens.v1.tokens_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _TOKENS._serialized_start = 50
    _TOKENS._serialized_end = 246
    _TOKEN._serialized_start = 249
    _TOKEN._serialized_end = 479
    _TOKENDATA._serialized_start = 482
    _TOKENDATA._serialized_end = 913
    _TOKENID._serialized_start = 915
    _TOKENID._serialized_end = 1003
    _TOKENDATAID._serialized_start = 1005
    _TOKENDATAID._serialized_end = 1082
    _COLLECTIONDATA._serialized_start = 1085
    _COLLECTIONDATA._serialized_end = 1331