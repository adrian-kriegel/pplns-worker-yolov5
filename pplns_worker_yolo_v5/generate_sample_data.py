
import json
import os 

import typing

from yolov5processor import YoloV5Processor

if __name__ == '__main__':

  api : typing.Any = None

  processor = YoloV5Processor(api)

  sample_data_dir = os.path.join(
    os.path.dirname(__file__), 
    '../test/sample-data/'
  )

  imgs = [
    os.path.join(
      sample_data_dir,
      'img-01.jpg'
    ),
    os.path.join(
      sample_data_dir,
      'img-02.jpg'
    ),
  ]

  results = processor.process_urls(imgs)

  for i,result in enumerate(results):

    open(
      os.path.join(
        sample_data_dir,
        f"img-0{i+1}.json"
      ),
      'w'
    ).write(json.dumps(result['boxes']))


