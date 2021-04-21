import os
import pandas as pd
import numpy as np
import tensorflow as tf

pd.options.display.max_colwidth = 150

IMG_WIDTH = 512
IMG_HEIGHT = 512
COLOR_CHANNELS = 3

# NOTE: Download flickr8k and put into data/ folder
flickr8k_dir = 'data/flickr8k/'
flickr8k_images_dir = 'data/flickr8k/Images/'

df_captions = pd.read_csv('data/flickr8k_2_shot_triplets.csv')

# Lists that hold image paths and captions
img_list = []
pos_cap_list = []
neg_cap_list = []

print('Creating image and caption lists...', end='')
for index, row in df_captions.iterrows():
    # triplet_list.append((img, pos_caption, neg_caption))
    img_list.append(row['image'])

    pos_c = row['positve_c']
    pos_cap_list.append(pos_c)

    neg_c = row['negative_c']
    neg_cap_list.append(neg_c)
print('Done!')

print('Loading image encoder model...', end='')
img_encoder = tf.keras.models.load_model('saved_models/img_encoder')
print('Done!')

print('Loading cached vectors...', end='')
cached_img_vectors = np.load('saved_models/cached_img_vectors.npy')
print('Done!')


def load_img(img_file):
    # If image is a file, give img_file path
    img = tf.io.read_file(img_file)

    img = tf.image.decode_jpeg(img, channels=3)
    #  If image is resized in mobile app, comment resize below
    img = tf.image.resize(
        img,
        [IMG_HEIGHT, IMG_WIDTH],
        method=tf.image.ResizeMethod.NEAREST_NEIGHBOR
    )
    #  Convert into float32
    img = tf.cast(img, tf.float32)
    # Normalize
    img = (img / 127.5) - 1.0
    return img


def calculate_cosine_similarity(img_vectors, query_vector, top_k=21):
    """
    img_vectors is cached image vectors (after training is complete)
    query_vector is the image received by mobile app
    returns a list of indices that match top_k amount (for img_list, pos_cap_list)
    """
    img_vectors = tf.math.l2_normalize(img_vectors, axis=1)
    query_vector = tf.math.l2_normalize(query_vector, axis=1)

    dot_similarity = tf.matmul(query_vector, img_vectors, transpose_b=True)

    predictions_cosine = tf.math.top_k(dot_similarity, top_k).indices.numpy()[0]
    return predictions_cosine


def get_predicted_img_cap_pair(predictions, k_index):
    #  Get the image path
    predicted_img = flickr8k_images_dir + img_list[predictions[k_index]]
    # print('Predicted image path:', predicted_img)

    #  Read jpg image file
    predicted_img = tf.io.read_file(predicted_img)
    predicted_img = tf.image.decode_jpeg(predicted_img, channels=3)

    # Get the captions
    predicted_caption = pos_cap_list[predictions[k_index]]

    return predicted_img, predicted_caption


def predict(query_img, k_index=0):
    """
    query_img is the image received by the mobile app
    k_index=0 means: fetch the most similar one
    """

    # Add dummy batch size
    query_img = tf.expand_dims(query_img, 0)
    # Get the vector representation from image encoder
    query_vector = img_encoder.predict(query_img)
    # Get the predictions by calculating the cosine similarity
    predictions_cosine = calculate_cosine_similarity(cached_img_vectors, query_vector)
    #  Get the final image and caption
    predicted_img, predicted_caption = get_predicted_img_cap_pair(predictions_cosine, k_index)

    return predicted_img, predicted_caption
