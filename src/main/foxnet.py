import tensorflow as tf
from functools import partial

xavier = tf.contrib.layers.xavier_initializer

class FoxNet(object):

    def fully_connected(self, X, y, n_labels):
        # Flatten: 48 x 64 x 3
        flattened_size = 48 * 64 * 3
        flattened = tf.reshape(X, [-1, flattened_size])

        # Fully connected layer
        affine_relu = tf.layers.dense(inputs=flattened, units=1024, activation=tf.nn.relu)

        # Logits Layer
        y_out = tf.layers.dense(inputs=affine_relu, units=n_labels)
        return y_out

    def simple_cnn(self, X, y, filter_size, n_filters, n_labels, is_training):
        # Input Layer [batch_size, image_width, image_height, channels]
        input_layer = X

        # Convolutional Layer + ReLU 1
        conv1 = tf.layers.conv2d(
            inputs=input_layer,
            filters=n_filters,
            kernel_size=filter_size,
            padding="same",
            activation=tf.nn.relu
        )

        # Batch norm 1
        norm1 = tf.layers.batch_normalization(
            conv1,
            axis=-1, 
            momentum=0.99,
            epsilon=0.001,
            training=is_training
        )

        # Convolutional Layer + ReLU 2
        conv2 = tf.layers.conv2d(
            inputs=norm1,
            filters=n_filters,
            kernel_size=n_filters + 2,
            padding="same",
            activation=tf.nn.relu
        )

        # Batch norm 2
        norm2 = tf.layers.batch_normalization(
            conv2,
            axis=-1, 
            momentum=0.99,
            epsilon=0.001,
            training=is_training
        )

        # Max pooling --> 24x32x32
        pool = tf.layers.max_pooling2d(inputs=norm2, pool_size=[2, 2], strides=2)

        # # Affine + ReLU
        magic_number = 24576 # TODO: What should this number be?
        pool_flat = tf.reshape(pool, [-1, magic_number]) 
        affine_relu = tf.layers.dense(inputs=pool_flat, units=1024, activation=tf.nn.relu)

        # Dropout
        dropout = tf.layers.dropout(inputs=affine_relu, rate=0.5, training=is_training)

        # Logits Layer
        y_out = tf.layers.dense(inputs=dropout, units=n_labels)
        return y_out
