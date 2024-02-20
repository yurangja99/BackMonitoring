import win32gui
import cv2
import time
from face_detection import RetinaFace
from dataclasses import dataclass
from typing import Union

# windows utils

def get_active_window() -> int:
  """
  Get handler of active window.

  Returns:
      int: handler of current window
  """
  return win32gui.GetForegroundWindow()

def set_window_visibility(handler: Union[int, None], option: int) -> None:
  """
  If handler is not None, set visual option of it. 
  
  - SW_HIDE 0 보이지 않도록 한다.
  - SW_SHOWNORMAL 1 윈도우를 보이도록 하되 최대화 or 최소화 되어있다면 원래상태로 되돌린다.
  - SW_SHOWMINIMIZED 2 윈도우를 활성화 하고 최소화 한다.
  - SW_MAXIMIZE 3 최대화 한다.
  - SW_SHOWNOACTIVATE 4 윈도우를 보이도록 하지만 활성화 하지 않는다.
  - SW_SHOW 5 윈도우를 보이도록 한다.
  - SW_MINIMIZE 6 최소화 한 후 이전 윈도우를 활성화한다.
  - SW_SHOWMINNOACTIVE 7 윈도우를 최소화 하지만 활성화 하지는 않는다.
  - SW_SHOWNA 8 윈도우를 보이도록 하지만 활성화 하지는 않는다.
  - SW_RESTORE 9 원 상태로 되돌린다.
  - SW_SHOWDEFAULT 10 윈도우 생성시의 Flag 값에 따라 설정합니다.
  - SW_FORCEMINIMIZE 11 최소화 한다.

  Args:
      handler (Union[int, None]): handler
      option (int): refer to the function description.
  """
  if handler is not None:
    win32gui.ShowWindow(handler, option)

# configs

@dataclass
class Config:
  gpu_id: int=-1
  cam: int=0
  vis: bool=True

if __name__ == "__main__":
  # config
  config = Config(gpu_id=0, cam=0)
  
  # video capture
  capture = cv2.VideoCapture(config.cam)
  if not capture.isOpened():
    raise IOError("Cannot open webcam")
  
  # face detector
  face_detector = RetinaFace(gpu_id=config.gpu_id)
  
  # print config
  print("Config:", config)
  print("Face detector on:", face_detector.device)
  
  # main loop
  prev_time = 0.0
  curr_time = time.time()
  while True:
    # get frame
    success, frame = capture.read()
    if not success:
      raise IOError("Cannot get frame")
    
    # get faces
    faces = face_detector(frame)
    faces = list(filter(lambda face: face[2] > 0.5, faces))
    
    if config.vis:
      # update timestamp
      prev_time = curr_time
      curr_time = time.time()
      
      # visualize
      for box, landmark, score in faces:
        x_min, y_min, x_max, y_max = max(int(box[0]), 0), max(int(box[1]), 0), int(box[2]), int(box[3])
        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 1)
      cv2.putText(frame, f"FPS: {1.0 / (curr_time - prev_time):.2f}", (10, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 1, cv2.LINE_AA)
      cv2.putText(frame, f"FACES: {len(faces)}", (10, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 1, cv2.LINE_AA)
      cv2.imshow(f"Device: {face_detector.device}", frame)
      
      # break: press q
      if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    
    # break: number of faces exceeds 1.
    if len(faces) > 1:
      print("Bye!")
      current_window_handler = get_active_window()
      set_window_visibility(current_window_handler, 11)
      break
