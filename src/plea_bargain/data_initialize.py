import random
import numpy as np

def weighted_choice(choices):
    total = sum(w for c, w in choices)
    r = random.uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w >= r:
            return c
        upto += w

# Demographics in United States
genders = [("male", 0.48), ("female", 0.5), ("non-binary", 0.01), ("other genders", 0.01)]
ethnicities = [("Asian", 0.067), ("African", 0.134), ("Caucasian", 0.601), ("Hispanic", 0.185), ("Native American", 0.013)]
educations = [("High School diploma", 0.28), ("Some college", 0.29), ("bachelor's degree", 0.21), ("master's degree", 0.12), ("Ph.D.", 0.03), ("other", 0.07)]
locations = [("urban", 0.81), ("suburban", 0.1), ("rural", 0.09)]
occupations = [("student", 0.15), ("employed", 0.6), ("unemployed", 0.04), ("retired", 0.2), ("other", 0.01)]

# Generate Agent Profile
def generate_profile():
    gender = weighted_choice(genders)
    ethnicity = weighted_choice(ethnicities)
    education = weighted_choice(educations)
    occupation = weighted_choice(occupations)
    location = weighted_choice(locations)
    return gender, ethnicity, education, occupation, location

# GPT Temperature Normalization
def map_samples(samples, src_min, src_max, dst_min, dst_max):
    scale = (dst_max - dst_min) / (src_max - src_min)
    mapped_samples = (samples - src_min) * scale + dst_min
    mapped_samples = np.clip(mapped_samples, dst_min, dst_max)
    return mapped_samples

def init_temperature(member_num, lower_temp, upper_temp):
    mean = 1
    std_dev = 1
    temperature_samples = np.random.normal(mean, std_dev, member_num)
    return map_samples(temperature_samples, 1 - 3 * std_dev, 1 + 3 * std_dev, lower_temp, upper_temp)
