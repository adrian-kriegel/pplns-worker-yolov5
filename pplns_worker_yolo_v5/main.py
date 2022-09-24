
import time

from pplns_python.api import PipelineApi
from s3_util import S3UrlSigner

from yolov5processor import YoloV5Processor
from util import env

if __name__ == '__main__':

  from dotenv import load_dotenv

  load_dotenv()

  api = PipelineApi(env('PPLNS_API'))

  p = YoloV5Processor(api)

  p.url_signer = S3UrlSigner()

  p.register_worker()

  stream = api.create_input_stream(
    {
      'taskId': env('PPLNS_TASK_ID'),
      'workerId': p.get_worker_id(),
    }
  )

  stream.on_data(p)
  stream.start()

  while True:

    time.sleep(1)

