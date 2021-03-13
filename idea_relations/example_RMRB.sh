#!/bin/bash

MALLET_BIN_DIR="/Users/shichengliu/Desktop/College_CS/cs257/NLP-win-21/idea_relations/mallet-2.0.8/bin"
# INPUT_FILE="/Users/shichengliu/Desktop/College_CS/cs257/NLP-win-21/idea_relations/data/acl.jsonlist.gz"
INPUT_FILE="/Users/shichengliu/Desktop/College_CS/cs257/NLP-win-21/idea_relations/data/RMRB_5_each_month.txt"
# BACKGROUND_FILE="/Users/shichengliu/Desktop/College_CS/cs257/NLP-win-21/idea_relations/data/nips.jsonlist.gz"
DATA_OUPUT_DIR="RMRB_5_each_month/processing/"
FINAL_OUTPUT_DIR="RMRB_5_each_month/output/"
PREFIX="RMRB_5_each_month"

# python main.py --input_file $INPUT_FILE --data_output_dir $DATA_OUPUT_DIR --final_output_dir $FINAL_OUTPUT_DIR --mallet_bin_dir $MALLET_BIN_DIR --option keywords --num_ideas 100 --prefix $PREFIX --background_file $BACKGROUND_FILE
python main.py --input_file $INPUT_FILE --data_output_dir $DATA_OUPUT_DIR --final_output_dir $FINAL_OUTPUT_DIR --mallet_bin_dir $MALLET_BIN_DIR --option topics --num_ideas 50 --prefix $PREFIX
# python main.py --input_file $INPUT_FILE --tokenize --data_output_dir $DATA_OUPUT_DIR --final_output_dir $FINAL_OUTPUT_DIR --mallet_bin_dir $MALLET_BIN_DIR --option topics --num_ideas 50 --prefix $PREFIX