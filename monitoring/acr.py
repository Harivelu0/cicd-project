from azure.mgmt.containerregistry import ContainerRegistryManagementClient
from azure.identity import DefaultAzureCredential

# Initialize the client with existing credentials
credential = DefaultAzureCredential()
subscription_id = ""  # This is required for the API
acr_client = ContainerRegistryManagementClient(credential, subscription_id)

# Create the container registry
acr_name = "mymonitoringapp"  # Your registry name
resource_group_name = "democlus"  # Your resource group

registry = acr_client.registries.begin_create(
    resource_group_name,
    acr_name,
    {"location": "centralindia", "sku": {"name": "Basic"}}
).result()

# Get the repository URI
repository_uri = f"{registry.login_server}/my_monitoring_app_image"
print(repository_uri)