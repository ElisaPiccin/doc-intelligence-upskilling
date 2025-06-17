"""
FILE: sample_analyze_batch_documents.py
SOURCE: https://github.com/Azure/azure-sdk-for-python/blob/azure-ai-documentintelligence_1.0.0/sdk/documentintelligence/azure-ai-documentintelligence/samples/sample_analyze_batch_documents.py
with minor modifications for training purposes.

DESCRIPTION:
    This sample demonstrates how to analyze documents in a batch.

    This sample uses Layout model to demonstrate.

    Add-on capabilities accept a list of strings containing values from the `DocumentAnalysisFeature`
    enum class. For more information, see:
    https://aka.ms/azsdk/python/documentintelligence/analysisfeature.

    The following capabilities are free:
    - BARCODES
    - LANGUAGES

    The following capabilities will incur additional charges:
    - FORMULAS
    - OCR_HIGH_RESOLUTION
    - STYLE_FONT
    - QUERY_FIELDS

    See pricing: https://azure.microsoft.com/pricing/details/ai-document-intelligence/.

USAGE:
    python sample_analyze_batch_documents.py

    While generating the SAS tokens, set the permissions you need:
    - at least Read, List, Write for the result container
    - at least Read, List for the source container

    Can be used with a SINGLE-SERVICE or with a MULTI-SERVICE Document Intelligence deployment in Azure.

    Set the environment variables with your own values before running the sample:
    1) AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT - the endpoint to your Document Intelligence resource.
    2) AZURE_DOCUMENT_INTELLIGENCE_KEY - your Document Intelligence API key.
    3) RESULT_CONTAINER_SAS_URL - the SAS URL to the result container where the analysis results will be stored.
    4) SOURCE_DATA_CONTAINER_SAS_URL - the SAS URL to the source data container where the documents to be analyzed are stored.
"""

import os


def analyze_batch_docs():
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.documentintelligence import DocumentIntelligenceClient
    from azure.ai.documentintelligence.models import (
        AnalyzeBatchDocumentsRequest,
        AzureBlobContentSource,
    )

    endpoint = os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
    key = os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]
    result_container_sas_url = os.environ["RESULT_CONTAINER_SAS_URL"]
    batch_training_data_container_sas_url = os.environ["SOURCE_DATA_CONTAINER_SAS_URL"]

    document_intelligence_client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    request = AnalyzeBatchDocumentsRequest(
        result_container_url=result_container_sas_url,
        azure_blob_source=AzureBlobContentSource(
            container_url=batch_training_data_container_sas_url,
        ),
    )
    poller = document_intelligence_client.begin_analyze_batch_documents(
        model_id="prebuilt-layout",
        body=request,
    )
    continuation_token = poller.continuation_token()  # a continuation token that allows to restart the poller later.
    poller2 = document_intelligence_client.get_analyze_batch_result(continuation_token)
    if poller2.done():
        final_result = poller2.result()
        print(f"Succeeded count: {final_result.succeeded_count}")
        print(f"Failed count: {final_result.failed_count}")
        print(f"Skipped count: {final_result.skipped_count}")
    else:
        print("The batch analyze is in process... Check your result container later!")


if __name__ == "__main__":
    from azure.core.exceptions import HttpResponseError
    from dotenv import find_dotenv, load_dotenv

    try:
        load_dotenv(find_dotenv(), override=True)
        azure_docintelligence_endpoint = os.environ.get('AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT')
        print(f'Current endpoint: {azure_docintelligence_endpoint}')
        analyze_batch_docs()
    except HttpResponseError as error:
        # Examples of how to check an HttpResponseError
        # Check by error code:
        if error.error is not None:
            if error.error.code == "InvalidImage":
                print(f"Received an invalid image error: {error.error}")
            if error.error.code == "InvalidRequest":
                print(f"Received an invalid request error: {error.error}")
            # Raise the error again after printing it
            raise
        # If the inner error is None and then it is possible to check the message to get more information:
        if "Invalid request".casefold() in error.message.casefold():
            print(f"Uh-oh! Seems there was an invalid request: {error}")
        # Raise the error again
        raise
