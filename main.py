from google.cloud import storage
from google.api_core.client_options import ClientOptions
from google.cloud import discoveryengine_v1alpha as discoveryengine


def import_documents(
        project_id: str,
        location: str,
        data_store_id: str,
        gcs_uri: str,
):
    # Create a client
    client_options = (
        ClientOptions(
            api_endpoint=f"{location}-discoveryengine.googleapis.com")
        if location != "global"
        else None
    )
    client = discoveryengine.DocumentServiceClient(
        client_options=client_options)

    # The full resource name of the search engine branch.
    # e.g. projects/{project}/locations/{location}/dataStores/{data_store_id}/branches/{branch}
    parent = client.branch_path(
        project=project_id,
        location=location,
        data_store=data_store_id,
        branch="default_branch",
    )

    source_documents = [f"{gcs_uri}"]

    request = discoveryengine.ImportDocumentsRequest(
        parent=parent,
        gcs_source=discoveryengine.GcsSource(
            input_uris=source_documents, data_schema="content"
        ),
        # Options: `FULL`, `INCREMENTAL`
        reconciliation_mode=discoveryengine.ImportDocumentsRequest.ReconciliationMode.INCREMENTAL,
    )

    # Make the request
    operation = client.import_documents(request=request)

    response = operation.result()

    # Once the operation is complete,
    # get information from operation metadata
    metadata = discoveryengine.ImportDocumentsMetadata(operation.metadata)

    # Handle the response
    return operation.operation.name







if __name__ == "__main__":

    import os
    from google.cloud import discoveryengine
    from google.api_core.client_options import ClientOptions
    # Replace with your project ID and location
    PROJECT_ID = "chatbot-poc-436512"
    DATASTORE_ID="eu-datastore-v2_1732559554898"
    LOCATION = "eu"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:/Projects/gcpServiceAccounts/chatbot-poc-436512-40e4b95f4ae7.json"
    source_documents_gs_uri = (
        "gs://pdf-bucket-11/Machine_Health_Monitoring_using_Fog_Computing.pdf"
    )
    print(" Starting loading data into datastore")
    import_documents(PROJECT_ID, LOCATION, DATASTORE_ID, source_documents_gs_uri)
    print(" Completed loading data into datastore")