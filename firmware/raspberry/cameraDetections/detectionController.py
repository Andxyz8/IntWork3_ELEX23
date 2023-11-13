
from yolo import detectPerson
from background import detectMovement
from distanceEstimation import detectAruco
from yolo8.yolov8 import detectPersonV8


def detect(duration):
    movement = detectMovement(duration)
    # person = detectPerson()
    person = detectPersonV8()

    return (movement or person)

def detectMarker():
    return detectAruco()
