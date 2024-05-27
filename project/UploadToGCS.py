import os
from datetime import datetime, timezone
import time
from google.cloud import storage

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'sa.json'

def upload_file_from_local(bucket_name):
    files = [
        f
        for f in os.listdir(".")
        if os.path.isfile(f) and f.endswith((".pcap", ".pcapng"))
    ]
    content = max(files, key=os.path.getctime)
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(content)
    blob.upload_from_filename(content, timeout=300)
    print(
        f"{content} uploaded to GCS."
    )

    current_time = datetime.now(timezone.utc)

    # Set the start time for looping
    start_time = time.time()
    # Define the maximum duration for running the loop (in seconds)
    max_duration = 60

    # Loop for a maximum of 1 minute
    while (time.time() - start_time) < max_duration:
        blobs = [i.name for i in bucket.list_blobs() if (current_time - i.time_created).total_seconds() < 120]

        if 'json/ip_placeholder.json' in blobs:
            blob1 = bucket.blob('json/ip_placeholder.json')
            blob1.download_to_filename('ip_placeholder.json')
            print(f"File ip_placeholder.json downloaded.")
            return

        # Wait for 5 seconds before running the loop again
        time.sleep(5)

upload_file_from_local('test-bucket-23432')
