
import os

from pplns_python.api import PipelineApi

from yolov5processor import YoloV5Processor

def env(name : str) -> str:

  if name in os.environ:

    return os.environ[name]

  else: 

    raise Exception(f'Missng {name} in env.')

if __name__ == '__main__':

  api = PipelineApi(env('PPLNS_API'))

  p = YoloV5Processor(api)

  p.register_worker()

  stream = api.create_input_stream(
    {
      'taskId': env('PPLNS_TASK_ID'),
      'workerId': p.get_worker_id(),
    }
  )

  stream.on('data', p)


