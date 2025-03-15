import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score

# Dataset path
DATASET_DIR = r"C:\Users\loiac\Desktop\recordings\spectrograms"

# Load images and labels
def load_dataset():
    images, labels = [], []
    
    for file in os.listdir(DATASET_DIR):
        if file.endswith(".png"):
            img_path = os.path.join(DATASET_DIR, file)
            
            # Load image and preprocess
            img = load_img(img_path, target_size=(128, 128))  # Resize to a common shape
            img_array = img_to_array(img) / 255.0  # Normalize pixel values
            
            images.append(img_array)
            
            # Extract label from filename (e.g., 'reuters_20250314_082700.png' → 'reuters')
            label = file.split('_')[0]
            labels.append(label)

    return np.array(images), np.array(labels)

# Load dataset
X, y = load_dataset()

# Encode categorical labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# One-hot encode labels for CNN
num_classes = len(label_encoder.classes_)
y_train_encoded = to_categorical(y_train, num_classes=num_classes)
y_test_encoded = to_categorical(y_test, num_classes=num_classes)

# CNN Model
model = Sequential([
    Conv2D(8, (4, 4), strides=(4, 4), activation='relu', input_shape=(128, 128, 3)),  # First Conv layer
    Conv2D(16, (4, 4), activation='relu'),  # Second Conv layer
    MaxPooling2D(pool_size=(2, 2)),  # Max pooling
    Flatten(),
    Dense(256, activation='relu'),  # Fully connected layer
    Dense(num_classes, activation='softmax')  # Linear output layer with softmax
])

# Compile model
model.compile(optimizer=tf.keras.optimizers.Adadelta(learning_rate=1.0), 
              loss='categorical_crossentropy', 
              metrics=['accuracy'])

# Train model
history = model.fit(X_train, y_train_encoded, 
                    epochs=100, batch_size=32, 
                    validation_split=0.2, verbose=1)

# Evaluate model
y_pred_probs = model.predict(X_test)
y_pred = np.argmax(y_pred_probs, axis=1)

print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))
