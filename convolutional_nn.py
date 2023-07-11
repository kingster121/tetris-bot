# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 18:31:19 2022

@author: General
"""

import tensorflow as tf


# Use MNIST dataset
mnist = tf.keras.datasets.mnist
(xtrain, ytrain), (xtest, ytest) = mnist.load_data()

# Normalize colour space
xtrain, xtest = xtrain/255.0, xtest/255.0

print("categorical labels")
print(ytrain[0:5])
# make labels one hot encoded
ytrain = tf.one_hot(ytrain, 10)
ytest = tf.one_hot(ytest, 10)
print("one hot encoded labels")
print(ytrain[0:5])


# Create batches for our datasets
train_ds = tf.data.Dataset.from_tensor_slices((xtrain, ytrain)).batch(50)
test_ds = tf.data.Dataset.from_tensor_slices((xtest, ytest)).batch(50)


from tensorflow.keras.layers import Flatten

# Original shape is (28x28) per image
print(xtrain.shape)
flatten = Flatten(dtype ='float32')
# New shape is (784)
print(flatten(xtrain).shape)


# Create weights and biases tensor
# Takes in 784 pixel values, returns 10
W = tf.Variable(tf.zeros([784, 10]),tf.float32)
# Simply adds so no. of pixels stay the same
b = tf.Variable(tf.zeros([10]), tf.float32)

def dummySoftmax():
	# a sample softmax calculation on an input vector
	vector = [10, 0.2, 8]
	softmax = tf.nn.softmax(vector)
	print("softmax calculation")
	print(softmax.numpy())
	print("Check if all probabilities add up to 1")
	print(tf.reduce_sum(softmax))
	print("finding vector with largest value (label assignment)")
	print("category", tf.argmax(softmax).numpy())

dummySoftmax()



def forward(x):
	return tf.matmul(x,W)+b

def activate(x):
	return tf.nn.softmax(forward(x))

def model(x):
	x = flatten(x)
	return(activate(x))

# Using CrossEntropy cost function
# The cost increases exponentially with lower correct label probability.
def cross_entropy(y_label, y_pred):
	# Add 1.e^-10 to prevent errors when y_pred = 0
	return(-tf.reduce_sum(y_label * tf.math.log(y_pred + 1.e-10)))

optimizer = tf.keras.optimizers.SGD(learning_rate = 0.25)

def train_step(x,y):
	with tf.GradientTape() as tape:
		# Compute loss
		current_loss = cross_entropy(y, model(x))
		# Gets the rate of change of loss with respect to [weights, bias]
		grads = tape.gradient(current_loss, [W,b])
		# Adjust W,b values based on gradients
		optimizer.apply_gradients(zip(grads, [W,b]))
	return current_loss.numpy()


loss_values=[]
accuracies = []
epochs = 10

def trainModel():
	for i in range(epochs):
		j = 0
		for x_train_batch, y_train_batch in train_ds:
			j+=1
			current_loss = train_step(x_train_batch, y_train_batch)
			if j%500 == 0:
				print("epoch", str(i), "batch",+j,"loss",str(current_loss))


		current_loss = cross_entropy(ytrain, model(xtrain)).numpy()
		loss_values.append(current_loss)
		# Returns a truth matrix of model(x) prediction vs actual ytrain values
		correct_prediction = tf.equal(tf.argmax(model(xtrain), axis=1),
								   tf.argmax(ytrain, axis=1))

		accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32)).numpy()
		accuracies.append(accuracy)
		print("end of epoch", str(i),"loss",str(current_loss), "accuracy:", str(accuracy))


trainModel()

correct_prediction_train = tf.equal(tf.argmax(model(xtrain), axis=1),
									tf.argmax(ytrain,axis=1))
accuracy_train = tf.reduce_mean(tf.cast(correct_prediction_train, tf.float32)).numpy()

correct_prediction_test = tf.equal(tf.argmax(model(xtest), axis=1),
								   tf.argmax(ytest, axis=1))
accuracy_test = tf.reduce_mean(tf.cast(correct_prediction_test, tf.float32)).numpy()

print("training accuracy", accuracy_train)
print("test accuracy", accuracy_test)



import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = (10, 6)
#print(loss_values)
plt.plot(loss_values,'-ro')
plt.title("loss per epoch")
plt.xlabel("epoch")
plt.ylabel("loss")
plt.show()

plt.plot(accuracies,'-ro')
plt.title("accuracy per epoch")
plt.xlabel("epoch")
plt.ylabel("accuracy")