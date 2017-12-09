#!/usr/bin/env python3
import boto3
import pickle
import generate_question

def create_hit(mturk,question):
    """
    Creates a single HIT using the MTurk object and the supplied XML-HTML question form
    Returns the ID of the created HIT

    """

    new_hit = mturk.create_hit(
        Title = 'Finding similar images',
        Description = 'Given are sets of 3 images, select which image looks more like the original image',
        Keywords = 'text, quick, labeling',
        Reward = '0.01',
        MaxAssignments = 1,
        LifetimeInSeconds = 172800,
        AssignmentDurationInSeconds = 600,
        AutoApprovalDelayInSeconds = 14400,
        Question = question
    )

    return new_hit['HIT']

def create_question(url_struct,question_num,num_images,pair_num):
    """
    Creates HTML (with XML wrapper) question form needed for a single HIT
    Returns created question and list of image triples part of the HIT

    """
    merged_questions = ""
    images_per_hit = []
    for image_num in range(question_num,question_num+num_images):
        image_triple = []
        merged_questions += generate_question.generate_single_question(url_struct[image_num][0],url_struct[image_num][pair_num][0],url_struct[image_num][pair_num][1])
        image_triple.append(url_struct[image_num][0])
        image_triple.append(url_struct[image_num][pair_num][0])
        image_triple.append(url_struct[image_num][pair_num][1])
        images_per_hit.append(image_triple)

    question = generate_question.generate_html_question(merged_questions = merged_questions)

    return question,images_per_hit

def get_url_struct(filename):

    """
    Returns struct containing all image URLs

    """
    with open(filename,'rb') as f:
        url_struct = pickle.load(f)
    return url_struct

def generate_single_hit(mturk,url_struct,question_num,num_images,pair_num,hit_dict):
    """
    Generates single HIT
    Returns updated dictionary that maintains HITID : Image triples mapping
    question_num : 0 - 500 (images) [row index in URL struct]
    num_images : Number of images in a single HIT, programmable 1-N
    pair_num : 1 - 9, index for each generated pair of the original image [coloumn in URL struct]

    """

    question,images_per_hit = create_question(url_struct,
                                              question_num = question_num,
                                              num_images = num_images,
                                              pair_num = pair_num)

    hit = create_hit(mturk=mturk,question=question)
    hit_dict[hit['HITId']] = images_per_hit #Update the dictionary
    print ("A new HIT has been created. You can preview it here:")
    print ("https://workersandbox.mturk.com/mturk/preview?groupId=" + hit['HITGroupId'])
    print ("HITID = " + hit['HITId']+ " (Use to Get Results)")
    return hit_dict

def save_hit_dict(filename,hit_dict):
    """
    Saves the HIT dictionary as a pickle file that can be processed
    while fetching results

    """
    with open(filename,'wb') as f:
        pickle.dump(hit_dict,f)


if __name__ == '__main__':

    MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

    mturk = boto3.client('mturk',
                        aws_access_key_id = "AKIAI4DQ22LGP4HC3X4Q",
                        aws_secret_access_key = "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",
                        region_name='us-east-1',
                        endpoint_url = MTURK_SANDBOX
                        )

    print ("I have $" + mturk.get_account_balance()['AvailableBalance'] + " in my Sandbox account")

    hit_dict = {}

    url_struct = get_url_struct('url_struct.pkl')

    hit_dict = generate_single_hit(mturk=mturk,
                                   url_struct=url_struct,
                                   question_num = 0,
                                   pair_num = 1,
                                   num_images = 10,
                                   hit_dict = hit_dict)

    save_hit_dict('hit_dict.pkl',hit_dict)


