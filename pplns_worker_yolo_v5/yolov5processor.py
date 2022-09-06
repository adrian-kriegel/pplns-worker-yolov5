
import torch

from pplns_types import \
  WorkerWrite, \
  Worker

from pplns_python.processor import \
  PreparedInput, \
  BatchProcessor, \
  ProcessorOutput

from pplns_python.api import PipelineApi

yolov5worker : WorkerWrite = {

  "key": "worker_yolo_v5",

  "title": "YOLO V5",

  "description": "Detect objects using YOLO V5.",

  "inputs": 
  {
    "image":
    {
      'type': "object",
      'properties': 
      {
        's3Url': { 'type': 'string' }
      }
    }
  },

  "outputs": 
  {
    "boxes": 
    {
      "description": "(x, y, x, y, conf., class_idx, class_name) for each box",
      "type": "array",
      "items":
      {
        "type": "array",
      }
    }
  },

  "params": 
  {
    "model":
    {
      "type": "string",
      "default": "ultralytics/yolov5 yolov5s"
    }
  },
}

class YoloV5Processor(BatchProcessor):

  worker : Worker | None = None

  def __init__(
    self,
    api : PipelineApi,
    **params
  ):

    self.api = api

    model_src = ('ultralytics/yolov5', 'yolov5s')

    if 'model' in params:

      model_src = params['model'].split(' ')

    self.model = torch.hub.load(
      model_src[0],
      model_src[1],
      pretrained=True,
    )

  def register_worker(self):

    self.worker = self.api.register_worker(yolov5worker)

    return self.worker

  def get_worker_id(self) -> str:

    if self.worker:

      return self.worker['_id']

    else:

      raise Exception('Worker has not been registered.')

  def process_urls(
    self,
    urls : list[str]
  ) -> list[ProcessorOutput]:

    dfs = self.model(urls).pandas().xyxy

    return [
      {
        'boxes': 
        {
          'data': list(df.itertuples(index=False, name=None))
        }
      } 
      for df in dfs
    ]

  def __call__(
    self,
    inputs : list[PreparedInput],
  ) -> list[ProcessorOutput]:

    urls = [
      inp["inputs"]['image']["data"][0]['s3Url']
      for inp in inputs
    ]

    return self.process_urls(urls)
      
    



      


