
from yolo import detectPerson
from background import detectMovement


def detect(duration):
    movement = detectMovement(duration)
    person = detectPerson()

    return (movement or person)

detect(3)