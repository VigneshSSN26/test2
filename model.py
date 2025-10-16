#1Pixel wise diff btw two images
import cv2
import numpy as np
import matplotlib.pyplot as plt

M1 = cv2.imread('image1.png')
M2 = cv2.imread('image.png')

M2 = cv2.resize(M2, (M1.shape[1], M1.shape[0]))

Out = cv2.absdiff(M1, M2)

plt.imshow(cv2.cvtColor(Out, cv2.COLOR_BGR2RGB))
plt.title('Output - Absolute Difference')
plt.axis('off')
plt.show()


#2 HOG feature extraction

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Preprocess the Data (resize to 64x128)
img = cv2.imread('image.png', cv2.IMREAD_GRAYSCALE)
img = cv2.resize(img, (64, 128))

plt.figure()
plt.title("Step 1: Preprocessed Image (64x128)")
plt.imshow(img, cmap='gray')
plt.axis('off')

# Step 2: Calculate Gradients (x and y direction)
gx = cv2.Sobel(img, cv2.CV_32F, 1, 0, ksize=1)
gy = cv2.Sobel(img, cv2.CV_32F, 0, 1, ksize=1)

plt.figure()
plt.subplot(1,2,1)
plt.title("Gradient X")
plt.imshow(gx, cmap='gray')
plt.axis('off')
plt.subplot(1,2,2)
plt.title("Gradient Y")
plt.imshow(gy, cmap='gray')
plt.axis('off')

# Step 3: Calculate Magnitude and Orientation
magnitude, angle = cv2.cartToPolar(gx, gy, angleInDegrees=True)

plt.figure()
plt.subplot(1,2,1)
plt.title("Gradient Magnitude")
plt.imshow(magnitude, cmap='gray')
plt.axis('off')
plt.subplot(1,2,2)
plt.title("Gradient Orientation")
plt.imshow(angle, cmap='gray')
plt.axis('off')

# Step 4: Calculate Histogram of Gradients in 8x8 cells
cell_size = (8, 8)
num_bins = 9
h, w = img.shape
cells_x = w // cell_size[0]
cells_y = h // cell_size[1]
hist = np.zeros((cells_y, cells_x, num_bins), dtype=np.float32)

for i in range(cells_y):
    for j in range(cells_x):
        cell_mag = magnitude[i*8:(i+1)*8, j*8:(j+1)*8]
        cell_ang = angle[i*8:(i+1)*8, j*8:(j+1)*8]
        hist_cell, _ = np.histogram(cell_ang, bins=num_bins, range=(0, 180), weights=cell_mag)
        hist[i, j, :] = hist_cell

plt.figure()
plt.title("Step 4: HOG Cell Histogram (Shape)")
plt.imshow(hist.sum(axis=2), cmap='gray')
plt.axis('off')

# Step 5: Normalize gradients in 16x16 blocks
features = []
for i in range(cells_y - 1):
    for j in range(cells_x - 1):
        block = hist[i:i+2, j:j+2, :].ravel()
        norm = np.linalg.norm(block) + 1e-5
        block = block / norm
        features.extend(block)

# Step 6: Final HOG feature vector for complete image
hog_features = np.array(features)

print("HOG feature vector length:", len(hog_features))

plt.show()

#3 - Contrast stretching and linear filtering===============================

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image in grayscale
img = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)

# -------------------------------
# 1. Contrast Stretching
# -------------------------------
min_val = np.min(img)
max_val = np.max(img)
stretched = ((img - min_val) / (max_val - min_val)) * 255
stretched = stretched.astype(np.uint8)

# -------------------------------
# 2. Linear Filtering (Smoothing)
# -------------------------------
kernel = np.ones((3,3), np.float32) / 9
filtered = cv2.filter2D(stretched, -1, kernel)

# -------------------------------
# 3. Plot images and histograms
# -------------------------------
plt.figure(figsize=(10,6))

plt.subplot(2,3,1)
plt.title("Original Image")
plt.imshow(img, cmap='gray')
plt.axis('off')

plt.subplot(2,3,2)
plt.title("Contrast Stretched")
plt.imshow(stretched, cmap='gray')
plt.axis('off')

plt.subplot(2,3,3)
plt.title("Linear Filtered")
plt.imshow(filtered, cmap='gray')
plt.axis('off')

plt.subplot(2,3,4)
plt.title("Original Histogram")
plt.hist(img.ravel(), 256, [0,256])

plt.subplot(2,3,5)
plt.title("Stretched Histogram")
plt.hist(stretched.ravel(), 256, [0,256])

plt.subplot(2,3,6)
plt.title("Filtered Histogram")
plt.hist(filtered.ravel(), 256, [0,256])

plt.tight_layout()
plt.show()

#4 Geometrical Transformations ==============================================
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image
img = cv2.imread('image.png')
rows, cols = img.shape[:2]

# ------------------------------
# 1. Scaling
# ------------------------------
scaled_up = cv2.resize(img, None, fx=1.5, fy=1.5)   # scale up by 1.5
scaled_down = cv2.resize(img, None, fx=0.5, fy=0.5) # scale down by 0.5

# ------------------------------
# 2. Rotation
# ------------------------------
M_rotate = cv2.getRotationMatrix2D((cols/2, rows/2), 45, 1)  # rotate 45 degrees
rotated = cv2.warpAffine(img, M_rotate, (cols, rows))

# ------------------------------
# 3. Shearing
# ------------------------------
M_shear = np.array([[1, 0.5, 0],   # shear along x
                    [0.5, 1, 0]], dtype=np.float32)
sheared = cv2.warpAffine(img, M_shear, (cols, rows))

# ------------------------------
# Display results
# ------------------------------
plt.figure(figsize=(10,8))

plt.subplot(2,2,1)
plt.title("Original Image")
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.axis('off')

plt.subplot(2,2,2)
plt.title("Scaled Up")
plt.imshow(cv2.cvtColor(scaled_up, cv2.COLOR_BGR2RGB))
plt.axis('off')

plt.subplot(2,2,3)
plt.title("Rotated 45°")
plt.imshow(cv2.cvtColor(rotated, cv2.COLOR_BGR2RGB))
plt.axis('off')

plt.subplot(2,2,4)
plt.title("Sheared")
plt.imshow(cv2.cvtColor(sheared, cv2.COLOR_BGR2RGB))
plt.axis('off')

plt.tight_layout()
plt.show()


#5 - SIFT Feature detector ==========================================

import cv2
import matplotlib.pyplot as plt

# Load the image in grayscale
img = cv2.imread('image.png', cv2.IMREAD_GRAYSCALE)

# ------------------------------
# 1. Construct Scale Space & 2. Keypoint Localisation
# ------------------------------
sift = cv2.SIFT_create()
keypoints = sift.detect(img, None)

# Draw keypoints
img_keypoints = cv2.drawKeypoints(img, keypoints, None)

plt.figure(figsize=(6,6))
plt.title("Keypoints detected")
plt.imshow(img_keypoints, cmap='gray')
plt.axis('off')
plt.show()

# ------------------------------
# 3. Orientation Assignment & 4. Keypoint Descriptor
# ------------------------------
keypoints, descriptors = sift.compute(img, keypoints)

print("Number of keypoints detected:", len(keypoints))
print("Descriptor shape:", descriptors.shape)

# Optional: show one descriptor vector
print("First descriptor vector (128 elements):\n", descriptors[0])

#6 - extract image from videos ==============================================

import cv2
import os

# Load the video
video_path = 'video.mp4'  # replace with your video file
cap = cv2.VideoCapture(video_path)

# Directory to save frames
output_dir = 'frames'
os.makedirs(output_dir, exist_ok=True)

frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Save each frame as an image
    frame_filename = os.path.join(output_dir, f'frame_{frame_count:04d}.jpg')
    cv2.imwrite(frame_filename, frame)
    
    frame_count += 1

cap.release()
print(f"Total frames extracted: {frame_count}")

#7 - Horse Human =====================================================================

import tensorflow as tf
import tensorflow_datasets as tfds
import matplotlib.pyplot as plt
import numpy as np

# a. Load the dataset
(ds_train, ds_test), ds_info = tfds.load(
    'horses_or_humans',
    split=['train', 'test'],
    as_supervised=True,
    with_info=True
)

# b. View the number of training and testing images
print("Training images:", ds_info.splits['train'].num_examples)
print("Testing images:", ds_info.splits['test'].num_examples)

# c. Plot some images
plt.figure(figsize=(10,5))
for i, (img, label) in enumerate(ds_train.take(6)):
    plt.subplot(2,3,i+1)
    plt.imshow(img)
    plt.title("Horse" if label==0 else "Human")
    plt.axis('off')
plt.show()

# d. Normalizing the training data
def normalize_img(image, label):
    image = tf.cast(image, tf.float32) / 255.0
    return image, label

ds_train = ds_train.map(normalize_img).batch(32).prefetch(1)
ds_test = ds_test.map(normalize_img).batch(32).prefetch(1)

# e. Build a simple ResNet-based CNN
base_model = tf.keras.applications.ResNet50(
    weights=None, include_top=False, input_shape=(300,300,3), pooling='avg'
)
model = tf.keras.Sequential([
    base_model,
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# f. Train and show accuracy
history = model.fit(ds_train, epochs=5, validation_data=ds_test)

print("Training accuracy:", history.history['accuracy'][-1])
print("Testing accuracy:", history.history['val_accuracy'][-1])

#8 - MS-COCO ============================================================

import tensorflow as tf
import tensorflow_datasets as tfds
import matplotlib.pyplot as plt
from tensorflow.keras import layers, models

# ------------------------------
# a. Load the dataset (small subset for demo)
# ------------------------------
(train_ds, val_ds), ds_info = tfds.load(
    'coco/2017',
    split=['train[:1%]', 'validation[:1%]'], 
    as_supervised=True,
    with_info=True
)

# ------------------------------
# b. Show number of training/testing images
# ------------------------------
print("Training samples:", ds_info.splits['train'].num_examples * 0.05)
print("Validation samples:", ds_info.splits['validation'].num_examples * 0.05)

# ------------------------------
# c. Plot some images
# ------------------------------
plt.figure(figsize=(6,6))
for img, label in train_ds.take(9):
    plt.subplot(3,3,label['image_id']%9 +1) # simplified label visualization
    plt.imshow(img)
    plt.axis('off')
plt.show()

# ------------------------------
# d. Image Augmentation – contrast, flip, rotation
# ------------------------------
def augment(image, label):
    image = tf.image.random_flip_left_right(image)
    image = tf.image.random_contrast(image, 0.8, 1.2)
    image = tf.image.random_rotation(image, 0.2) if hasattr(tf.image, 'random_rotation') else image
    return image, label

aug_train_ds = train_ds.map(augment).batch(32)
val_ds = val_ds.batch(32)

# ------------------------------
# f. Normalize the training data
# ------------------------------
aug_train_ds = aug_train_ds.map(lambda x, y: (tf.cast(x, tf.float32)/255.0, y))
val_ds = val_ds.map(lambda x, y: (tf.cast(x, tf.float32)/255.0, y))

# ------------------------------
# g. Build a simple CNN for demo
# ------------------------------
cnn_model = models.Sequential([
    layers.InputLayer(input_shape=(128,128,3)),
    layers.Resizing(128,128),
    layers.Conv2D(32, 3, activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, activation='relu'),
    layers.MaxPooling2D(),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(1, activation='sigmoid')  # simplified for demo
])

cnn_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# ------------------------------
# h. Train CNN
# ------------------------------
history = cnn_model.fit(aug_train_ds, validation_data=val_ds, epochs=3)

plt.figure()
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Test Accuracy')
plt.title('CNN Training vs Testing Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

# ------------------------------
# j. Faster R-CNN for object detection (Using TensorFlow Object Detection API recommended)
# ------------------------------
# Full Faster R-CNN training is complex for exam/demo purposes.
# Placeholder for reference:
print("Faster R-CNN training requires TF Object Detection API and COCO formatted annotations.")
print("Refer to https://www.tensorflow.org/object_detection/tutorials for practical implementation.")



#9 - CANNY ===============================================================================
import cv2
import matplotlib.pyplot as plt

# Load image in grayscale
img = cv2.imread('image.png', cv2.IMREAD_GRAYSCALE)

# 1. Smoothing using Gaussian Blur
smoothed = cv2.GaussianBlur(img, (5,5), 1.4)

# 2. Canny Edge Detection (includes gradient calculation & non-maximum suppression)
edges = cv2.Canny(smoothed, threshold1=50, threshold2=150)

# Display results
plt.figure(figsize=(10,5))
plt.subplot(1,2,1)
plt.title('Original Grayscale')
plt.imshow(img, cmap='gray')
plt.axis('off')

plt.subplot(1,2,2)
plt.title('Edges Detected')
plt.imshow(edges, cmap='gray')
plt.axis('off')

plt.show()


#10 - Region Growing ===========================================================
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load image in grayscale
img = cv2.imread('image1.png', cv2.IMREAD_GRAYSCALE)

# Convert image to float32
img = np.float32(img)

# Seed point for region growing (you can change coordinates)
seed_point = (50, 50)  # (row, col)

# Region-growing mask
h, w = img.shape
segmented = np.zeros((h, w), np.uint8)
tolerance = 10  # intensity difference tolerance

# Initialize region with seed
region_pixels = [seed_point]
segmented[seed_point] = 255

while region_pixels:
    x, y = region_pixels.pop(0)
    for dx in [-1,0,1]:
        for dy in [-1,0,1]:
            nx, ny = x+dx, y+dy
            if 0<=nx<h and 0<=ny<w and segmented[nx,ny]==0:
                if abs(int(img[nx,ny]) - int(img[x,y])) < tolerance:
                    segmented[nx,ny] = 255
                    region_pixels.append((nx,ny))

# Display results
plt.figure(figsize=(10,5))
plt.subplot(1,2,1)
plt.title('Original')
plt.imshow(img, cmap='gray')
plt.axis('off')

plt.subplot(1,2,2)
plt.title('Region Growing Segmentation')
plt.imshow(segmented, cmap='gray')
plt.axis('off')

plt.show()


#11 - BCCD ===================================================================
import tensorflow as tf
import tensorflow_datasets as tfds
import matplotlib.pyplot as plt
from tensorflow.keras import layers, models

# a. Load the dataset (no as_supervised)
(train_ds, val_ds), ds_info = tfds.load(
    'bccd',
    split=['train', 'test'],
    with_info=True
)

# Helper: extract first class label for demo classification
def extract_label(example):
    # Use tf.cond for graph compatibility
    labels = example['objects']['label']
    label = tf.cond(
        tf.size(labels) > 0,
        lambda: labels[0],
        lambda: tf.constant(0, dtype=labels.dtype)
    )
    return example['image'], label

train_ds = train_ds.map(extract_label)
val_ds = val_ds.map(extract_label)

# b. Show the number of training and testing images
print("Training samples:", ds_info.splits['train'].num_examples)
print("Testing samples:", ds_info.splits['test'].num_examples)

# c. Plot some images
plt.figure(figsize=(6,6))
for i, (img, label) in enumerate(train_ds.take(9)):
    plt.subplot(3,3,i+1)
    plt.imshow(img)
    plt.title(str(label.numpy()))
    plt.axis('off')
plt.show()

# d. Image Augmentation – contrast, flipping, rotation
data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomContrast(0.2),
    layers.RandomRotation(0.1)
])

def augment(image, label):
    image = data_augmentation(image)
    return image, label

aug_train_ds = train_ds.map(augment)

# e. After augmentation, show the number of images (unchanged)
print("Training samples after augmentation:", ds_info.splits['train'].num_examples)

# f. Normalize the training data
def normalize(image, label):
    image = tf.cast(image, tf.float32) / 255.0
    return image, label

train_ds_norm = train_ds.map(normalize).batch(32).prefetch(1)
aug_train_ds_norm = aug_train_ds.map(normalize).batch(32).prefetch(1)
val_ds_norm = val_ds.map(normalize).batch(32).prefetch(1)

# g. Build a simple CNN for training (before augmentation)
cnn_model = models.Sequential([
    layers.InputLayer(input_shape=(None, None, 3)),
    layers.Resizing(128,128),
    layers.Conv2D(32, 3, activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, activation='relu'),
    layers.MaxPooling2D(),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(3, activation='softmax')  # 3 classes: WBC, RBC, Platelets
])

cnn_model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# h. Train and show accuracy (before augmentation)
history = cnn_model.fit(train_ds_norm, validation_data=val_ds_norm, epochs=5)
print("Train accuracy (no augmentation):", history.history['accuracy'][-1])
print("Test accuracy (no augmentation):", history.history['val_accuracy'][-1])

# i. Build a CNN for training (after augmentation)
cnn_model_aug = models.Sequential([
    layers.InputLayer(input_shape=(None, None, 3)),
    layers.Resizing(128,128),
    layers.Conv2D(32, 3, activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, activation='relu'),
    layers.MaxPooling2D(),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(3, activation='softmax')
])

cnn_model_aug.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# j. Train and show accuracy (after augmentation)
history_aug = cnn_model_aug.fit(aug_train_ds_norm, validation_data=val_ds_norm, epochs=5)
print("Train accuracy (with augmentation):", history_aug.history['accuracy'][-1])
print("Test accuracy (with augmentation):", history_aug.history['val_accuracy'][-1])

# k. Compare the training and testing accuracy before and after augmentation
print("Accuracy comparison:")
print("No augmentation - Train:", history.history['accuracy'][-1], "Test:", history.history['val_accuracy'][-1])
print("With augmentation - Train:", history_aug.history['accuracy'][-1], "Test:", history_aug.history['val_accuracy'][-1]
