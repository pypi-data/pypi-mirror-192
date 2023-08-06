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
"""Utility functions and classes."""

import platform
import random
from typing import Optional

import docker  # type: ignore
from docker.errors import APIError  # type: ignore
from docker.models.containers import Container  # type: ignore


class DockerError(Exception):
    """A generic error occurred from Docker."""


class UnreachableServerError(DockerError):
    """The Docker server was unreachable."""


class InvalidValue(Exception):
    """The value was invalid."""


def __init__() -> docker.DockerClient:
    """Initializes a Docker client."""
    client = docker.from_env()
    try:
        client.ping()
    except APIError:
        raise UnreachableServerError(
            "The Docker Hub server was unreachable. Are you connected to the Internet?"
        )
    return client


def create(client: docker.DockerClient, environment: dict, variant: Optional[str] = None):
    """Create the Docker container, but don't run it yet.

    Args:
        client (docker.DockerClient): The Docker client to create under.
        environment (dict): The environment variables, to pass to itzg/minecraft-server.
        variant (str, optional): The variant

    Returns:
        Container: The container object.
    """
    if variant is not None:
        if variant not in [
            "latest",
            "java8",
            "java8-multiarch",
            "java8-jdk",
            "java8-openj9",
            "java8-graalvm-ce",
            "java11",
            "java11-jdk",
            "java11-openj9",
            "java17",
            "java17-jdk",
            "java17-openj9",
            "java17-graalvm-ce",
            "java17-alpine",
            "java19",
        ]:
            raise InvalidValue(
                "Invalid variant. Check https://github.com/itzg/docker-minecraft-server#running-minecraft-server-on-different-java-version for a list of valid variants."
            )
        elif (
            variant
            not in [
                "latest",
                "java8-multiarch",
                "java11",
                "java11-jdk",
                "java17",
                "java17-jdk",
                "java17-graalvm-ce",
                "java19",
            ]
            and platform.machine().startswith("arm")
            or platform.machine().startswith("aarch")
        ):
            raise InvalidValue("This value won't work on your CPU.")
    else:
        if environment["VERSION"] == "LATEST" or "SNAPSHOT":
            pass
        elif environment["VERSION"] < 1.17:
            variant = "java8-multiarch"
        else:
            variant = "latest"
    client.images.pull("itzg/minecraft-server", variant)
    return client.containers.create(f"itzg/minecraft-server", name=f"minecraft-server-{str(random.random())}", environment=environment, ports={"25565/tcp": "25565"})


def run_existing(container: Container):
    container.start()
    for line in container.logs(stream=True):
        print(line.strip())
