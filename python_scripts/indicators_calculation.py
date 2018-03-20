from __future__ import print_function, division
import thinkdsp
from scipy.stats import stats, skew
import statistics
import time
import pandas as pd
import numpy as np
import csv
from config import constants

start_time = time.time()

# Writter implementation
csvfile_writer = open(constants.indicators_path, 'wb')
writer = csv.writer(csvfile_writer)
writer.writerow(('folder', 'record_name', 'mean_frequency', 'standard_deviation', 'median_frequency',
                 'first_quantile', 'third_quantile', 'inter_quantile_range', 'kurtosis', 'skewness',
                 'speaker_name', 'speaker_gender', 'speaker_age_range', 'speaker_language', 'speaker_dialect',
                 'sampling_rate', 'sample_rate_format'))

# @TODO don't save the index of a dataframe // don't upload the index of the csv file in a dataframe
scraping_df = pd.read_csv(constants.scraping_result_path,error_bad_lines=False)
scraping_df = scraping_df.drop("Unnamed: 0", axis=1)

start_time = time.time()

# Loop on every folder (6244)
for i in range(len(scraping_df["sub_link"])):
    folder = scraping_df["sub_link"][i][:-4]
    print(folder)
    print (i)

    try:
        # Extract main information from README
        with open(
                '/Users/kevenlemoing/Sites/sandvik_code_assignement/data/downloads/{}/etc/README'.format(folder),
                'r') as readme:

            for line in readme:
                if 'User' in line:
                    speaker_name = " ".join(line[10:].split())
                elif 'Gender' in line:
                    speaker_gender = " ".join(line[8:].split())
                elif 'Age' in line:
                    speaker_age_range = " ".join(line[11:].split())
                elif 'Language' in line:
                    speaker_language = " ".join(line[10:].split())
                elif 'dialect' in line:
                    speaker_dialect = " ".join(line[23:].split())
                elif 'Sampling' in line:
                    sampling_rate = line[15:]
                elif 'Sample' in line:
                    sample_rate_format = line[20:]

        readme.close()

        # Extract records' file names contained in the folder
        file_name_list = []
        with open(
                '/Users/kevenlemoing/Sites/sandvik_code_assignement/data/downloads/{}/etc/prompts-original'.format(
                    folder), 'r') as prompts_original:
            for line in prompts_original:
                if "*/" in line:
                    line = line.split(" ")
                    file_name_list.append(line[0][2:])
                else:
                    line = line.split(" ")
                    file_name_list.append(line[0])

        prompts_original.close()

        for i in range(len(file_name_list)):
            file_name = file_name_list[i]

            wave = thinkdsp.read_wave(
                '/Users/kevenlemoing/Sites/sandvik_code_assignement/data/downloads/{}/wav/{}.wav'.format(folder,
                                                                                                         file_name))

            spectrum = wave.make_spectrum()
            # mean
            mean_frequency = statistics.mean(spectrum.peaks()[1])
            # standarddeviation
            standard_deviation = statistics.stdev(spectrum.peaks()[1])
            # median
            median_frequency = statistics.median(spectrum.peaks()[1])
            ##First quantile
            d = {'frequency': spectrum.peaks()[1]}
            freq_df = pd.DataFrame(d)
            first_quantile = freq_df.quantile(0.1)[0]
            # Third quantile
            third_quantile = freq_df.quantile(0.3)[0]
            # Inter quantile range
            q75, q25 = np.percentile(spectrum.peaks()[1], [75, 25])
            inter_quantile_range = q75 - q25
            # Kurtosis
            kurtosis = stats.kurtosis(spectrum.peaks()[1])
            # Skewness (skewness of normal distribution should be 0)
            skewness = skew(spectrum.peaks()[1])

            writer.writerow((folder, file_name, mean_frequency, standard_deviation, median_frequency,
                             first_quantile, third_quantile, inter_quantile_range, kurtosis, skewness,
                             speaker_name, speaker_gender, speaker_age_range, speaker_language, speaker_dialect,
                             sampling_rate, sample_rate_format))

            print("It's ok for this record: {}; from this folder: {}".format(file_name, folder))


    except IOError:
        print("Oops! Something with for this folder:{}".format(folder))


csvfile_writer.close()
print("")
print("--- %s seconds ---" % (time.time() - start_time))
print("")
