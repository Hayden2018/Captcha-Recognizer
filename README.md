Captcha Recognizer is a simple Python program using convolutional neural networks to recognize words in a specific type of Captcha. 
It is implemented using Pytorch. The targetted captcha are those found on : https://w6.ab.ust.hk/fbs_user/html/main.htm<br><br>
The current weight best weight for the model has around 80% accuracy by each character and 33% full correct accuracy.<br><br>
The model is first trained on ten thousands of generated sample which is similar to true captcha with auto generated labels. After that, I manually label a few hundreds true captcha and for further adjust the parameters of the model. Without the generator, I need to manually labels a serveral thousands of labels to get the model to work.
#
<b>captcha_reducer.py</b> : This script is for preprocessing the input image.<br>
<b>Models.py</b> : This file define the three neural models in this program. Including encoder, decoder and classifier.<br>
<b>ModelTrain.py</b> : This script is for training the models. 
The resulting weight dictionary will be saved in the same directory as this script.<br>
<b>ModelTest.py</b> : This script is for testing the accuracy of the model. 
It should be place in the same directory as Models.py and weight dictionary.<br>
<b>Recognizer.py</b> : This file contain the fuction recognize which act as a API. 
It in-take a string filename of the file to be recognized and return the recognized result as string.<br>
<b>DataProcessing.py</b> : This file contain functions that are used to prepare data for training.<br>
<b>Generator/</b> : This directory contain the sample generator.<br>
