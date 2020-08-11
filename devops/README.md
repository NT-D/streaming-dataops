# CI/CD with Azure DataBricks and Azure Devops
This document describes how to automate testing, buidling package and deploy it to Azure DataBricks with Azure DevOps and Azure KeyVault. You'll create CI/CD pipeliine on Azure DevOps and utilized KeyVault to persisting and fetching secrets such as Azure DataBricks hostname and tokens

# Manual Steps
For easier understanding about pyspark CI/CD with DataBricks, let me explain manual steps at first.

## Build the python package
Because DataBricks accespts a whl package instead of project files, we need to build package with setuptool. If you are a beginner of packaging, please see **Packaging Python Projects** in the reference section.
1. Run `python setup.py sdist bdist_wheel`

## Publish the package to the Azure DataBricks
Upload whl package to DataBrciks and install it to specific cluster
1. [Setup DataBricks CLI](https://docs.databricks.com/dev-tools/cli/index.html)
1. Run `dbfs mkdirs dbfs:/FileStore/whls` to make library folder in DBFS (DataBricks File System)
1. Run `dbfs cp "{Your local code path}/streaming-dataops/dist/pyot-0.0.1-py3-none-any.whl" dbfs:/FileStore/whls` to upload package to DBFS.
1. Run `databricks clusters list` to see cluster ids
1. Run `databricks clusters start --cluster-id {Your cluster id}` to start your cluster
1. Install own python library by runnning `databricks libraries install --cluster-id {Your cluster id} --whl "dbfs:/FileStore/whls/pyot-0.0.1-py3-none-any.whl"`

## Install required package
1. Install Event Hub connector by running `databricks libraries install --cluster-id {Your cluster id} --maven-coordinates com.microsoft.azure:azure-eventhubs-spark_2.11:2.3.16`

# Setup CI/CD pipeline in Azure DevOps
## Prerequistics
- Have initialized Azure DataBricks and created at least one cluster (**DBR 6.5/Spark 2.4.5**)
- Have basic understanding to use Azure Pipeline. You can learn it [here](https://docs.microsoft.com/en-us/azure/devops/pipelines/ecosystems/python?view=azure-devops).
- Access secrets from Azure KeyVault. You can understand in this [tutorial](https://docs.microsoft.com/en-us/azure/devops/pipelines/release/azure-key-vault?view=azure-devops).

## Steps
1. [Get Databricks personal access token](https://docs.databricks.com/dev-tools/api/latest/authentication.html).
1. Save following secrets in Azure KeyVault
1. Setup Azure Pipeline with `devops/ci-python-package.yml` and run pipeline. You can refer [this page](https://docs.microsoft.com/en-us/azure/devops/pipelines/ecosystems/python?view=azure-devops#create-the-pipeline) to know how to setup pipeline.
   - After the step 6 in the document, please select **Existing Azure Pipelines YAML file** in [Configure] tab, then you can select YAML file in [Path] dropdown menu in pop-up window to utilize our pipeline.
   - In the [Review] tab, you can setup KeyVault configuration. Please click **Settings** just above the **task: AzureKeyVault@1**, so that you can setup your Azure subscription and Key vault name.

### Required secrets
|Secrets name|Secret value|
|--|--|
|databricks-host|{Your Databricks host name} such as https://adb-xxxx.azuredatabricks.net|
|databricks-token|{Your DataBricks personal access token}|
|databricks-cluster-id|{Your cluster id}|

### Tips
Databricks CLI needs initiali **interactive** setup by `databricks configure --token`, but we can't do interaction in the pipeline. CLI 0.8.0 and above supports `DATABRICKS_HOST` and `DATABRICKS_TOKEN` environmental variable, so we utilize it from CLI for achieving non-interactive setup.

# Reference
- [Packaging Python Projects](https://packaging.python.org/tutorials/packaging-projects/)
- [Libraries CLI](https://docs.microsoft.com/en-us/azure/databricks/dev-tools/cli/libraries-cli)