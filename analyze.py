"""Module to analyze audio samples.
"""
import argparse
import datetime
import json
import operator
import os
import sys
from multiprocessing import Pool, freeze_support
from typing import Dict

import numpy

import audio
import config
import model
import species
import utils


def load_codes():
    """Loads the eBird codes.

    Returns:
        A dictionary containing the eBird codes.
    """
    with open(config.CODES_FILE, "r") as cfile:
        codes = json.load(cfile)

    return codes


def save_result_file(r: Dict[str, list], path: str, afile_path: str):
    """Saves the results to the hard drive.

    Args:
        r: The dictionary with {segment: scores}.
        path: The path where the result should be saved.
        afile_path: The path to audio file.
    """
    # Make folder if it doesn't exist
    if os.path.dirname(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)

    # Selection table
    out_string = ""

    if config.RESULT_TYPE == "table":
        # Raven selection header
        header = "Selection\tView\tChannel\tBegin Time (s)\tEnd Time (s)\tLow Freq (Hz)\tHigh Freq (Hz)\tSpecies Code\tCommon Name\tConfidence\n"
        selection_id = 0

        # Write header
        out_string += header

        # Extract valid predictions for every timestamp
        for timestamp in get_sorted_timestamps(r):
            rstring = ""
            start, end = timestamp.split("-", 1)

            for c in r[timestamp]:
                if c[1] > config.MIN_CONFIDENCE and (not config.SPECIES_LIST or c[0] in config.SPECIES_LIST):
                    selection_id += 1
                    label = config.TRANSLATED_LABELS[config.LABELS.index(c[0])]
                    rstring += "{}\tSpectrogram 1\t1\t{}\t{}\t{}\t{}\t{}\t{}\t{:.4f}\n".format(
                        selection_id,
                        start,
                        end,
                        150,
                        15000,
                        config.CODES[c[0]] if c[0] in config.CODES else c[0],
                        label.split("_", 1)[-1],
                        c[1],
                    )

            # Write result string to file
            out_string += rstring

    elif config.RESULT_TYPE == "audacity":
        # Audacity timeline labels
        for timestamp in get_sorted_timestamps(r):
            rstring = ""

            for c in r[timestamp]:
                if c[1] > config.MIN_CONFIDENCE and (not config.SPECIES_LIST or c[0] in config.SPECIES_LIST):
                    label = config.TRANSLATED_LABELS[config.LABELS.index(c[0])]
                    rstring += "{}\t{}\t{:.4f}\n".format(timestamp.replace("-", "\t"), label.replace("_", ", "), c[1])

            # Write result string to file
            out_string += rstring

    elif config.RESULT_TYPE == "r":
        # Output format for R
        header = "filepath,start,end,scientific_name,common_name,confidence,lat,lon,week,overlap,sensitivity,min_conf,species_list,model"
        out_string += header

        for timestamp in get_sorted_timestamps(r):
            rstring = ""
            start, end = timestamp.split("-", 1)

            for c in r[timestamp]:
                if c[1] > config.MIN_CONFIDENCE and (not config.SPECIES_LIST or c[0] in config.SPECIES_LIST):
                    label = config.TRANSLATED_LABELS[config.LABELS.index(c[0])]
                    rstring += "\n{},{},{},{},{},{:.4f},{:.4f},{:.4f},{},{},{},{},{},{}".format(
                        afile_path,
                        start,
                        end,
                        label.split("_", 1)[0],
                        label.split("_", 1)[-1],
                        c[1],
                        config.LATITUDE,
                        config.LONGITUDE,
                        config.WEEK,
                        config.SIG_OVERLAP,
                        (1.0 - config.SIGMOID_SENSITIVITY) + 1.0,
                        config.MIN_CONFIDENCE,
                        config.SPECIES_LIST_FILE,
                        os.path.basename(config.MODEL_PATH),
                    )

            # Write result string to file
            out_string += rstring

    elif config.RESULT_TYPE == "kaleidoscope":
        # Output format for kaleidoscope
        header = "INDIR,FOLDER,IN FILE,OFFSET,DURATION,scientific_name,common_name,confidence,lat,lon,week,overlap,sensitivity"
        out_string += header

        folder_path, filename = os.path.split(afile_path)
        parent_folder, folder_name = os.path.split(folder_path)

        for timestamp in get_sorted_timestamps(r):
            rstring = ""
            start, end = timestamp.split("-", 1)

            for c in r[timestamp]:
                if c[1] > config.MIN_CONFIDENCE and (not config.SPECIES_LIST or c[0] in config.SPECIES_LIST):
                    label = config.TRANSLATED_LABELS[config.LABELS.index(c[0])]
                    rstring += "\n{},{},{},{},{},{},{},{:.4f},{:.4f},{:.4f},{},{},{}".format(
                        parent_folder.rstrip("/"),
                        folder_name,
                        filename,
                        start,
                        float(end) - float(start),
                        label.split("_", 1)[0],
                        label.split("_", 1)[-1],
                        c[1],
                        config.LATITUDE,
                        config.LONGITUDE,
                        config.WEEK,
                        config.SIG_OVERLAP,
                        (1.0 - config.SIGMOID_SENSITIVITY) + 1.0,
                    )

            # Write result string to file
            out_string += rstring

    else:
        # CSV output file
        header = "Start (s),End (s),Scientific name,Common name,Confidence\n"

        # Write header
        out_string += header

        for timestamp in get_sorted_timestamps(r):
            rstring = ""

            for c in r[timestamp]:
                start, end = timestamp.split("-", 1)

                if c[1] > config.MIN_CONFIDENCE and (not config.SPECIES_LIST or c[0] in config.SPECIES_LIST):
                    label = config.TRANSLATED_LABELS[config.LABELS.index(c[0])]
                    rstring += "{},{},{},{},{:.4f}\n".format(start, end, label.split("_", 1)[0], label.split("_", 1)[-1], c[1])

            # Write result string to file
            out_string += rstring

    # Save as file
    with open(path, "w", encoding="utf-8") as rfile:
        rfile.write(out_string)


def get_sorted_timestamps(results: Dict[str, list]):
    """Sorts the results based on the segments.

    Args:
        results: The dictionary with {segment: scores}.

    Returns:
        Returns the sorted list of segments and their scores.
    """
    return sorted(results, key=lambda t: float(t.split("-", 1)[0]))


def get_raw_audio_from_file(fpath: str):
    """Reads an audio file.

    Reads the file and splits the signal into chunks.

    Args:
        fpath: Path to the audio file.

    Returns:
        The signal split into a list of chunks.
    """
    # Open file
    sig, rate = audio.open_audio_file(fpath, config.SAMPLE_RATE)

    # Split into raw audio chunks
    chunks = audio.split_signal(sig, rate, config.SIG_LENGTH, config.SIG_OVERLAP, config.SIG_MINLEN)

    return chunks


def predict(samples):
    """Predicts the classes for the given samples.

    Args:
        samples: Samples to be predicted.

    Returns:
        The prediction scores.
    """
    # Prepare sample and pass through model
    data = numpy.array(samples, dtype="float32")
    prediction = model.predict(data)

    # Logits or sigmoid activations?
    if config.APPLY_SIGMOID:
        prediction = model.flat_sigmoid(numpy.array(prediction), sensitivity=-config.SIGMOID_SENSITIVITY)

    return prediction


def analyze_file(item):
    """Analyzes a file.

    Predicts the scores for the file and saves the results.

    Args:
        item: Tuple containing (file path, config)

    Returns:
        The `True` if the file was analyzed successfully.
    """
    # Get file path and restore cfg
    fpath: str = item[0]
    config.set_config(item[1])

    # Start time
    start_time = datetime.datetime.now()

    # Status
    print(f"Analyzing {fpath}", flush=True)

    try:
        # Open audio file and split into 3-second chunks
        chunks = get_raw_audio_from_file(fpath)

    # If no chunks, show error and skip
    except Exception as ex:
        print(f"Error: Cannot open audio file {fpath}", flush=True)
        utils.write_error_log(ex)

        return False

    # Process each chunk
    try:
        start, end = 0, config.SIG_LENGTH
        results = {}
        samples = []
        timestamps = []

        for chunk_index, chunk in enumerate(chunks):
            # Add to batch
            samples.append(chunk)
            timestamps.append([start, end])

            # Advance start and end
            start += config.SIG_LENGTH - config.SIG_OVERLAP
            end = start + config.SIG_LENGTH

            # Check if batch is full or last chunk
            if len(samples) < config.BATCH_SIZE and chunk_index < len(chunks) - 1:
                continue

            # Predict
            p = predict(samples)

            # Add to results
            for i in range(len(samples)):
                # Get timestamp
                s_start, s_end = timestamps[i]

                # Get prediction
                pred = p[i]

                # Assign scores to labels
                p_labels = zip(config.LABELS, pred)

                # Sort by score
                p_sorted = sorted(p_labels, key=operator.itemgetter(1), reverse=True)

                # Store top 5 results and advance indices
                results[str(s_start) + "-" + str(s_end)] = p_sorted

            # Clear batch
            samples = []
            timestamps = []

    except Exception as ex:
        # Write error log
        print(f"Error: Cannot analyze audio file {fpath}.\n", flush=True)
        utils.write_error_log(ex)

        return False

    # Save as selection table
    try:
        # We have to check if output path is a file or directory
        if not config.OUTPUT_PATH.rsplit(".", 1)[-1].lower() in ["txt", "csv"]:
            rpath = fpath.replace(config.INPUT_PATH, "")
            rpath = rpath[1:] if rpath[0] in ["/", "\\"] else rpath

            # Make target directory if it doesn't exist
            rdir = os.path.join(config.OUTPUT_PATH, os.path.dirname(rpath))

            os.makedirs(rdir, exist_ok=True)

            if config.RESULT_TYPE == "table":
                rtype = ".BirdNET.selection.table.txt"
            elif config.RESULT_TYPE == "audacity":
                rtype = ".BirdNET.results.txt"
            else:
                rtype = ".BirdNET.results.csv"

            save_result_file(results, os.path.join(config.OUTPUT_PATH, rpath.rsplit(".", 1)[0] + rtype), fpath)
        else:
            save_result_file(results, config.OUTPUT_PATH, fpath)

    except Exception as ex:
        # Write error log
        print(f"Error: Cannot save result for {fpath}.\n", flush=True)
        utils.write_error_log(ex)

        return False

    delta_time = (datetime.datetime.now() - start_time).total_seconds()
    print("Finished {} in {:.2f} seconds".format(fpath, delta_time), flush=True)

    return True


if __name__ == "__main__":
    # Freeze support for executable
    freeze_support()

    # Parse arguments
    parser = argparse.ArgumentParser(description="Analyze audio files with BirdNET")
    parser.add_argument(
        "--i", default="example/", help="Path to input file or folder. If this is a file, --o needs to be a file too."
    )
    parser.add_argument(
        "--o", default="example/", help="Path to output file or folder. If this is a file, --i needs to be a file too."
    )
    parser.add_argument("--lat", type=float, default=-1, help="Recording location latitude. Set -1 to ignore.")
    parser.add_argument("--lon", type=float, default=-1, help="Recording location longitude. Set -1 to ignore.")
    parser.add_argument(
        "--week",
        type=int,
        default=-1,
        help="Week of the year when the recording was made. Values in [1, 48] (4 weeks per month). Set -1 for year-round species list.",
    )
    parser.add_argument(
        "--slist",
        default="",
        help='Path to species list file or folder. If folder is provided, species list needs to be named "species_list.txt". If lat and lon are provided, this list will be ignored.',
    )
    parser.add_argument(
        "--sensitivity",
        type=float,
        default=1.0,
        help="Detection sensitivity; Higher values result in higher sensitivity. Values in [0.5, 1.5]. Defaults to 1.0.",
    )
    parser.add_argument(
        "--min_conf", type=float, default=0.1, help="Minimum confidence threshold. Values in [0.01, 0.99]. Defaults to 0.1."
    )
    parser.add_argument(
        "--overlap", type=float, default=0.0, help="Overlap of prediction segments. Values in [0.0, 2.9]. Defaults to 0.0."
    )
    parser.add_argument(
        "--rtype",
        default="table",
        help="Specifies output format. Values in ['table', 'audacity', 'r',  'kaleidoscope', 'csv']. Defaults to 'table' (Raven selection table).",
    )
    parser.add_argument("--threads", type=int, default=4, help="Number of CPU threads.")
    parser.add_argument(
        "--batchsize", type=int, default=1, help="Number of samples to process at the same time. Defaults to 1."
    )
    parser.add_argument(
        "--locale",
        default="en",
        help="Locale for translated species common names. Values in ['af', 'de', 'it', ...] Defaults to 'en'.",
    )
    parser.add_argument(
        "--sf_thresh",
        type=float,
        default=0.03,
        help="Minimum species occurrence frequency threshold for location filter. Values in [0.01, 0.99]. Defaults to 0.03.",
    )
    parser.add_argument(
        "--classifier",
        default=None,
        help="Path to custom trained classifier. Defaults to None. If set, --lat, --lon and --locale are ignored.",
    )

    args = parser.parse_args()

    # Set paths relative to script path (requested in #3)
    script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    config.MODEL_PATH = os.path.join(script_dir, config.MODEL_PATH)
    config.LABELS_FILE = os.path.join(script_dir, config.LABELS_FILE)
    config.TRANSLATED_LABELS_PATH = os.path.join(script_dir, config.TRANSLATED_LABELS_PATH)
    config.MDATA_MODEL_PATH = os.path.join(script_dir, config.MDATA_MODEL_PATH)
    config.CODES_FILE = os.path.join(script_dir, config.CODES_FILE)
    config.ERROR_LOG_FILE = os.path.join(script_dir, config.ERROR_LOG_FILE)

    # Load eBird codes, labels
    config.CODES = load_codes()
    config.LABELS = utils.read_lines(config.LABELS_FILE)

    # Set custom classifier?
    if args.classifier is not None:
        config.CUSTOM_CLASSIFIER = args.classifier  # we treat this as absolute path, so no need to join with dirname
        config.LABELS_FILE = args.classifier.replace(".tflite", "_Labels.txt")  # same for labels file
        config.LABELS = utils.read_lines(config.LABELS_FILE)
        args.lat = -1
        args.lon = -1
        args.locale = "en"

    # Load translated labels
    lfile = os.path.join(
        config.TRANSLATED_LABELS_PATH, os.path.basename(config.LABELS_FILE).replace(".txt", "_{}.txt".format(args.locale))
    )

    if not args.locale in ["en"] and os.path.isfile(lfile):
        config.TRANSLATED_LABELS = utils.read_lines(lfile)
    else:
        config.TRANSLATED_LABELS = config.LABELS

    ### Make sure to comment out appropriately if you are not using args. ###

    # Load species list from location filter or provided list
    config.LATITUDE, config.LONGITUDE, config.WEEK = args.lat, args.lon, args.week
    config.LOCATION_FILTER_THRESHOLD = max(0.01, min(0.99, float(args.sf_thresh)))

    if config.LATITUDE == -1 and config.LONGITUDE == -1:
        if not args.slist:
            config.SPECIES_LIST_FILE = None
        else:
            config.SPECIES_LIST_FILE = os.path.join(script_dir, args.slist)

            if os.path.isdir(config.SPECIES_LIST_FILE):
                config.SPECIES_LIST_FILE = os.path.join(config.SPECIES_LIST_FILE, "species_list.txt")

        config.SPECIES_LIST = utils.read_lines(config.SPECIES_LIST_FILE)
    else:
        config.SPECIES_LIST_FILE = None
        config.SPECIES_LIST = species.get_species_list(config.LATITUDE, config.LONGITUDE, config.WEEK, config.LOCATION_FILTER_THRESHOLD)

    if not config.SPECIES_LIST:
        print(f"Species list contains {len(config.LABELS)} species")
    else:
        print(f"Species list contains {len(config.SPECIES_LIST)} species")

    # Set input and output path
    config.INPUT_PATH = args.i
    config.OUTPUT_PATH = args.o

    # Parse input files
    if os.path.isdir(config.INPUT_PATH):
        config.FILE_LIST = utils.collect_audio_files(config.INPUT_PATH)
        print(f"Found {len(config.FILE_LIST)} files to analyze")
    else:
        config.FILE_LIST = [config.INPUT_PATH]

    # Set confidence threshold
    config.MIN_CONFIDENCE = max(0.01, min(0.99, float(args.min_conf)))

    # Set sensitivity
    config.SIGMOID_SENSITIVITY = max(0.5, min(1.0 - (float(args.sensitivity) - 1.0), 1.5))

    # Set overlap
    config.SIG_OVERLAP = max(0.0, min(2.9, float(args.overlap)))

    # Set result type
    config.RESULT_TYPE = args.rtype.lower()

    if not config.RESULT_TYPE in ["table", "audacity", "r", "kaleidoscope", "csv"]:
        config.RESULT_TYPE = "table"

    # Set number of threads
    if os.path.isdir(config.INPUT_PATH):
        config.CPU_THREADS = max(1, int(args.threads))
        config.TFLITE_THREADS = 1
    else:
        config.CPU_THREADS = 1
        config.TFLITE_THREADS = max(1, int(args.threads))

    # Set batch size
    config.BATCH_SIZE = max(1, int(args.batchsize))

    # Add config items to each file list entry.
    # We have to do this for Windows which does not
    # support fork() and thus each process has to
    # have its own config. USE LINUX!
    flist = [(f, config.get_config()) for f in config.FILE_LIST]

    # Analyze files
    if config.CPU_THREADS < 2:
        for entry in flist:
            analyze_file(entry)
    else:
        with Pool(config.CPU_THREADS) as p:
            p.map(analyze_file, flist)

    # A few examples to test
    # python3 analyze.py --i example/ --o example/ --slist example/ --min_conf 0.5 --threads 4
    # python3 analyze.py --i example/soundscape.wav --o example/soundscape.BirdNET.selection.table.txt --slist example/species_list.txt --threads 8
    # python3 analyze.py --i example/ --o example/ --lat 42.5 --lon -76.45 --week 4 --sensitivity 1.0 --rtype table --locale de
