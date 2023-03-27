import json
import gzip
import base64

def lambda_handler(event, context):
    output = []

    for record in event['records']:
        compressed_payload = base64.b64decode(record['data'])
        uncompressed_payload = gzip.decompress(compressed_payload)
        log_data = json.loads(uncompressed_payload)

        log_events = log_data.get('logEvents', [])

        for log_event in log_events:
            message = log_event.get('message', '')
            if message:
                try:
                    json_message = json.loads(message)
                    output_record = {
                        'recordId': record['recordId'],
                        'result': 'Ok',
                        'data': base64.b64encode(json.dumps(json_message).encode('utf-8')).decode('utf-8')
                    }
                except json.JSONDecodeError:
                    output_record = {
                        'recordId': record['recordId'],
                        'result': 'ProcessingFailed'
                    }
            else:
                output_record = {
                    'recordId': record['recordId'],
                    'result': 'ProcessingFailed'
                }
            output.append(output_record)
   return {'records': output}
