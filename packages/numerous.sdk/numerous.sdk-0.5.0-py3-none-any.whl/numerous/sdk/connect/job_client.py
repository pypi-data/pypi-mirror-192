"""Contains the implementation of the job client."""

import json
import os
from types import TracebackType
from typing import Any

import grpc
import spm_pb2
from spm_pb2 import RefreshRequest, Token
from spm_pb2_grpc import SPMStub, TokenManagerStub

from ..models.scenario import Scenario
from . import defaults
from .auth import AccessTokenAuthMetadataPlugin


class JobClient:
    """The JobClient is the recommended way to connect to the numerous platform."""

    def __init__(
        self, channel: grpc.Channel, project_id: str, scenario_id: str, job_id: str
    ):
        """Initialize the job client with a gRPC channel. The channel must be
        configured with credentials.

        :param channel: A gRPC channel configured with required authorization.
        :param project_id: Associated project ID.
        :param scenario_id: Associated scenario ID.
        :param job_id: Associated job ID.
        """
        self._channel = channel
        self._project_id = project_id
        self._scenario_id = scenario_id
        self._job_id = job_id

        self._spm_client = SPMStub(self._channel)

    @staticmethod
    def channel_options() -> list[tuple[str, Any]]:
        """Returns the default gRPC channel options."""
        return [
            ("grpc.max_message_length", defaults.GRPC_MAX_MESSAGE_SIZE),
            ("grpc.max_send_message_length", defaults.GRPC_MAX_MESSAGE_SIZE),
            ("grpc.max_receive_message_length", defaults.GRPC_MAX_MESSAGE_SIZE),
        ]

    @staticmethod
    def create(
        hostname: str,
        port: str,
        refresh_token: str,
        project_id: str,
        scenario_id: str,
        job_id: str,
    ) -> "JobClient":
        """Create a JobClient from connection parameters.

        :param hostname: Hostname of the numerous server
        :param port: gRPC port of the numerous server
        :param refresh_token: Refresh token for the execution.
        :param project_id: Associated project ID.
        :param scenario_id: Associated scenario ID.
        :param job_id: Associated job ID.
        """
        with grpc.secure_channel(
            f"{hostname}:{port}",
            grpc.ssl_channel_credentials(),
            JobClient.channel_options(),
        ) as unauthorized_channel:
            token_manager = TokenManagerStub(unauthorized_channel)
            access_token = token_manager.GetAccessToken(
                RefreshRequest(refresh_token=Token(val=refresh_token))
            )

        authorized_channel = grpc.secure_channel(
            f"{hostname}:{port}",
            grpc.composite_channel_credentials(
                grpc.ssl_channel_credentials(),
                grpc.metadata_call_credentials(
                    AccessTokenAuthMetadataPlugin(access_token.val)
                ),
            ),
            JobClient.channel_options(),
        )

        return JobClient(authorized_channel, project_id, scenario_id, job_id)

    @staticmethod
    def from_environment() -> "JobClient":
        """Create a JobClient from environment variables.

        Uses the following environment variables:
         - `NUMEROUS_API_SERVER`
         - `NUMEROUS_API_PORT`
         - `NUMEROUS_API_REFRESH_TOKEN`
        """
        return JobClient.create(
            os.environ["NUMEROUS_API_SERVER"],
            os.environ["NUMEROUS_API_PORT"],
            os.environ["NUMEROUS_API_REFRESH_TOKEN"],
            os.environ["NUMEROUS_PROJECT"],
            os.environ["NUMEROUS_SCENARIO"],
            os.environ["JOB_ID"],
        )

    def close(self) -> None:
        """Close the JobClient.

        Closes the JobClient's connection to the numerous platform, immediately
        terminating any active communication.

        This method is idempotent.
        """
        self._channel.close()

    @property
    def scenario(self) -> Scenario:
        response = self._spm_client.GetScenario(
            spm_pb2.Scenario(project=self._project_id, scenario=self._scenario_id)
        )
        data = json.loads(response.scenario_document)
        return Scenario(id=data["id"], name=data.get("scenarioName", ""))

    def __enter__(self) -> "JobClient":
        """Return itself upon entering the context manager."""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,  # noqa: F841
        exc_value: BaseException | None,  # noqa: F841
        traceback: TracebackType | None,  # noqa: F841
    ) -> bool | None:
        """Closes the gRPC channel upon exiting the context manager."""
        self.close()
        return None
