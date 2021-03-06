from builtins import object
import numpy as np

from cs231n.layers import *
from cs231n.fast_layers import *
from cs231n.layer_utils import *


class ThreeLayerConvNet(object):
    """
    A three-layer convolutional network with the following architecture:

    conv - relu - 2x2 max pool - affine - relu - affine - softmax

    The network operates on minibatches of data that have shape (N, C, H, W)
    consisting of N images, each with height H and width W and with C input
    channels.
    """

    def __init__(self, input_dim=(3, 32, 32), num_filters=32, filter_size=7,
                 hidden_dim=100, num_classes=10, weight_scale=1e-3, reg=0.0,
                 dtype=np.float32):
        """
        Initialize a new network.

        Inputs:
        - input_dim: Tuple (C, H, W) giving size of input data
        - num_filters: Number of filters to use in the convolutional layer
        - filter_size: Size of filters to use in the convolutional layer
        - hidden_dim: Number of units to use in the fully-connected hidden layer
        - num_classes: Number of scores to produce from the final affine layer.
        - weight_scale: Scalar giving standard deviation for random initialization
          of weights.
        - reg: Scalar giving L2 regularization strength
        - dtype: numpy datatype to use for computation.
        """
        self.params = {}
        self.reg = reg
        self.dtype = dtype

        ############################################################################
        # TODO: Initialize weights and biases for the three-layer convolutional    #
        # network. Weights should be initialized from a Gaussian with standard     #
        # deviation equal to weight_scale; biases should be initialized to zero.   #
        # All weights and biases should be stored in the dictionary self.params.   #
        # Store weights and biases for the convolutional layer using the keys 'W1' #
        # and 'b1'; use keys 'W2' and 'b2' for the weights and biases of the       #
        # hidden affine layer, and keys 'W3' and 'b3' for the weights and biases   #
        # of the output affine layer.                                              #
        ############################################################################
        C, H, W = input_dim
        W1 = np.random.normal(scale = weight_scale, size = (num_filters, C, filter_size, filter_size))
        W2 = np.random.normal(scale = weight_scale, size = (num_filters * (H//2) * (W//2), hidden_dim))
        W3 = np.random.normal(scale = weight_scale, size = (hidden_dim, num_classes))
        b1 = np.zeros(num_filters)
        b2 = np.zeros(hidden_dim)
        b3 = np.zeros(num_classes)
        self.params["W1"] = W1 
        self.params["W2"] = W2 
        self.params["W3"] = W3 
        self.params["b1"] = b1 
        self.params["b2"] = b2 
        self.params["b3"] = b3 
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        for k, v in self.params.items():
            self.params[k] = v.astype(dtype)


    def loss(self, X, y=None):
        """
        Evaluate loss and gradient for the three-layer convolutional network.

        Input / output: Same API as TwoLayerNet in fc_net.py.
        """
        W1, b1 = self.params['W1'], self.params['b1']
        W2, b2 = self.params['W2'], self.params['b2']
        W3, b3 = self.params['W3'], self.params['b3']

        # pass conv_param to the forward pass for the convolutional layer
        filter_size = W1.shape[2]
        conv_param = {'stride': 1, 'pad': (filter_size - 1) // 2}

        # pass pool_param to the forward pass for the max-pooling layer
        pool_param = {'pool_height': 2, 'pool_width': 2, 'stride': 2}

        scores = None
        ############################################################################
        # TODO: Implement the forward pass for the three-layer convolutional net,  #
        # computing the class scores for X and storing them in the scores          #
        # variable.                                                                #
        ############################################################################
        pass
        N, C, H, W = X.shape
        num_filters = W1.shape[0]
        pool_out, pool_cache = conv_relu_pool_forward(X, W1, b1, conv_param, pool_param)
        relu_out, relu_cache = affine_relu_forward(pool_out.reshape(N, -1), W2, b2)
        affine_out, affine_cache = affine_forward(relu_out, W3, b3)
        scores = affine_out
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        if y is None:
            return scores

        loss, grads = 0, {}
        ############################################################################
        # TODO: Implement the backward pass for the three-layer convolutional net, #
        # storing the loss and gradients in the loss and grads variables. Compute  #
        # data loss using softmax, and make sure that grads[k] holds the gradients #
        # for self.params[k]. Don't forget to add L2 regularization!               #
        ############################################################################
        data_loss, dL = softmax_loss(scores, y)
        reg_loss = 0.5 * self.reg * np.sum(W1**2) + 0.5 * self.reg * np.sum(W2**2) + 0.5 * self.reg * np.sum(W3**2) 
        loss = data_loss + reg_loss
        affine_dx, affine_dw, affine_db = affine_backward(dL, affine_cache) 
        relu_dx, relu_dw, relu_db = affine_relu_backward(affine_dx, relu_cache)
        conv_dx, conv_dw, conv_db = conv_relu_pool_backward(relu_dx.reshape(pool_out.shape), pool_cache)

        grads["W1"] = conv_dw
        grads["b1"] = conv_db
        grads["W2"] = relu_dw
        grads["b2"] = relu_db
        grads["W3"] = affine_dw
        grads["b3"] = affine_db
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        return loss, grads
