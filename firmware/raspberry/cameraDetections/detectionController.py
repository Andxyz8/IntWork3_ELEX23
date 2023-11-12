
from yolo import detectPerson
from background import detectMovement
from distanceEstimation import detectAruco


def detect(duration):
    movement = detectMovement(duration)
    person = detectPerson()

    return (movement or person)

def detectMarker():
    return detectAruco()