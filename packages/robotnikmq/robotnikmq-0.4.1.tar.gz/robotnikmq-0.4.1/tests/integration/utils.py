from contextlib import contextmanager
from multiprocessing import Process
from subprocess import run
from time import sleep
from typing import Callable, Any, Tuple, Optional

# pylint: disable=E0401
from pytest_rabbitmq.factories.executor import RabbitMqExecutor  # type: ignore

# pylint: enable=E0401
from pytest import fixture

from robotnikmq.config import server_config, RobotnikConfig


USERNAME = "robotnik"
PASSWORD = "hackme"
VIRTUAL_HOST = "/robotnik"

META_QUEUE = "skynet.legion"


@contextmanager
def sub_process(
    target: Callable,
    args: Optional[Tuple[Any, ...]] = None,
    name: Optional[str] = None,
    terminate: bool = True,
):
    proc = Process(target=target, args=args or (), name=name)
    proc.start()
    try:
        sleep(0.2)
        yield proc
    finally:
        if terminate:
            proc.terminate()
        proc.join()


def initialize_rabbitmq(proc: RabbitMqExecutor):
    run(
        [
            proc.rabbit_ctl,
            "--quiet",
            "-n",
            f"rabbitmq-test-{proc.port}",
            "add_user",
            USERNAME,
            PASSWORD,
        ],
        check=False,
    )
    run(
        [
            proc.rabbit_ctl,
            "--quiet",
            "-n",
            f"rabbitmq-test-{proc.port}",
            "add_vhost",
            VIRTUAL_HOST,
            "--description",
            "Used for testing RobotnikMQ",
        ],
        check=False,
    )
    run(
        [
            proc.rabbit_ctl,
            "--quiet",
            "-n",
            f"rabbitmq-test-{proc.port}",
            "set_permissions",
            "-p",
            VIRTUAL_HOST,
            USERNAME,
            ".*",
            ".*",
            ".*",
        ],
        check=False,
    )


@fixture(scope="module")
def robotnikmq_config(rabbitmq_proc):
    initialize_rabbitmq(rabbitmq_proc)
    return config_for(rabbitmq_proc)


def config_for(proc: RabbitMqExecutor) -> RobotnikConfig:
    return RobotnikConfig(
        tiers=[[server_config(proc.host, proc.port, USERNAME, PASSWORD, VIRTUAL_HOST)]]
    )
