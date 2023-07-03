import tensorflow as tf
import numpy
#print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))

print(tf.equal([0,0,0], [0,1,0]).numpy())