# Databricks notebook source
## Setup Azure IoT Hub (Event Hub compatible endpoint) connection information

# Read secret from Azure KeyVault secret scope
# Please add "key-vault-secrets" as Scope Name in the following instruction
# https://docs.microsoft.com/en-us/azure/databricks/security/secrets/secret-scopes
# You can see key names by running following command in Databricks CLI
# databricks secrets list --scope key-vault-secrets
KEY_VAULT_SCOPE_NAME = "key-vault-secrets"
# App assume "iot-connection-string" is stored in Azure KeyVault
EVENTHUB_CONNECTION_STRING = dbutils.secrets.get(scope=KEY_VAULT_SCOPE_NAME, key="iot-connection-string")
EVENTHUB_CONSUMER_GROUP = "$Default"

# COMMAND ----------

from pyot import connector, aggregate

# Source with default settings
raw_streaming_df = connector.create_eventhub_streamdf(
    spark,
    EVENTHUB_CONNECTION_STRING,
    EVENTHUB_CONSUMER_GROUP
)

aggregated_df = aggregate.create_averaged_df(raw_streaming_df, 30, 60)

# Write data in the console
display(aggregated_df)

# COMMAND ----------

