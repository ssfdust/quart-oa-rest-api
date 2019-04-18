import os
import time
import sys
from typing import Any
from colored import fg, bg, attr

from loguru import logger


class AccessLogger:
    def __init__(self, log_format: str, target) -> None:
        logger.start(sys.stdout, colorize=True,
                     format="<green>{time:YY-MM-DD HH:mm:ss}</green> | {message}",
                     filter='extensions.colored_quart.logging')
        # logger.add(sys.stderr, format="{time} {message}")
        self.logger = logger
        self.log_format = log_format

    def access(self, request: dict, response: dict, request_time: float) -> None:
        if self.logger is not None:
            self.logger.info(self.log_format,
                             **AccessLogAtoms(request, response, request_time))

    def __getattr__(self, name: str) -> Any:
        if self.logger is None:
            return lambda *_: None
        else:
            return getattr(self.logger, name)


class AccessLogAtoms(dict):
    def __init__(self, request: dict, response: dict, request_time: float) -> None:
        for name, value in request["headers"]:
            self[f"{{{name.decode().lower()}}}i"] = value.decode()
        for name, value in response["headers"]:
            self[f"{{{name.decode().lower()}}}o"] = value.decode()
        for name, value in os.environ.items():
            self[f"{{{name.lower()}}}e"] = value
        protocol = request.get("http_version", "ws")
        client = request.get("client")
        if client is None:
            remote_addr = None
        elif len(client) == 2:
            remote_addr = f"{client[0]}:{client[1]}"
        elif len(client) == 1:
            remote_addr = client[0]
        else:  # make sure not to throw UnboundLocalError
            remote_addr = f"<???{client}???>"
        method = request.get("method", "GET")
        if method == 'POST':
            method = fg('white') + bg(70) + ' POST ' + attr(0)
        elif method == 'GET':
            method = fg('white') + bg(33) + ' GET ' + attr(0)
        elif method == 'DELETE':
            method = fg('white') + bg(196) + ' DELETE ' + attr(0)
        if response["status"] == 200:
            statusColor = fg(76) + attr(1)
        elif str(response["status"])[0] in ['4', '5']:
            statusColor = fg('red') + attr(1)
        else:
            statusColor = fg('light_gray') + attr(1)
        colored_status = "{statusColor}{status}{colorEnd}"\
            .format(statusColor=statusColor,
                    status=response["status"],
                    colorEnd=attr(0))
        colored_path = "{}{}{}".format(fg('light_gray'),
                                       request['path'],
                                       attr(0))
        request['path'] = colored_path
        remote_addr = fg(108) + remote_addr + attr(0)
        self.update(
            {
                "h": remote_addr,
                "l": "-",
                "t": time.strftime("[%d/%b/%Y:%H:%M:%S %z]"),
                "r": f"{method} {request['path']} {protocol}",
                "s": colored_status,
                "S": request["scheme"],
                "m": method,
                "U": request["path"],
                "q": request["query_string"].decode(),
                "H": protocol,
                "b": self["{Content-Length}o"],
                "B": self["{Content-Length}o"],
                "f": self["{Referer}i"],
                "a": self["{User-Agent}i"],
                "T": int(request_time),
                "D": int(request_time * 1_000_000),
                "L": f"{request_time:.6f}",
                "p": f"<{os.getpid()}>",
            }
        )

    def __getitem__(self, key: str) -> str:
        try:
            if key.startswith("{"):
                return super().__getitem__(key.lower())
            else:
                return super().__getitem__(key)
        except KeyError:
            return "-"
