from .catr import Catr


def catr(request):
    return {'catr': Catr(request)}