import json
import logging
from pathlib import Path
from typing import Any, Dict

import click

from roborock import RoborockException
from roborock.api import RoborockClient, RoborockMqttClient
from roborock.containers import LoginData
from roborock.typing import RoborockDeviceInfo
from roborock.util import run_sync

_LOGGER = logging.getLogger(__name__)


class RoborockContext:
    roborock_file = Path("~/.roborock").expanduser()
    _login_data: LoginData = None

    def __init__(self):
        self.reload()

    def reload(self):
        if self.roborock_file.is_file():
            with open(self.roborock_file, 'r') as f:
                data = json.load(f)
                if data:
                    self._login_data = LoginData(data)

    def update(self, login_data: LoginData):
        data = json.dumps(login_data, default=vars)
        with open(self.roborock_file, 'w') as f:
            f.write(data)
        self.reload()

    def validate(self):
        if self._login_data is None:
            raise RoborockException("You must login first")

    def login_data(self):
        self.validate()
        return self._login_data


@click.option("-d", "--debug", default=False, count=True)
@click.version_option(package_name="python-roborock")
@click.group()
@click.pass_context
def cli(ctx, debug: int):
    logging_config: Dict[str, Any] = {
        "level": logging.DEBUG if debug > 0 else logging.INFO
    }
    logging.basicConfig(**logging_config)  # type: ignore
    ctx.obj = RoborockContext()


@click.command()
@click.option("--email", required=True)
@click.option("--password", required=True)
@click.pass_context
@run_sync()
async def login(ctx, email, password):
    """Login to Roborock account."""
    context: RoborockContext = ctx.obj
    try:
        context.validate()
        _LOGGER.info("Already logged in")
        return
    except RoborockException:
        pass
    client = RoborockClient(email)
    user_data = await client.pass_login(password)
    context.update(LoginData({"user_data": user_data, "email": email}))

async def _discover(ctx):
    context: RoborockContext = ctx.obj
    login_data = context.login_data()
    client = RoborockClient(login_data.email)
    home_data = await client.get_home_data(login_data.user_data)
    context.update(LoginData({**login_data, "home_data": home_data}))
    click.echo(f"Discovered devices {', '.join([device.name for device in home_data.devices + home_data.received_devices])}")

@click.command()
@click.pass_context
@run_sync()
async def discover(ctx):
    await _discover(ctx)

@click.command()
@click.pass_context
@run_sync()
async def list_devices(ctx):
    context: RoborockContext = ctx.obj
    login_data = context.login_data()
    if not login_data.home_data:
        await _discover(ctx)
        login_data = context.login_data()
    home_data = login_data.home_data
    click.echo(f"Known devices {', '.join([device.name for device in home_data.devices + home_data.received_devices])}")

@click.command()
@click.pass_context
@run_sync()
async def get_status(ctx):
    context: RoborockContext = ctx.obj
    login_data = context.login_data()
    if not login_data.home_data:
        await _discover(ctx)
        login_data = context.login_data()
    home_data = login_data.home_data
    device_map: dict[str, RoborockDeviceInfo] = {}
    for device in home_data.devices + home_data.received_devices:
        product = next(
            (
                product
                for product in home_data.products
                if product.id == device.product_id
            ),
            {},
        )
        device_map[device.duid] = RoborockDeviceInfo(device, product)
    mqtt_client = RoborockMqttClient(login_data.user_data, device_map)
    await mqtt_client.get_status(home_data.devices[0].duid)
    mqtt_client.__del__()


cli.add_command(login)
cli.add_command(discover)
cli.add_command(list_devices)
cli.add_command(get_status)


def main():
    return cli()


if __name__ == "__main__":
    main()
