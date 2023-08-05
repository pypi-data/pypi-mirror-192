# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

import sys
from typing import Any, TYPE_CHECKING

from azure.core.configuration import Configuration
from azure.core.pipeline import policies
from azure.mgmt.core.policies import ARMChallengeAuthenticationPolicy, ARMHttpLoggingPolicy

from ._version import VERSION

if sys.version_info >= (3, 8):
    from typing import Literal  # pylint: disable=no-name-in-module, ungrouped-imports
else:
    from typing_extensions import Literal  # type: ignore  # pylint: disable=ungrouped-imports

if TYPE_CHECKING:
    # pylint: disable=unused-import,ungrouped-imports
    from azure.core.credentials import TokenCredential


class KeyVaultManagementClientConfiguration(Configuration):  # pylint: disable=too-many-instance-attributes
    """Configuration for KeyVaultManagementClient.

    Note that all parameters used to create this instance are saved as instance
    attributes.

    :param credential: Credential needed for the client to connect to Azure. Required.
    :type credential: ~azure.core.credentials.TokenCredential
    :param subscription_id: Subscription credentials which uniquely identify Microsoft Azure
     subscription. The subscription ID forms part of the URI for every service call. Required.
    :type subscription_id: str
    :keyword api_version: Api Version. Default value is "2019-09-01". Note that overriding this
     default value may result in unsupported behavior.
    :paramtype api_version: str
    """

    def __init__(self, credential: "TokenCredential", subscription_id: str, **kwargs: Any) -> None:
        super(KeyVaultManagementClientConfiguration, self).__init__(**kwargs)
        api_version: Literal["2019-09-01"] = kwargs.pop("api_version", "2019-09-01")

        if credential is None:
            raise ValueError("Parameter 'credential' must not be None.")
        if subscription_id is None:
            raise ValueError("Parameter 'subscription_id' must not be None.")

        self.credential = credential
        self.subscription_id = subscription_id
        self.api_version = api_version
        self.credential_scopes = kwargs.pop("credential_scopes", ["https://management.azure.com/.default"])
        kwargs.setdefault("sdk_moniker", "mgmt-keyvault/{}".format(VERSION))
        self._configure(**kwargs)

    def _configure(self, **kwargs: Any) -> None:
        self.user_agent_policy = kwargs.get("user_agent_policy") or policies.UserAgentPolicy(**kwargs)
        self.headers_policy = kwargs.get("headers_policy") or policies.HeadersPolicy(**kwargs)
        self.proxy_policy = kwargs.get("proxy_policy") or policies.ProxyPolicy(**kwargs)
        self.logging_policy = kwargs.get("logging_policy") or policies.NetworkTraceLoggingPolicy(**kwargs)
        self.http_logging_policy = kwargs.get("http_logging_policy") or ARMHttpLoggingPolicy(**kwargs)
        self.retry_policy = kwargs.get("retry_policy") or policies.RetryPolicy(**kwargs)
        self.custom_hook_policy = kwargs.get("custom_hook_policy") or policies.CustomHookPolicy(**kwargs)
        self.redirect_policy = kwargs.get("redirect_policy") or policies.RedirectPolicy(**kwargs)
        self.authentication_policy = kwargs.get("authentication_policy")
        if self.credential and not self.authentication_policy:
            self.authentication_policy = ARMChallengeAuthenticationPolicy(
                self.credential, *self.credential_scopes, **kwargs
            )
