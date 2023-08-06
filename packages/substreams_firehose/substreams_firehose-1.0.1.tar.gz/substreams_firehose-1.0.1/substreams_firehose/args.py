"""
SPDX-License-Identifier: MIT

Argument parsing and checking for the main script.
"""

import argparse

def check_period(arg_period: str) -> int:
	"""
	Convert the specified period argument from an integer to a block number.

	Args:
		arg_period: A period argument from the ArgumentParser.

	Returns:
		An integer representing the corresponding block number.

	Raises:
		ArgumentTypeError: If the period cannot be parsed.
	"""
	try:
		arg_period = int(arg_period)
	except ValueError:
		# TODO: Add date parsing
		arg_period = -1

	if arg_period < 0:
		raise argparse.ArgumentTypeError(f'Invalid period: {arg_period} must be positive `int` or `datetime`-like object')

	return arg_period

def parse_arguments() -> argparse.Namespace:
	"""
	Setup the command line interface and return the parsed arguments.

	Returns:
		A `Namespace` object containing the parsed arguments.
	"""
	arg_parser = argparse.ArgumentParser(
		description=('Extract any data from the blockchain using gRPC-enabled endpoints.'
					 'Powered by Firehose (https://firehose.streamingfast.io/) and Substreams (https://substreams.streamingfast.io).'),
		formatter_class=argparse.ArgumentDefaultsHelpFormatter,
	)
	arg_parser.add_argument('start', type=str,
							help='starting block number')
	arg_parser.add_argument('end', type=str,
							help='ending block number')
	arg_parser.add_argument('-c', '--config', type=str, default='substreams_firehose/config.hjson',
							help='config file path in HJSON or JSON format')
	arg_parser.add_argument('-s', '--stub', type=str,
							help='stub config file path in HJSON or JSON format')
	arg_parser.add_argument('-o', '--out-file', type=str, default='jsonl/{chain}_{start}_to_{end}.jsonl',
							help='output file path')
	arg_parser.add_argument('-l', '--log', nargs='?', type=str, const=None, default='logs/{datetime}.log',
							help='log debug information to log file (can specify the full path)')
	arg_parser.add_argument('-q', '--quiet', action='store_true',
							help='disable console logging')
	arg_parser.add_argument('-g', '--grpc-entry', type=str,
							help='id of a grpc entry in the "grpc" array found in the main config file')
	arg_parser.add_argument('-e', '--extractor', choices=['optimized', 'single', 'multi'], default='optimized',
							help='type of extractor used for streaming blocks from the gRPC endpoint')
	arg_parser.add_argument('-p', '--custom-processor', type=str, default='default_processor',
							help='name of a custom block processing function located in the "block_processors.processors" module')
	arg_parser.add_argument('--no-json-output', action='store_true',
							help='don\'t try to convert block processor output to JSON')
	arg_parser.add_argument('--overwrite-log', action='store_true',
							help='overwrite log file, erasing its content (default is to append)')
	arg_parser.add_argument('--request-parameters', nargs=argparse.REMAINDER,
							help='optional keyword arguments (key=val) sent with the gRPC request (must match .proto definition, \
							will override any parameters set in the config)')

	return arg_parser.parse_args()
