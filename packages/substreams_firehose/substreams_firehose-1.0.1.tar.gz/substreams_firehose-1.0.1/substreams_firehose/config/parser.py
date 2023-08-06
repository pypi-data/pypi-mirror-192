"""
SPDX-License-Identifier: MIT

Parses the main config and stub config files for use by the application.
Refer to the [`README.md`](../../../README.md) and comments within the config files for more details about each parameters.
"""

import logging
from argparse import ArgumentTypeError
from dataclasses import dataclass
from typing import Any, ClassVar

# https://hjson.github.io/hjson-py/ -- allow comments in JSON files for configuration purposes
import hjson
from google.protobuf.json_format import MessageToJson
from grpc import Compression

from substreams_firehose.utils import generate_proto_messages_classes, open_file_from_package

@dataclass
class StubConfig:
	"""
	Holds the stub configuration.
	"""
	RESPONSE_PARAMETERS: ClassVar[dict | list]
	REQUEST_OBJECT: ClassVar[Any]
	REQUEST_PARAMETERS: ClassVar[dict]
	SERVICE_METHOD_FUNCTION: ClassVar[Any]
	SERVICE_OBJECT: ClassVar[Any]
	SUBSTREAMS_PACKAGE_OBJECT: ClassVar[Any]

@dataclass
class Config:
	"""
	Holds the main configuration.
	"""
	API_KEY: ClassVar[str]
	AUTH_ENDPOINT: ClassVar[str]
	CHAIN: ClassVar[str]
	COMPRESSION: ClassVar[Compression]
	GRPC_ENDPOINT: ClassVar[str]
	MAX_BLOCK_SIZE: ClassVar[int]
	MAX_FAILED_BLOCK_RETRIES: ClassVar[int]
	PROTO_MESSAGES_CLASSES: ClassVar[dict[str, type]]

def load_config(file: str, grpc_entry_id: str | None = None) -> bool:
	"""
	Load the main config from the specified file. If a gRPC entry id is specified, it overwrites the default specified
	in the config.

	Args:
		file: A local path to the main configuration file.
		grpc_entry_id: A string identifier of a gRPC entry present in the "grpc" array of the main configuration file.

	Returns:
		A boolean indicating if the stub configuration file has also been loaded.

	Raises:
		ArgumentTypeError: If an entry is not recognized within the configuration file.
		HjsonDecodeError: If the `hjson` module fails to parse the configuration file.
		ImportError: If the stub configuration file fails to import the specified modules.
		KeyError: If a required key is missing from the configuration file.
	"""
	with open_file_from_package(file, 'r') as config_file:
		try:
			options = hjson.load(config_file)
		except hjson.HjsonDecodeError as error:
			logging.exception('Error decoding main config file (%s): %s', file, error)
			raise

	try:
		if grpc_entry_id:
			options['default'] = grpc_entry_id

		try:
			default_grpc_id = [i for i, entry in enumerate(options['grpc']) if entry['id'] == options['default']][0]
		except IndexError as error:
			logging.exception('Could not find "%s" entry in grpc endpoints array', options['default'])
			raise ArgumentTypeError from error

		default_grpc = options['grpc'][default_grpc_id]
		default_auth = next(iter([o for o in options['auth'] if o['id'] == default_grpc['auth']]))
		if not default_auth:
			logging.exception('Could not find "%s" entry in auth providers array', default_grpc['auth'])
			raise ArgumentTypeError

		default_stub = default_grpc['stub'] if 'stub' in default_grpc else ''

		Config.API_KEY 					= default_auth['api_key']
		Config.AUTH_ENDPOINT 			= default_auth['endpoint']
		Config.CHAIN 					= default_grpc.get('chain', '<UNKNOWN CHAIN>')
		Config.GRPC_ENDPOINT 			= default_grpc['url']
		Config.MAX_BLOCK_SIZE 			= options.get('max_block_size', 8388608) # 8MB default
		Config.MAX_FAILED_BLOCK_RETRIES = options.get('max_failed_block_retries', 3)
	except KeyError as error:
		logging.exception('Error parsing main config file (%s): %s', file, error)
		raise

	try:
		compression_option = default_grpc['compression'].lower()
		if compression_option in ['gzip', 'deflate']:
			Config.COMPRESSION = Compression.Gzip if compression_option == 'gzip' else Compression.Deflate
		else:
			logging.exception('Unrecognized compression option: "%s" not one of "gzip" or "deflate"', compression_option)
			raise ArgumentTypeError
	except KeyError as error:
		Config.COMPRESSION = Compression.NoCompression

	Config.PROTO_MESSAGES_CLASSES = generate_proto_messages_classes()

	if default_stub:
		load_stub_config(default_stub)
	else:
		return False

	return True

def load_substream_package(url: str) -> dict:
	"""
	Parse a substream package from an `.spkg` file.

	Args:
		url: A local path to `.spkg` file.

	Returns:
		A dictionary containing fields available in the package file.

	Raises:
		google.protobuf.message.DecodeError: If the Google protobuf library cannot parse the file.
		FileNotFoundError: If the file specified by `url` doesn't exists.
		IsADirectoryError: If the file specified by `url` is a directory.
	"""
	with open_file_from_package(url, 'rb') as package_file:
		pkg = StubConfig.SUBSTREAMS_PACKAGE_OBJECT()
		pkg.ParseFromString(package_file.read())

	return hjson.loads(MessageToJson(pkg))

def load_stub_config(stub: str | dict) -> None:
	"""
	Load the stub config from a file (str) or directly from a key-value dictionary.

	Args:
		stub: The stub to load either as a local path or a dictionary.

	Raises:
		HjsonDecodeError: If the `hjson` module fails to parse the configuration file.
		ImportError: If the specified stub or request object cannot be imported.
		KeyError: If a required key is missing from the configuration file.
	"""
	stub_config = stub
	# Load stub config from external file
	if isinstance(stub, str):
		with open_file_from_package(stub, 'r') as stub_config_file:
			try:
				stub_config = hjson.load(stub_config_file)
			except hjson.HjsonDecodeError as error:
				logging.exception('Error decoding stub config file (%s): %s', stub, error)
				raise

	try:
		try:
			StubConfig.REQUEST_OBJECT = Config.PROTO_MESSAGES_CLASSES[f'{stub_config["base"]}.{stub_config["request"]["object"]}']
		except KeyError as error:
			logging.exception('Could not load request object from config: unable to locate "%s" in "%s" module',
				stub_config['request']['object'],
				stub_config['base']
			)
			raise ImportError from error

		StubConfig.SERVICE_METHOD_FUNCTION = stub_config['method']
		try:
			StubConfig.SERVICE_OBJECT = Config.PROTO_MESSAGES_CLASSES[f'{stub_config["base"]}.{stub_config["service"]}']
		except KeyError as error:
			logging.exception('Could not load service object from config: unable to locate "%s" in "%s" module',
				stub_config['service'],
				stub_config['base']
			)
			raise ImportError from error

		# If is using substreams load the package object used to decode package files
		if 'modules' in stub_config['request']['params'] and '.spkg' in stub_config['request']['params']['modules']:
			try:
				StubConfig.SUBSTREAMS_PACKAGE_OBJECT = Config.PROTO_MESSAGES_CLASSES[
					f'{stub_config["base"]}.Package'
				]
			except KeyError as error:
				logging.exception('Error loading stub config SUBSTREAMS_PACKAGE_OBJECT: message class "%s" not found',
					f'{stub_config["base"]}.Package'
				)
				raise ImportError from error

			stub_config['request']['params']['modules'] = load_substream_package(
				stub_config['request']['params']['modules']
			)['modules']
		else:
			StubConfig.SUBSTREAMS_PACKAGE_OBJECT = None

		StubConfig.REQUEST_PARAMETERS = stub_config['request']['params']
		StubConfig.RESPONSE_PARAMETERS = stub_config['response']['params']

	except ImportError as error:
		logging.exception('Error importing modules from specified directory (%s): %s',
			stub_config['base'],
			error
		)
		raise
	except KeyError as error:
		logging.exception('Error parsing stub config (%s): %s', stub_config, error)
		raise
