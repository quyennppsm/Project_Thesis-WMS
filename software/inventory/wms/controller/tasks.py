from wms.celery import app
from controller.models import ABC
import skfuzzy.control as ctrl
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 

@app.task
def task_fuzzy():
    print ("summoning twilight caller")
    return "[fuzzy]"
