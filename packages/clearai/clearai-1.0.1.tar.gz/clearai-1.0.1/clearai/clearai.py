from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.datasets import fashion_mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras import utils
from IPython.display import Image
from keras.datasets import boston_housing
import cv2
import numpy as np

class ClearAI:
    def createNeuralNetworkForClassification(saveNeuralNetwork=[True, "fashion_mnist_dense.h5"],lossD="categorical_crossentropy",
                                            optimizerD="SGD", metricsD=["accuracy"],
                                            batchSizeD=200,epochsD=100,verboseD=1,
                                            activationD=['relu','softmax'], Neurons=[800,10],
                                            xTrainRS=[60000,784], toCategoricalD=10, xTrainNorm=255,
                                            loadData=fashion_mnist.load_data(), neuronLayersCount=2,
                                            TestNeuralNetwork=[True, True]):
        (x_train, y_train), (x_test, y_test) = loadData
        x_train = x_train.reshape(xTrainRS[0],xTrainRS[1])
        x_train = x_train / xTrainNorm
        y_train = utils.to_categorical(y_train,toCategoricalD)

        model = Sequential()
        for i in range(neuronLayersCount):
            if i == 0:
                model.add(Dense(Neurons[i], input_dim=xTrainRS[1], activation=activationD[i]))
            else:
                model.add(Dense(Neurons[i], activation=activationD[i]))

        model.compile(loss=lossD, optimizer=optimizerD, metrics=metricsD)
        model.fit(x_train, y_train, batch_size=batchSizeD, epochs=epochsD, verbose=verboseD)
        if saveNeuralNetwork[0]:
            model.save(saveNeuralNetwork[1])
        if TestNeuralNetwork[0]:
            predictions = model.predict(x_train)
            if TestNeuralNetwork[1]:
                print(f"{predictions[0]}-{np.argmax(predictions[0])}-{np.argmax(y_train[0])}")

    def loadNeuralNetworkForClassification(targetSize, imageSize,
                                        classes, imgPath, modelPath,
                                        xNorm=255, xRS=[1, 784], colorMode="grayscale"):
        model = load_model(modelPath)
        model.summary()
        Image(imgPath, width=imageSize[0], height=imageSize[1])
        img = image.load_img(imgPath, target_size=targetSize, color_mode=colorMode)
        x = image.img_to_array(img)
        x = x.reshape(xRS[0], xRS[1])
        x = xNorm - x
        x /= xNorm
        prediction = model.predict(x)
        prediction = np.argmax(prediction)
        return classes[prediction]

    def loadNeuralNetworkForReggresion(modelPath, verboseM=0, axises=[0,0],
                                    loadData=boston_housing.load_data(),
                                    npSeed=42):
        np.random.seed(npSeed)
        (x, y), (x_test, y_test) = loadData
        mean = x.mean(axis=axises[0])
        std = x.std(axis=axises[1])
        x -= mean
        x /= std
        np.random.seed(npSeed)
        model = load_model(modelPath)
        mse, mae = model.evaluate(x, y, verbose=verboseM)
        pred = model.predict(x)
        return f"{mae}\n{pred[1][0]} {y[1]}\n{pred[50][0]} {y[50]}\n{pred[100][0]} {y[100]}"

    def createNeuralNetworkForReggresion(saveNeuralNetwork=[True, "boston_housing_dense.h5"],lossD="mse",
                                        optimizerD="adam", metricsD=["mae"],
                                        batchSizeD=1,epochsD=100,
                                        verboseM=0,verboseD=1,
                                        activationD='relu', Neurons=[128,1],
                                        axises=[0,0],
                                        loadData=boston_housing.load_data(),
                                        TestNeuralNetwork=[True, True], npSeed=42):
        np.random.seed(npSeed)
        (x_train, y_train), (x_test, y_test) = loadData
        mean = x_train.mean(axis=axises[0])
        std = x_train.std(axis=axises[1])
        x_train -= mean
        x_train /= std
        x_test -= mean
        x_test /= std
        model = Sequential()
        model.add(Dense(Neurons[0], activation=activationD, input_shape=(x_train.shape[1],)))
        model.add(Dense(Neurons[1]))
        model.compile(optimizer=optimizerD, loss=lossD, metrics=metricsD)
        model.fit(x_train, y_train, epochs=epochsD, batch_size=batchSizeD, verbose=verboseD)
        if saveNeuralNetwork[0]:
            model.save(saveNeuralNetwork[1])
        if TestNeuralNetwork[0]:
            mse, mae = model.evaluate(x_test, y_test, verbose=verboseM)
            pred = model.predict(x_test)
            if TestNeuralNetwork[1]:
                return f"{mae}\n{pred[1][0]} {y_test[1]}\n{pred[50][0]} {y_test[50]}\n{pred[100][0]} {y_test[100]}"

    def startCv2(type="camera", stopWindowSymbol=[True, "x"], windowName="Camera", VideoCaptureNum=0, movementObjName="Movement"):
        if type == "camera":
            cap = cv2.VideoCapture(VideoCaptureNum)
            while cap.isOpened():
                success, img = cap.read()
                img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                cv2.imshow(windowName, img)
                if stopWindowSymbol[0]:
                    if cv2.waitKey(1) & 0xff == ord(stopWindowSymbol[1]):
                        break
                else:
                    if cv2.waitKey(0) == 27:
                        break
            cap.release()
            cv2.destroyAllWindows()
        elif type == "md":
            cap = cv2.VideoCapture(0)
            ret, frame1 = cap.read()
            ret, frame2 = cap.read()
            while cap.isOpened():
                diff = cv2.absdiff(frame1, frame2)
                gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                blur = cv2.GaussianBlur(gray, (5, 5), 0)
                _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
                dilated = cv2.dilate(thresh, None, iterations=3)
                сontours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                for contour in сontours:
                    (x, y, w, h) = cv2.boundingRect(contour)
                    if cv2.contourArea(contour) < 800:
                        continue
                    cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame1, movementObjName, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv2.LINE_AA)
                cv2.imshow(windowName, frame1)
                frame1 = frame2
                ret, frame2 = cap.read()
                if stopWindowSymbol[0]:
                    if cv2.waitKey(1) & 0xff == ord(stopWindowSymbol[1]):
                        break
                else:
                    if cv2.waitKey(0) == 27:
                        break
            cap.release()
            cv2.destroyAllWindows()