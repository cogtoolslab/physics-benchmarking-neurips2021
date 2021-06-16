import boto3
import logging
from pathlib import Path
from botocore.exceptions import ClientError
from boto3.s3.transfer import TransferConfig
from hurry.filesize import size, si
import errno
import sys, os
import threading
import ntpath

# to log progress
log = logging.getLogger('s3_uploader')
log.setLevel(logging.INFO)
format = logging.Formatter("%(asctime)s: - %(levelname)s: %(message)s", "%H:%M:%S")
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(format)
log.addHandler(stream_handler)

MP_THRESHOLD = 1
MP_CONCURRENCY = 10
MAX_RETRY_COUNT = 3

s3_client = None


class ProgressPercentage(object):
    def __init__(self, filename):
        self._filename = filename
        self._size = float(Path(filename).stat().st_size)
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write("\r%s  %s / %s  (%.2f \%)" % (ntpath.basename(self._filename), size(self._seen_so_far), size(self._size), percentage))
            sys.stdout.flush()


def login():
    global s3_client
    s3_client = boto3.client('s3')

def upload_file_multipart(file, bucket, object_path, metadata=None):
    log.info("Uploading [" + file + "] to [" + bucket + "] bucket ...")
    log.info("S3 path: [ s3://" + bucket + "/" + object_path + " ]")

    if not Path(file).is_file:
        log.error("File [" + file + "] does not exist!")
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file)

    if object_path is None:
        log.error("object_path is null!")
        raise ValueError("S3 object must be set!")

    GB = 1024 ** 3
    mp_threshold = MP_THRESHOLD * GB
    concurrency = MP_CONCURRENCY
    transfer_config = TransferConfig(multipart_threshold=mp_threshold,
                                     use_threads=True,
                                     max_concurrency=concurrency)

    login_attempt = False
    retry = MAX_RETRY_COUNT

    while retry > 0:
        try:
            s3_client.upload_file(file, bucket, object_path, Config=transfer_config,
                                  ExtraArgs=metadata, Callback=ProgressPercentage(file))
            sys.stdout.write('\n')
            log.info("File [" + file + "] uploaded successfully")
            log.info("Object name: [" + object_path + "]")
            retry = 0

        except ClientError as e:
            log.error("Failed to upload object!")
            log.exception(e)
            if e.response['Error']['Code'] == 'ExpiredToken':
                log.warning('Login token expired')
                retry = 1
                log.debug("retry = " + str(retry))
                login_attempt = True
                login()
            else:
                log.error("Unhandled error code:")
                log.debug(e.response['Error']['Code'])
                raise

        except boto3.exceptions.S3UploadFailedError as e:
            log.error("Failed to upload object!")
            log.exception(e)
            if 'ExpiredToken' in str(e):
                log.warning('Login token expired')
                log.info("Handling...")
                retry -= 1
                log.debug("retry = " + str(retry))
                login_attempt = True
                login()
            else:
                log.error("Unknown error!")
                raise

        except Exception as e:
            log.error("Unknown exception occurred!")
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(e).__name__, e.args)
            log.debug(message)
            log.exception(e)
            raise

    if login_attempt:
        raise Exception("Tried to login " + str(MAX_RETRY_COUNT) + " times but failed to upload!")

def main(args):
    login()
    filename = args[0]
    bucket = args[1]
    if len(args) > 2:
        object_path = args[2]
    else:
        object_path = filename.split('/')[-1]
    upload_file_multipart(filename, bucket, object_path, metadata=None)
    log.info("Upload finished!")

if __name__ == '__main__':
    main(sys.argv[1:])
