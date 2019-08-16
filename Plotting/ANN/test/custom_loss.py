import tensorflow as tf
import keras.backend as K

###############################################################################
# Custom loss functions
#######################

# https://towardsdatascience.com/handling-imbalanced-datasets-in-deep-learning-f48407a0e758
def focal_loss(y_true, y_pred):
    gamma = 0.1 #2.0
    alpha = 0.95 #0.25 #0.95
    pt_1 = tf.where(tf.equal(y_true, 1), y_pred, tf.ones_like(y_pred))
    pt_0 = tf.where(tf.equal(y_true, 0), y_pred, tf.zeros_like(y_pred))
    return(-K.sum(alpha * K.pow(1. - pt_1, gamma) * K.log(pt_1))-K.sum((1-alpha) * K.pow( pt_0, gamma) * K.log(1. - pt_0)))

# signal efficiency
def sig_loss(y_true, y_pred):
    #for (signal):
    #    loss +=  (s / sqrt(7*b)) )**2;
    #loss = math.sqrt(1/loss);
    pt_1 = tf.where(tf.equal(y_true, 1), y_pred, tf.ones_like(y_pred))
    pt_0 = tf.where(tf.equal(y_true, 0), y_pred, tf.zeros_like(y_pred))
    sig = K.sum(((1.-pt_1) / K.pow(7*(1-pt_0), 0.5))**2)
    loss = K.pow(1/sig, 0.5)
    return(loss)

# signal efficiency
def sig_eff(y_true, y_pred):
    #for (signal):
    #    loss +=  (s / sqrt(7*b)) )**2;
    #loss = math.sqrt(1/loss);
    #pt_1 = tf.where(tf.equal(y_true, 1), y_pred, tf.ones_like(y_pred))
    #pt_0 = tf.where(tf.equal(y_true, 0), y_pred, tf.zeros_like(y_pred))
    #sig_eff = K.pow(K.sum((pt_1 / K.pow(7*(1-pt_0), 0.5))**2), 0.5)
    sig = tf.where(tf.equal(y_true, 1), y_pred, tf.zeros_like(y_pred))
    bkg = tf.where(tf.equal(y_true, 0), y_pred, tf.ones_like(y_pred))
    sig = K.sum(sig)
    bkg = K.sum(1-bkg)
    sig_eff = sig/K.pow(bkg, 0.5)
    return(1/sig_eff)

###############################################################################
