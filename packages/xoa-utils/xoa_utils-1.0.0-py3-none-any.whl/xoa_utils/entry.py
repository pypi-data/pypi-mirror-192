import asyncssh
import asyncio
import asyncclick
import sys
import os
from xoa_utils.clis import ReadConfig
from xoa_utils.hub import Hub
from xoa_utils.ssh_server import XenaSSHServer
from xoa_utils.cmds import CmdWorker


class XenaSSHCLIHandle:
    def __init__(self, config: ReadConfig) -> None:
        self.config = config

    async def handle_client(self, process: asyncssh.SSHServerProcess) -> None:
        out = process.stdout
        setattr(out, "flush", out._chan._flush_send_buf)
        # patch the flush() method since it doesn't exist.
        asyncclick.echo(
            f"Hello {process.get_extra_info('username')}, welcome to Xena OpenAutomation Utilities SSH Service.",
            file=out,
        )
        worker = CmdWorker(process)
        await worker.run(self.config)


async def start_server(config: ReadConfig) -> None:
    Hub.check_hub_process(config)
    print(
        f"(PID: {os.getpid()}) XOA Utils SSH Service running on 0.0.0.0:{config.conn_port}."
    )
    await asyncssh.create_server(
        XenaSSHServer,
        "0.0.0.0",
        config.conn_port,
        server_host_keys=[config.conn_host_keys],
        process_factory=XenaSSHCLIHandle(config).handle_client,
    )


def main() -> None:
    loop = asyncio.get_event_loop()
    argv = (sys.argv[1],) if len(sys.argv) >= 2 else tuple()
    config = ReadConfig(*argv)
    try:
        loop.run_until_complete(start_server(config))
        loop.run_forever()
    except (OSError, asyncssh.Error) as exc:
        sys.exit(f"Error starting server: <{type(str(exc))}> {exc}")
    except KeyboardInterrupt:
        os.remove(config.hub_pid_path)


if __name__ == "__main__":
    main()
