# pylint: disable=too-many-lines
# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
import sys
from typing import Any, AsyncIterable, Callable, Dict, IO, Optional, TypeVar, Union, overload
import urllib.parse

from azure.core.async_paging import AsyncItemPaged, AsyncList
from azure.core.exceptions import (
    ClientAuthenticationError,
    HttpResponseError,
    ResourceExistsError,
    ResourceNotFoundError,
    ResourceNotModifiedError,
    map_error,
)
from azure.core.pipeline import PipelineResponse
from azure.core.pipeline.transport import AsyncHttpResponse
from azure.core.rest import HttpRequest
from azure.core.tracing.decorator import distributed_trace
from azure.core.tracing.decorator_async import distributed_trace_async
from azure.core.utils import case_insensitive_dict
from azure.mgmt.core.exceptions import ARMErrorFormat

from ... import models as _models
from ..._vendor import _convert_request
from ...operations._secrets_operations import (
    build_create_or_update_request,
    build_get_request,
    build_list_request,
    build_update_request,
)

if sys.version_info >= (3, 8):
    from typing import Literal  # pylint: disable=no-name-in-module, ungrouped-imports
else:
    from typing_extensions import Literal  # type: ignore  # pylint: disable=ungrouped-imports
T = TypeVar("T")
ClsType = Optional[Callable[[PipelineResponse[HttpRequest, AsyncHttpResponse], T, Dict[str, Any]], Any]]


class SecretsOperations:
    """
    .. warning::
        **DO NOT** instantiate this class directly.

        Instead, you should access the following operations through
        :class:`~azure.mgmt.keyvault.v2021_06_01_preview.aio.KeyVaultManagementClient`'s
        :attr:`secrets` attribute.
    """

    models = _models

    def __init__(self, *args, **kwargs) -> None:
        input_args = list(args)
        self._client = input_args.pop(0) if input_args else kwargs.pop("client")
        self._config = input_args.pop(0) if input_args else kwargs.pop("config")
        self._serialize = input_args.pop(0) if input_args else kwargs.pop("serializer")
        self._deserialize = input_args.pop(0) if input_args else kwargs.pop("deserializer")

    @overload
    async def create_or_update(
        self,
        resource_group_name: str,
        vault_name: str,
        secret_name: str,
        parameters: _models.SecretCreateOrUpdateParameters,
        *,
        content_type: str = "application/json",
        **kwargs: Any
    ) -> _models.Secret:
        """Create or update a secret in a key vault in the specified subscription.  NOTE: This API is
        intended for internal use in ARM deployments. Users should use the data-plane REST service for
        interaction with vault secrets.

        :param resource_group_name: The name of the Resource Group to which the vault belongs.
         Required.
        :type resource_group_name: str
        :param vault_name: Name of the vault. Required.
        :type vault_name: str
        :param secret_name: Name of the secret. Required.
        :type secret_name: str
        :param parameters: Parameters to create or update the secret. Required.
        :type parameters:
         ~azure.mgmt.keyvault.v2021_06_01_preview.models.SecretCreateOrUpdateParameters
        :keyword content_type: Body Parameter content-type. Content type parameter for JSON body.
         Default value is "application/json".
        :paramtype content_type: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: Secret or the result of cls(response)
        :rtype: ~azure.mgmt.keyvault.v2021_06_01_preview.models.Secret
        :raises ~azure.core.exceptions.HttpResponseError:
        """

    @overload
    async def create_or_update(
        self,
        resource_group_name: str,
        vault_name: str,
        secret_name: str,
        parameters: IO,
        *,
        content_type: str = "application/json",
        **kwargs: Any
    ) -> _models.Secret:
        """Create or update a secret in a key vault in the specified subscription.  NOTE: This API is
        intended for internal use in ARM deployments. Users should use the data-plane REST service for
        interaction with vault secrets.

        :param resource_group_name: The name of the Resource Group to which the vault belongs.
         Required.
        :type resource_group_name: str
        :param vault_name: Name of the vault. Required.
        :type vault_name: str
        :param secret_name: Name of the secret. Required.
        :type secret_name: str
        :param parameters: Parameters to create or update the secret. Required.
        :type parameters: IO
        :keyword content_type: Body Parameter content-type. Content type parameter for binary body.
         Default value is "application/json".
        :paramtype content_type: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: Secret or the result of cls(response)
        :rtype: ~azure.mgmt.keyvault.v2021_06_01_preview.models.Secret
        :raises ~azure.core.exceptions.HttpResponseError:
        """

    @distributed_trace_async
    async def create_or_update(
        self,
        resource_group_name: str,
        vault_name: str,
        secret_name: str,
        parameters: Union[_models.SecretCreateOrUpdateParameters, IO],
        **kwargs: Any
    ) -> _models.Secret:
        """Create or update a secret in a key vault in the specified subscription.  NOTE: This API is
        intended for internal use in ARM deployments. Users should use the data-plane REST service for
        interaction with vault secrets.

        :param resource_group_name: The name of the Resource Group to which the vault belongs.
         Required.
        :type resource_group_name: str
        :param vault_name: Name of the vault. Required.
        :type vault_name: str
        :param secret_name: Name of the secret. Required.
        :type secret_name: str
        :param parameters: Parameters to create or update the secret. Is either a
         SecretCreateOrUpdateParameters type or a IO type. Required.
        :type parameters:
         ~azure.mgmt.keyvault.v2021_06_01_preview.models.SecretCreateOrUpdateParameters or IO
        :keyword content_type: Body Parameter content-type. Known values are: 'application/json'.
         Default value is None.
        :paramtype content_type: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: Secret or the result of cls(response)
        :rtype: ~azure.mgmt.keyvault.v2021_06_01_preview.models.Secret
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: Literal["2021-06-01-preview"] = kwargs.pop(
            "api_version", _params.pop("api-version", "2021-06-01-preview")
        )
        content_type: Optional[str] = kwargs.pop("content_type", _headers.pop("Content-Type", None))
        cls: ClsType[_models.Secret] = kwargs.pop("cls", None)

        content_type = content_type or "application/json"
        _json = None
        _content = None
        if isinstance(parameters, (IO, bytes)):
            _content = parameters
        else:
            _json = self._serialize.body(parameters, "SecretCreateOrUpdateParameters")

        request = build_create_or_update_request(
            resource_group_name=resource_group_name,
            vault_name=vault_name,
            secret_name=secret_name,
            subscription_id=self._config.subscription_id,
            api_version=api_version,
            content_type=content_type,
            json=_json,
            content=_content,
            template_url=self.create_or_update.metadata["url"],
            headers=_headers,
            params=_params,
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
            request, stream=False, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200, 201]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        if response.status_code == 200:
            deserialized = self._deserialize("Secret", pipeline_response)

        if response.status_code == 201:
            deserialized = self._deserialize("Secret", pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})  # type: ignore

        return deserialized  # type: ignore

    create_or_update.metadata = {
        "url": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.KeyVault/vaults/{vaultName}/secrets/{secretName}"
    }

    @overload
    async def update(
        self,
        resource_group_name: str,
        vault_name: str,
        secret_name: str,
        parameters: _models.SecretPatchParameters,
        *,
        content_type: str = "application/json",
        **kwargs: Any
    ) -> _models.Secret:
        """Update a secret in the specified subscription.  NOTE: This API is intended for internal use in
        ARM deployments.  Users should use the data-plane REST service for interaction with vault
        secrets.

        :param resource_group_name: The name of the Resource Group to which the vault belongs.
         Required.
        :type resource_group_name: str
        :param vault_name: Name of the vault. Required.
        :type vault_name: str
        :param secret_name: Name of the secret. Required.
        :type secret_name: str
        :param parameters: Parameters to patch the secret. Required.
        :type parameters: ~azure.mgmt.keyvault.v2021_06_01_preview.models.SecretPatchParameters
        :keyword content_type: Body Parameter content-type. Content type parameter for JSON body.
         Default value is "application/json".
        :paramtype content_type: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: Secret or the result of cls(response)
        :rtype: ~azure.mgmt.keyvault.v2021_06_01_preview.models.Secret
        :raises ~azure.core.exceptions.HttpResponseError:
        """

    @overload
    async def update(
        self,
        resource_group_name: str,
        vault_name: str,
        secret_name: str,
        parameters: IO,
        *,
        content_type: str = "application/json",
        **kwargs: Any
    ) -> _models.Secret:
        """Update a secret in the specified subscription.  NOTE: This API is intended for internal use in
        ARM deployments.  Users should use the data-plane REST service for interaction with vault
        secrets.

        :param resource_group_name: The name of the Resource Group to which the vault belongs.
         Required.
        :type resource_group_name: str
        :param vault_name: Name of the vault. Required.
        :type vault_name: str
        :param secret_name: Name of the secret. Required.
        :type secret_name: str
        :param parameters: Parameters to patch the secret. Required.
        :type parameters: IO
        :keyword content_type: Body Parameter content-type. Content type parameter for binary body.
         Default value is "application/json".
        :paramtype content_type: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: Secret or the result of cls(response)
        :rtype: ~azure.mgmt.keyvault.v2021_06_01_preview.models.Secret
        :raises ~azure.core.exceptions.HttpResponseError:
        """

    @distributed_trace_async
    async def update(
        self,
        resource_group_name: str,
        vault_name: str,
        secret_name: str,
        parameters: Union[_models.SecretPatchParameters, IO],
        **kwargs: Any
    ) -> _models.Secret:
        """Update a secret in the specified subscription.  NOTE: This API is intended for internal use in
        ARM deployments.  Users should use the data-plane REST service for interaction with vault
        secrets.

        :param resource_group_name: The name of the Resource Group to which the vault belongs.
         Required.
        :type resource_group_name: str
        :param vault_name: Name of the vault. Required.
        :type vault_name: str
        :param secret_name: Name of the secret. Required.
        :type secret_name: str
        :param parameters: Parameters to patch the secret. Is either a SecretPatchParameters type or a
         IO type. Required.
        :type parameters: ~azure.mgmt.keyvault.v2021_06_01_preview.models.SecretPatchParameters or IO
        :keyword content_type: Body Parameter content-type. Known values are: 'application/json'.
         Default value is None.
        :paramtype content_type: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: Secret or the result of cls(response)
        :rtype: ~azure.mgmt.keyvault.v2021_06_01_preview.models.Secret
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: Literal["2021-06-01-preview"] = kwargs.pop(
            "api_version", _params.pop("api-version", "2021-06-01-preview")
        )
        content_type: Optional[str] = kwargs.pop("content_type", _headers.pop("Content-Type", None))
        cls: ClsType[_models.Secret] = kwargs.pop("cls", None)

        content_type = content_type or "application/json"
        _json = None
        _content = None
        if isinstance(parameters, (IO, bytes)):
            _content = parameters
        else:
            _json = self._serialize.body(parameters, "SecretPatchParameters")

        request = build_update_request(
            resource_group_name=resource_group_name,
            vault_name=vault_name,
            secret_name=secret_name,
            subscription_id=self._config.subscription_id,
            api_version=api_version,
            content_type=content_type,
            json=_json,
            content=_content,
            template_url=self.update.metadata["url"],
            headers=_headers,
            params=_params,
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
            request, stream=False, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200, 201]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        if response.status_code == 200:
            deserialized = self._deserialize("Secret", pipeline_response)

        if response.status_code == 201:
            deserialized = self._deserialize("Secret", pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})  # type: ignore

        return deserialized  # type: ignore

    update.metadata = {
        "url": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.KeyVault/vaults/{vaultName}/secrets/{secretName}"
    }

    @distributed_trace_async
    async def get(self, resource_group_name: str, vault_name: str, secret_name: str, **kwargs: Any) -> _models.Secret:
        """Gets the specified secret.  NOTE: This API is intended for internal use in ARM deployments.
        Users should use the data-plane REST service for interaction with vault secrets.

        :param resource_group_name: The name of the Resource Group to which the vault belongs.
         Required.
        :type resource_group_name: str
        :param vault_name: The name of the vault. Required.
        :type vault_name: str
        :param secret_name: The name of the secret. Required.
        :type secret_name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: Secret or the result of cls(response)
        :rtype: ~azure.mgmt.keyvault.v2021_06_01_preview.models.Secret
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: Literal["2021-06-01-preview"] = kwargs.pop(
            "api_version", _params.pop("api-version", "2021-06-01-preview")
        )
        cls: ClsType[_models.Secret] = kwargs.pop("cls", None)

        request = build_get_request(
            resource_group_name=resource_group_name,
            vault_name=vault_name,
            secret_name=secret_name,
            subscription_id=self._config.subscription_id,
            api_version=api_version,
            template_url=self.get.metadata["url"],
            headers=_headers,
            params=_params,
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
            request, stream=False, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        deserialized = self._deserialize("Secret", pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    get.metadata = {
        "url": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.KeyVault/vaults/{vaultName}/secrets/{secretName}"
    }

    @distributed_trace
    def list(
        self, resource_group_name: str, vault_name: str, top: Optional[int] = None, **kwargs: Any
    ) -> AsyncIterable["_models.Secret"]:
        """The List operation gets information about the secrets in a vault.  NOTE: This API is intended
        for internal use in ARM deployments. Users should use the data-plane REST service for
        interaction with vault secrets.

        :param resource_group_name: The name of the Resource Group to which the vault belongs.
         Required.
        :type resource_group_name: str
        :param vault_name: The name of the vault. Required.
        :type vault_name: str
        :param top: Maximum number of results to return. Default value is None.
        :type top: int
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: An iterator like instance of either Secret or the result of cls(response)
        :rtype:
         ~azure.core.async_paging.AsyncItemPaged[~azure.mgmt.keyvault.v2021_06_01_preview.models.Secret]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: Literal["2021-06-01-preview"] = kwargs.pop(
            "api_version", _params.pop("api-version", "2021-06-01-preview")
        )
        cls: ClsType[_models.SecretListResult] = kwargs.pop("cls", None)

        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        def prepare_request(next_link=None):
            if not next_link:

                request = build_list_request(
                    resource_group_name=resource_group_name,
                    vault_name=vault_name,
                    subscription_id=self._config.subscription_id,
                    top=top,
                    api_version=api_version,
                    template_url=self.list.metadata["url"],
                    headers=_headers,
                    params=_params,
                )
                request = _convert_request(request)
                request.url = self._client.format_url(request.url)

            else:
                # make call to next link with the client's api-version
                _parsed_next_link = urllib.parse.urlparse(next_link)
                _next_request_params = case_insensitive_dict(
                    {
                        key: [urllib.parse.quote(v) for v in value]
                        for key, value in urllib.parse.parse_qs(_parsed_next_link.query).items()
                    }
                )
                _next_request_params["api-version"] = self._config.api_version
                request = HttpRequest(
                    "GET", urllib.parse.urljoin(next_link, _parsed_next_link.path), params=_next_request_params
                )
                request = _convert_request(request)
                request.url = self._client.format_url(request.url)
                request.method = "GET"
            return request

        async def extract_data(pipeline_response):
            deserialized = self._deserialize("SecretListResult", pipeline_response)
            list_of_elem = deserialized.value
            if cls:
                list_of_elem = cls(list_of_elem)  # type: ignore
            return deserialized.next_link or None, AsyncList(list_of_elem)

        async def get_next(next_link=None):
            request = prepare_request(next_link)

            pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
                request, stream=False, **kwargs
            )
            response = pipeline_response.http_response

            if response.status_code not in [200]:
                map_error(status_code=response.status_code, response=response, error_map=error_map)
                raise HttpResponseError(response=response, error_format=ARMErrorFormat)

            return pipeline_response

        return AsyncItemPaged(get_next, extract_data)

    list.metadata = {
        "url": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.KeyVault/vaults/{vaultName}/secrets"
    }
