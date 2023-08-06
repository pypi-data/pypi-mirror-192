# docker-minecraft-cli, a wrapper to install a Minecraft server under Docker.
# Copyright (C) 2023 osfanbuff63
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
"""docker-minecraft-cli, a wrapper to install a Minecraft server under Docker."""

import sys

import click

from . import lib

__version__ = "0.1.0"


@click.command(help="Run a Minecraft server under Docker in one command.")
@click.option(
    "--version", "-v", "version", is_flag=True, help="Show the version and exit."
)
@click.option(
    "--memory",
    "-m",
    "memory",
    default="2G",
    show_default=True,
    help="How much memory to allocate, in the format numberG. As an example, 2G is 2 gigabytes of memory, 3G would be 3, and so on.",
)
@click.option(
    "--mc-version",
    "-V",
    "mc_version",
    default="LATEST",
    show_default=True,
    help="The version of Minecraft to use. Any version of Minecraft is acceptable, as well as LATEST (the latest version) or SNAPSHOT (the latest snapshot).",
    required=True,
)
@click.option(
    "--variant",
    "-a",
    "variant",
    help="The variant of the Docker image to use. Valid variants can be found at https://github.com/itzg/docker-minecraft-server#running-minecraft-server-on-different-java-version",
)
@click.option(
    "--type",
    "-t",
    "type",
    help="The type of server. Can be Forge, Fabric, Quilt, Bukkit/Spigot/Paper/Pufferfish/Purpur, you name it. Full list at https://github.com/itzg/docker-minecraft-server#server-types",
)
@click.option("--run/--no-run", "run", help="Create and run this container now.")
def docker_minecraft(version, memory, mc_version, variant, type, run):
    if version:
        click.echo(f"docker-minecraft-cli {__version__}")
        sys.exit(0)
    type_str = str(type)
    environment = {
        "EULA": "true",
        "MEMORY": memory,
        "VERSION": mc_version,
        "TYPE": type_str.upper(),
    }
    click.echo("Preparing Docker.")
    client = lib.__init__()
    click.echo("Creating container. This could take a while...")
    container = lib.create(client, environment, variant)
    click.echo("Container created!")
    if run is False:
        click.echo(f"\nContainer ID: {container.id}")
        click.echo("Copy the above ID now, you will need it to run this container later.")
        click.echo("This isn't super sensitive, but keep it in a safe place.")
        click.echo("If you don't copy it, just run this command again and it will generate a new one.")
    else:
        click.echo("Running container!")
        lib.run_existing(container)
