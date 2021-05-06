# hand-gesture-controlled-robot
- Make a folder name dataset and again make 6 folder in dataset folder namely (0,1,2,3,4,5) for six different class, then, run dataset_generatio.py code with valid path of folder and press 's' to take sanpshot of gestures. this will create dataset.
- After creating dataset, Run model_train.py with valid path of datasets to train the machine learning model.
- Upload copy_wireless_esp.ino script into NodeMCU.
- After model training, run gesture_prediction.py and press 's' to start prediction of gestures and send command to NodeMCU.
- **NOTE:- NodeMCU and Laptop must be connected to same wifi/internet before running the gesture_prediction.py**
