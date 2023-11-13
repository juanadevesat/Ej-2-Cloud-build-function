import json

def pruebacloudbuild(event, context):
    """Triggered by a change to a Cloud Storage bucket.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    file = event
    data = json.load(file)
    print(f"Processing file: {file['name']}.")
    print(data)