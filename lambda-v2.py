import base64
import gzip
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Process each record in the event
    output_records = []
    for record in event['records']:
        try:
            # Decode the base64-encoded data
            payload = base64.b64decode(record['data'])

            # Decompress the Gzip-encoded data
            decompressed_payload = gzip.decompress(payload)

            # Convert the payload to a JSON object
            json_payload = json.loads(decompressed_payload)

            # Perform any transformations on the payload here
            transformed_payload = json_payload

            # Re-encode the payload in Gzip and base64 formats
            compressed_payload = gzip.compress(bytes(json.dumps(transformed_payload), 'utf-8'))
            encoded_payload = base64.b64encode(compressed_payload).decode('utf-8')

            # Update the record with the transformed and encoded data
            output_record = {
                'recordId': record['recordId'],
                'result': 'Ok',
                'data': encoded_payload
            }
            output_records.append(output_record)
        except Exception as e:
            # Log the error and mark the record as failed
            logger.error(f'Error processing record {record["recordId"]}: {e}')
            output_record = {
                'recordId': record['recordId'],
                'result': 'ProcessingFailed',
                'data': record['data']
            }
            output_records.append(output_record)

    # Return the transformed records
    return {'records': output_records}
