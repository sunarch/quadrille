#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# imports: library
from argparse import ArgumentParser
import time

# imports: dependencies
from libmonty_logging.config.file_and_stream.v1 import config as logging_config
import libmonty_logging.helper as logging_helper
import libmonty_logging.message as logging_message

# imports: project
from quadrille import version
from quadrille import cogol, network
from quadrille.cogol import Grid


def main() -> None:

    logging_helper.apply_config(version.PROGRAM_NAME,
                                version.__version__,
                                logging_config)

    logging_message.program_header(version.PROGRAM_NAME)

    parser = ArgumentParser(prog=version.PROGRAM_NAME)

    parser.add_argument('--version',
                        help='Display version',
                        action='store_true',
                        dest='version')

    parser.add_argument('--grid-height',
                        help='Height of the grid',
                        action='store', type=int, required=True,
                        dest='grid_height')

    parser.add_argument('--grid-width',
                        help='Width of the grid',
                        action='store', type=int, required=True,
                        dest='grid_width')

    parser.add_argument('--loopback',
                        help='Connect the opposite edges',
                        action='store_true',
                        dest='loopback')

    parser.add_argument('--add-glider',
                        help='Add a glider to the initial state',
                        action='store_true',
                        dest='add_glider')

    parser.add_argument('--send-over-network', metavar='ADDR:PORT',
                        help='Send data over the network to "address:port"',
                        default=None,
                        dest='network_address')

    args = parser.parse_args()

    if args.version:
        print(f'{version.PROGRAM_NAME} {version.__version__}')
        return

    grid = Grid(height=args.grid_height, width=args.grid_width, is_loopback=args.loopback)

    if args.add_glider:
        grid.add_glider(1, 1)

    network_iterator = None
    if args.network_address is not None:
        network_iterator = network.tcp_send(*args.network_address.split(':'))
        next(network_iterator)

    while True:
        try:
            cogol.print_grid(grid)

            if network_iterator is not None:
                network_iterator.send(cogol.grid_to_color_bytes(grid))

            grid.advance()

            if grid.is_empty:
                network_iterator.send(b'\x00')
                network_iterator.send(None)
                break
            else:
                time.sleep(0.5)
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    main()
