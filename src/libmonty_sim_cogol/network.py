#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import logging
import socket
from typing import Generator


def tcp_send(
    ip_address: str = '127.0.0.1',
    port: int = 9000
) -> Generator:

    with socket.create_connection((ip_address, port)) as tcp_socket:

        while True:
            data = (yield)

            if data is None:
                break

            tcp_socket.sendall(data)

        logging.info("Closing socket")
