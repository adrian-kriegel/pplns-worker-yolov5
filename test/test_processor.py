
import os
import typing

from pplns_worker_yolo_v5.yolov5processor import \
  YoloV5Processor

from pplns_python.testing_utils import \
  TestPipelineApi as PipelineApi, \
  mock_prepared_input

from pplns_python.processor import \
  PreparedInput

def test_processing():

  api = PipelineApi()

  process = YoloV5Processor(api)

  imgs = [
    os.path.join(os.path.dirname(__file__), 'sample-data/img-01.jpg'),
    os.path.join(os.path.dirname(__file__), 'sample-data/img-02.jpg'),
  ]

  items : list[typing.Any] = [
    {
      'data': 
      [
        { 's3Url': url }
      ]
    } for url in imgs
  ]

  inputs : list[PreparedInput] = [
    {
      **mock_prepared_input,
      'inputs': { 'image': item }
    }
    for item in items
  ]

  results = process(inputs)

  assert len(results) == len(inputs)

  assert 'boxes' in results[0]
  assert 'boxes' in results[1]

  for result in results:

    data = result['boxes']['data']

    assert type(data) == list or \
      type(data) == tuple

    for box in data:

      # should be x,y,x,y,conf,class_idx,class_name
      assert [type(v) for v in box] == [float, float, float, float, float, int, str]
