Initial input layers
model.add(tf.keras.layers.Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)))
- Takes 5s per epoch but resulrs in 0.9514 acc and 0.1767 loss

model.add(tf.keras.layers.Input(shape=(IMG_WIDTH, IMG_HEIGHT, 3)))
- Takes 2 s per Epoch, 0.8482 acc and 0.4867 loss

Adding additional layers does not have a large effect on acuracy, but reducing to 2 does

Changing dropout to 0.05 = accuracy: 0.8847 - loss: 0.4967
0.1 -accuracy: 0.8867 - loss: 0.4121
0.3 0.8411 - loss: 0.5136
0.9 accuracy: 0.0559 - loss: 3.4983


