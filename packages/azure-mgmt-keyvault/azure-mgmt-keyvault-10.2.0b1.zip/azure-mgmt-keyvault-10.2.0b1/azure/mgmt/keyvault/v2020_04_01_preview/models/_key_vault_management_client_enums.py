# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from enum import Enum
from azure.core import CaseInsensitiveEnumMeta


class AccessPolicyUpdateKind(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """AccessPolicyUpdateKind."""

    ADD = "add"
    REPLACE = "replace"
    REMOVE = "remove"


class ActionsRequired(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """A message indicating if changes on the service provider require any updates on the consumer."""

    NONE = "None"


class CertificatePermissions(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """CertificatePermissions."""

    GET = "get"
    LIST = "list"
    DELETE = "delete"
    CREATE = "create"
    IMPORT = "import"
    UPDATE = "update"
    MANAGECONTACTS = "managecontacts"
    GETISSUERS = "getissuers"
    LISTISSUERS = "listissuers"
    SETISSUERS = "setissuers"
    DELETEISSUERS = "deleteissuers"
    MANAGEISSUERS = "manageissuers"
    RECOVER = "recover"
    PURGE = "purge"
    BACKUP = "backup"
    RESTORE = "restore"


class CreateMode(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The vault's create mode to indicate whether the vault need to be recovered or not."""

    RECOVER = "recover"
    DEFAULT = "default"


class DeletionRecoveryLevel(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The deletion recovery level currently in effect for the object. If it contains 'Purgeable',
    then the object can be permanently deleted by a privileged user; otherwise, only the system can
    purge the object at the end of the retention interval.
    """

    PURGEABLE = "Purgeable"
    RECOVERABLE_PURGEABLE = "Recoverable+Purgeable"
    RECOVERABLE = "Recoverable"
    RECOVERABLE_PROTECTED_SUBSCRIPTION = "Recoverable+ProtectedSubscription"


class Enum16(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Enum16."""

    RESOURCE_TYPE_EQ_MICROSOFT_KEY_VAULT_VAULTS_ = "resourceType eq 'Microsoft.KeyVault/vaults'"


class Enum17(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Enum17."""

    TWO_THOUSAND_FIFTEEN11_01 = "2015-11-01"


class IdentityType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The type of identity."""

    USER = "User"
    APPLICATION = "Application"
    MANAGED_IDENTITY = "ManagedIdentity"
    KEY = "Key"


class JsonWebKeyCurveName(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The elliptic curve name. For valid values, see JsonWebKeyCurveName."""

    P256 = "P-256"
    P384 = "P-384"
    P521 = "P-521"
    P256_K = "P-256K"


class JsonWebKeyOperation(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The permitted JSON web key operations of the key. For more information, see
    JsonWebKeyOperation.
    """

    ENCRYPT = "encrypt"
    DECRYPT = "decrypt"
    SIGN = "sign"
    VERIFY = "verify"
    WRAP_KEY = "wrapKey"
    UNWRAP_KEY = "unwrapKey"
    IMPORT = "import"


class JsonWebKeyType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The type of the key. For valid values, see JsonWebKeyType."""

    EC = "EC"
    EC_HSM = "EC-HSM"
    RSA = "RSA"
    RSA_HSM = "RSA-HSM"


class KeyPermissions(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """KeyPermissions."""

    ENCRYPT = "encrypt"
    DECRYPT = "decrypt"
    WRAP_KEY = "wrapKey"
    UNWRAP_KEY = "unwrapKey"
    SIGN = "sign"
    VERIFY = "verify"
    GET = "get"
    LIST = "list"
    CREATE = "create"
    UPDATE = "update"
    IMPORT = "import"
    DELETE = "delete"
    BACKUP = "backup"
    RESTORE = "restore"
    RECOVER = "recover"
    PURGE = "purge"


class ManagedHsmSkuFamily(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """SKU Family of the managed HSM Pool."""

    B = "B"


class ManagedHsmSkuName(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """SKU of the managed HSM Pool."""

    STANDARD_B1 = "Standard_B1"
    CUSTOM_B32 = "Custom_B32"


class NetworkRuleAction(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The default action when no rule from ipRules and from virtualNetworkRules match. This is only
    used after the bypass property has been evaluated.
    """

    ALLOW = "Allow"
    DENY = "Deny"


class NetworkRuleBypassOptions(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Tells what traffic can bypass network rules. This can be 'AzureServices' or 'None'.  If not
    specified the default is 'AzureServices'.
    """

    AZURE_SERVICES = "AzureServices"
    NONE = "None"


class PrivateEndpointConnectionProvisioningState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The current provisioning state."""

    SUCCEEDED = "Succeeded"
    CREATING = "Creating"
    UPDATING = "Updating"
    DELETING = "Deleting"
    FAILED = "Failed"
    DISCONNECTED = "Disconnected"


class PrivateEndpointServiceConnectionStatus(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The private endpoint connection status."""

    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    DISCONNECTED = "Disconnected"


class ProvisioningState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Provisioning state."""

    SUCCEEDED = "Succeeded"
    """The managed HSM Pool has been full provisioned."""
    PROVISIONING = "Provisioning"
    """The managed HSM Pool is currently being provisioned."""
    FAILED = "Failed"
    """Provisioning of the managed HSM Pool has failed."""
    UPDATING = "Updating"
    """The managed HSM Pool is currently being updated."""
    DELETING = "Deleting"
    """The managed HSM Pool is currently being deleted."""
    ACTIVATED = "Activated"
    """The managed HSM pool is ready for normal use."""
    SECURITY_DOMAIN_RESTORE = "SecurityDomainRestore"
    """The managed HSM pool is waiting for a security domain restore action."""
    RESTORING = "Restoring"
    """The managed HSM pool is being restored from full HSM backup."""


class Reason(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The reason that a vault name could not be used. The Reason element is only returned if
    NameAvailable is false.
    """

    ACCOUNT_NAME_INVALID = "AccountNameInvalid"
    ALREADY_EXISTS = "AlreadyExists"


class SecretPermissions(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """SecretPermissions."""

    GET = "get"
    LIST = "list"
    SET = "set"
    DELETE = "delete"
    BACKUP = "backup"
    RESTORE = "restore"
    RECOVER = "recover"
    PURGE = "purge"


class SkuFamily(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """SKU family name."""

    A = "A"


class SkuName(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """SKU name to specify whether the key vault is a standard vault or a premium vault."""

    STANDARD = "standard"
    PREMIUM = "premium"


class StoragePermissions(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """StoragePermissions."""

    GET = "get"
    LIST = "list"
    DELETE = "delete"
    SET = "set"
    UPDATE = "update"
    REGENERATEKEY = "regeneratekey"
    RECOVER = "recover"
    PURGE = "purge"
    BACKUP = "backup"
    RESTORE = "restore"
    SETSAS = "setsas"
    LISTSAS = "listsas"
    GETSAS = "getsas"
    DELETESAS = "deletesas"


class VaultProvisioningState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Provisioning state of the vault."""

    SUCCEEDED = "Succeeded"
    REGISTERING_DNS = "RegisteringDns"
