import sys
import os
import json
from typing import Union

import pandas as pd
from pathlib import Path
from pydub import AudioSegment
from colorama import Fore
from tqdm import tqdm


# all paths without / at the end

# Update the path to read audio
def update_path(path):
    new_path = f"/home/nolan/DOCKER_SHARE/whisper/V1_0_0/{path}"
    return new_path


class VoiceFormatConvert(object):
    """
    This is a class that does conversions for audio

    This class can convert opus voice format to MP3, WAV and other formats, while the voice and corresponding text in
    the json file will be stored in csv, which is convenient for subsequent addition to the dataset

    Attributes:
        _filelist: Full list of pathname of the incoming json files, private attribute
        new_path: Name of the parent folder where all converted voices are stored
    """

    def __init__(self, filelist: Union[list, set, tuple], new_path):
        """This is initial function"""
        self._filelist = filelist
        self.new_path = new_path

    @property
    def filelist(self):
        return self._filelist

    @filelist.setter
    def filelist(self, filelist: Union[list, set, tuple]):
        self._filelist = filelist

    @staticmethod
    def _judge(list_: Union[list, set, tuple]):
        try:
            if not list_:
                raise IndexError("The list passed in is empty")
        except IndexError as error:
            print("引发异常：", repr(error))
            return False
        else:
            return True

    @staticmethod
    def _make_new_dirs(dir_name: str):
        try:
            os.makedirs(dir_name, exist_ok=False)
        except FileExistsError:
            print(Fore.BLUE + "[notice]", Fore.RED + "{}".format(dir_name), "already exists. If there is no problem "
                                                                            "with this path, please ignore this notice")

    @staticmethod
    def _convert_format(audio, file_parent: Path, num: int, type_: str):
        audio_clips_name = f"{file_parent}/{str(num).zfill(9)}.{type_}"
        resampled_audio = audio.set_frame_rate(16000).set_channels(1)
        resampled_audio.export(audio_clips_name, format=type_)
        return audio_clips_name

    def opus_to_mp3(self, csv_path: str) -> list[str]:
        """
        This is a function to convert opus to MP3

        Args:
            csv_path(str):Parent path to store csv files

        Returns:
            list[str]
        """
        if not self._judge(self._filelist):
            sys.exit()
        self._make_new_dirs(self.new_path)
        csv_path_list = []
        for file in tqdm(self.filelist, position=0, desc="file", leave=False, colour='green'):
            audio_parent_path = Path(self.new_path).joinpath(Path(file).stem)
            self._make_new_dirs(audio_parent_path)
            with open(file, "r", encoding="utf-8") as audio:
                content = json.load(audio)
            voice_item = content['audios']
            voice_list, text_list = [[] for _ in range(2)]
            count_num = 0
            for aid in tqdm(range(len(voice_item)), position=1, desc="voice_item", leave=False, colour='green'):
                segments = voice_item[aid]['segments']
                path_to_opus = update_path(voice_item[aid]['path'])
                sound = AudioSegment.from_file(path_to_opus, codec="opus")
                for seg_num in range(len(segments)):
                    text_list.append(segments[seg_num]['text'])
                    audio_clips = sound[segments[seg_num]['begin_time'] * 1000:segments[seg_num]['end_time'] * 1000]
                    audio_clips_name = self._convert_format(audio_clips, audio_parent_path, count_num, "mp3")
                    voice_list.append(audio_clips_name)
                    count_num += 1

            dataset = list(zip(voice_list, text_list))
            dataset = pd.DataFrame(dataset, columns=['audio', 'sentence'])
            dataset.to_csv(f"{csv_path}/{Path(file).stem}.csv", sep='\t', index=False, header=True)
            csv_path_list.append(f"{csv_path}/{Path(file).stem}.csv")
        return csv_path_list


'''Older versions, not working need to roll back'''
# for seg_num in range(len(segments)):
#     seg_begin = segments[seg_num]['begin_time'] * 1000
#     seg_end = segments[seg_num]['end_time'] * 1000
#     text = segments[seg_num]['text']
#     audio_clips = sound[seg_begin:seg_end]
#     # audio_parent_path = Path(self.new_path).joinpath(Path(file).stem)
#     audio_clips_name = f"{self.new_path}/{file_path.stem}/{str(count_num).zfill(9)}.mp3"
#
#     resampled_audio = audio_clips.set_frame_rate(16000).set_channels(1)
#     resampled_audio.export(audio_clips_name, format="mp3")
#
#     voice_list.append(audio_clips_name)
#     text_list.append(text)
#     count_num += 1
# dataset = list(zip(voice_list, text_list))
# dataset = pd.DataFrame(dataset, columns=['audio', 'sentence'])
#
# dataset.to_csv(csv_path, sep='\t', index=False, header=True)
