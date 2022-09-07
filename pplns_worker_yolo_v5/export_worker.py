
import json
from yolov5processor import yolov5worker

if __name__ == '__main__':

  open(
    './pplns_workers/{}.json'.format(
      yolov5worker['_id']
    ),
    'w'
  ).write(
    json.dumps(yolov5worker, indent=2)
  )
