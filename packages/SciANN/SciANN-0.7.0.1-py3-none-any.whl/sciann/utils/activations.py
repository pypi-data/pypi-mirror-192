
from tensorflow import math as tf_math
from tensorflow.python.util.tf_export import keras_export
import keras as k
from keras import constraints
from keras import initializers
from keras import regularizers
from keras.utils import tf_utils
from tensorflow.python.keras.layers import InputSpec
from keras.initializers import Constant as default_constant_initializer


@keras_export('keras.activations.SciActivation')
class SciActivation(k.layers.Activation):
    """Applies an activation function to an output.

    # Arguments
        w0: The factor to be applied to initialized weights.
            e.g. sin(w0 * input)
        activation: name of activation function to use
            (see: [activations](../activations.md)),
            or alternatively, a TensorFlow operation.

    # Input shape
        Arbitrary. Use the keyword argument `input_shape`
        (tuple of integers, does not include the samples axis)
        when using this layer as the first layer in a model.

    # Output shape
        Same shape as input.
    """

    def __init__(self, w0=1.0, activation='linear', **kwargs):
        super(SciActivation, self).__init__(
            get_activation(activation),
            **kwargs
        )
        self.activation_name = self.activation.__name__
        self.w0 = w0

    def call(self, inputs):
        return self.activation(self.w0 * inputs)

    def get_config(self):
        config = {'w0': self.w0}
        base_config = super(SciActivation, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))


@keras_export('keras.layers.SciActivationLayer')
class SciActivationLayer(k.layers.Layer):
    """Applies an activation layer with trainable parameter to an output.

    # Arguments
        alpha: The trainable factor to be applied to initialized weights.
            e.g. sin(alpha * input)
        activation: name of activation function to use
            (see: [activations](../activations.md)),
            or alternatively, a TensorFlow operation.
        type: ('l', 'g') for locally or globally activation functions.

    # Input shape
        Arbitrary. Use the keyword argument `input_shape`
        (tuple of integers, does not include the samples axis)
        when using this layer as the first layer in a model.

    # Output shape
        Same shape as input.
    """

    def __init__(self, alpha=1.0, activation='linear', type='l', **kwargs):
        super(SciActivationLayer, self).__init__(**kwargs)
        self.activation = get_activation(activation)
        self.activation_name = self.activation.__name__
        self.alpha_initializer = default_constant_initializer(alpha)
        self.alpha_regularizer = None
        self.alpha_constraint = None
        self.shared_axes = None
        assert type in ('l', 'g')
        self.type = type

    @tf_utils.shape_type_conversion
    def build(self, input_shape):
        param_shape = list(input_shape[1:])
        if self.shared_axes is not None:
            for i in self.shared_axes:
                param_shape[i - 1] = 1
        self.alpha = self.add_weight(
            shape=param_shape if self.type=='l' else [1,],
            name='alpha',
            initializer=self.alpha_initializer,
            regularizer=self.alpha_regularizer,
            constraint=self.alpha_constraint)
        # Set input spec
        axes = {}
        if self.shared_axes:
            for i in range(1, len(input_shape)):
                if i not in self.shared_axes:
                    axes[i] = input_shape[i]
        self.built = True

    def call(self, inputs):
        return self.activation(self.alpha * inputs)

    def get_config(self):
        config = {
            'alpha_initializer': initializers.serialize(self.alpha_initializer),
            'alpha_regularizer': regularizers.serialize(self.alpha_regularizer),
            'alpha_constraint': constraints.serialize(self.alpha_constraint),
            'shared_axes': self.shared_axes
        }
        base_config = super(SciActivationLayer, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))

    @tf_utils.shape_type_conversion
    def compute_output_shape(self, input_shape):
        return input_shape


@keras_export('keras.layers.SciRowdyActivationLayer')
class SciRowdyActivationLayer(k.layers.Layer):
    """Adds multiple activations together.

    # Arguments
        activation: list of activations functions of class SciActivation or SciActivationLayer.

    # Output shape
        Same shape as input.
    """

    def __init__(self, phis, **kwargs):
        super(SciRowdyActivationLayer, self).__init__(**kwargs)
        self.phis = phis
        self.activation = None
        self.activation_name = "rowdy"
        self.alpha_initializer = default_constant_initializer(1.0/len(phis))
        self.alpha_regularizer = None
        self.alpha_constraint = None

    @tf_utils.shape_type_conversion
    def build(self, input_shape):
        for i, phi in enumerate(self.phis):
            self.add_weight(
                shape=[1, ],
                name=f'alpha{i}',
                initializer=self.alpha_initializer,
                regularizer=self.alpha_regularizer,
                constraint=self.alpha_constraint)
        self.built = True

    def call(self, inputs):
        sums = [a*f(inputs) for a, f in zip(self.weights, self.phis)]
        return tf_math.add_n(sums, name='rowdy_sum')

    def get_config(self):
        config = {
            'alpha_initializer': initializers.serialize(self.alpha_initializer),
            'alpha_regularizer': regularizers.serialize(self.alpha_regularizer),
            'alpha_constraint': constraints.serialize(self.alpha_constraint),
            'shared_axes': self.shared_axes
        }
        base_config = super(SciRowdyActivationLayer, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))

    @tf_utils.shape_type_conversion
    def compute_output_shape(self, input_shape):
        return input_shape


def get_activation(activation):
    """ Evaluates the activation function from a string or list of string inputs.

    # Arguments
        activation: A string pointing to the function name.

    # Returns:
        A function handle.
    """

    if isinstance(activation, list):
        return [get_activation(act) for act in activation]

    elif isinstance(activation, str):
        if hasattr(k.activations, activation):
            return getattr(k.activations, activation)
        elif hasattr(k.backend, activation):
            return getattr(k.backend, activation)
        elif hasattr(tf_math, activation):
            return getattr(tf_math, activation)
        else:
            raise ValueError(
                'Not a valid function name: ' + activation +
                ' - Please provide a valid activation '  
                'function name from tensorflow.python.keras or Tensorflow. '
            )

    elif callable(activation):
        return activation

    else:
        raise TypeError(
            'Please provide a valid input: ' + type(activation) +
            ' - Expecting a function name or function handle. '
        )


# not supported tensorflow >= 2.10
# k.utils.get_custom_objects().update({
#     'SciActivation': SciActivation
# })
