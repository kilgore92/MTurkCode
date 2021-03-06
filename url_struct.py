#!/usr/bin/env python3

import pickle

n_images = 1000

def generate_url_struct():
    base_url = 'https://s3-us-west-1.amazonaws.com/facesdb/gans_compare/celeba_fixed'
    image_names = ['dcgan.jpg','dcgan-cons.jpg','dcgan-gp.jpg','wgan.jpg','wgan-gp.jpg','dragan.jpg']
    pairs = generate_pairs(image_names)
    url_struct = []
    for folder in range(n_images):
        struct_row = []
        folder_url = base_url + '/' + str(folder)
        struct_row.append(folder_url+'/original.jpg')
        for pair in pairs:
            single_pair = []
            for item in pair:
                single_pair.append(folder_url + '/gen/' + item)
            struct_row.append(single_pair)
        url_struct.append(struct_row)
    #Save the struct
    with open('url_struct.pkl','wb') as f:
        pickle.dump(url_struct,f)


def generate_pairs(imgList):
    pairsList = []
    for idx in range(len(imgList)):
        for idx_2 in range(idx+1,len(imgList)):
            pair = []
            pair.append(imgList[idx])
            pair.append(imgList[idx_2])
            pairsList.append(pair)
    return pairsList

if __name__ == '__main__':
    generate_url_struct()

