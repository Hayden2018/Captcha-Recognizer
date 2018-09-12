Captcha Recognizer is a simple Python program using convolutional neural networks to recognize words in a specific type of Captcha. 
It is implemented using Pytorch. The targeted captcha are those found on : https://w6.ab.ust.hk/fbs_user/html/main.htm<br><br>
The current best weight for the model has around 80% accuracy by each character and 33% full correct accuracy.<br><br>
The model is first trained on ten thousands of generated sample which is similar to true captcha with auto generated labels. 
After that, I manually label a few hundreds true captcha and for further adjust of the parameters of the model. 
Without the generator, I need to manually labels a several thousands of labels to get the model to work.<br><br>
Training use auto-encoder for regularization with data pre-processing.
#
<b>captcha_reducer.py</b> : This script is for pre-processing the input image.<br>
<b>Models.py</b> : This file define the three neural models in this program. Including encoder, decoder and classifier.<br>
<b>ModelTrain.py</b> : This script is for training the models on generated sample. Written for two GPU.<br>
<b>ModelTransfer.py</b> : This script is for training the models on true data. Written for two GPU.<br>
<b>ModelTest.py</b> : This script is for testing the accuracy of the model with GPU.
It should be place in the same directory as Models.py and parameter files.<br>
<b>Recognizer.py</b> : This file contain the function recognize which act as a API. 
It in-take the captcha to be recognized as Pytorch tensor and return the recognized result as string.<br>
<b>DataProcessing.py</b> : This file contain functions that are used to prepare data for training.<br>
<b>Generator/</b> : This directory contain the sample generator.<br>
<b>Cls_param</b> : Parameters for the classification network.<br>
<b>Net_param</b> : Parameters for the encoder network.<br>
<b>Decode_param</b> : Parameters for the decoder network. (Only used during training for regularization purpose)<br>
