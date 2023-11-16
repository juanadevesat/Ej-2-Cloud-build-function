from google.cloud import storage, firestore
import json


def frombuckettofirestore(event, context):
     """Triggered by a change to a Cloud Storage bucket.
     Args:
          event (dict): Event payload.
          context (google.cloud.functions.Context): Metadata for the event.
     """
     file = event

     # Inicia cliente de GC storage y especifica el bucket y el fichero
     storage_client = storage.Client()
     bucket = storage_client.get_bucket('bucket-juan-ejercicio-final')
     blob = bucket.blob(str(file['name']))

     # Descarga los contenidos del blob como un string y lo carga usando el metodo using json.loads()
     data = json.loads(blob.download_as_string(client=None))

     # Agrega data a firestore
     db = firestore.Client()
     db.collection("firestore-juan-ejercicio-final").document(str(data['ID'])).set(data)
