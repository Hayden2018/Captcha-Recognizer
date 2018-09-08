Captcha Recognizer is a simple Python program using convolutional neural networks to recognize words in a specific type of Captcha. 
It is implemented using Pytorch. 
#
<b>captcha_reducer.py</b> : This script is for preprocessing the input image.<br>
<b>Models.py</b> : This file define the three neural models in this program. Icluding encoder, decoder and classifier.<br>
<b>ModelTrain.py</b> : This file contain the script for training the file. 
The resulting weight dictionary will be saved in the same directory as this script.<br>
<b>ModelTest.py</b> : This file contain script that test accuracy of the model. 
It should be place in the same directory as Models.py and weight dictionary.<br>
<b>Recognizer.py</b> : This file contain the fuction recognize which act as a API. 
It in-take a string filename of the file to be recognized and return the recognized result as string.
