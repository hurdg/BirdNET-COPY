import os
from typing import Dict
from typing import Tuple
from typing import List

import audio
import config as cfg
import utils


def extract_segments(item: Tuple[Tuple[str, List[Dict]], float, Dict[str, str]]):
    """Saves each segment separately.
    Creates an audio file for each species segment.
    Args:
        item: A tuple that contains ((audio file path, segments), segment length, config)
    """
    # Paths and config
    afile = item[0][0]
    segments = item[0][1]
    seg_length = item[1]
    cfg.set_config(item[2])

    # Status
    print(f"Extracting segments from {afile}")

    try:
        # Open audio file
        sig, _ = audio.open_audio_file(afile, cfg.SAMPLE_RATE)
    except Exception as ex:
        print(f"Error: Cannot open audio file {afile}", flush=True)
        utils.write_error_log(ex)

        return

    # Extract segments
    for seg_cnt, seg in enumerate(segments, 1):
        try:
            # Get start and end times
            start = int(seg["start"] * cfg.SAMPLE_RATE)
            end = int(seg["end"] * cfg.SAMPLE_RATE)
            offset = ((seg_length * cfg.SAMPLE_RATE) - (end - start)) // 2
            start = max(0, start - offset)
            end = min(len(sig), end + offset)

            # Make sure segment is long enough
            if end > start:
                # Get segment raw audio from signal
                seg_sig = sig[int(start) : int(end)]

                # Make output path
                outpath = os.path.join(cfg.OUTPUT_PATH, seg["species"])
                os.makedirs(outpath, exist_ok=True)

                # Save segment
                seg_name = "{:.3f}_{}_{}.wav".format(
                    seg["confidence"], seg_cnt, seg["audio"].rsplit(os.sep, 1)[-1].rsplit(".", 1)[0]
                )
                seg_path = os.path.join(outpath, seg_name)
                audio.save_signal(seg_sig, seg_path)

        except Exception as ex:
            # Write error log
            print(f"Error: Cannot extract segments from {afile}.", flush=True)
            utils.write_error_log(ex)
            return False

    return True