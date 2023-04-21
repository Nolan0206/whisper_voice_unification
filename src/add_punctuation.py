import sys
from typing import Union

import pandas as pd
import paddle
from tqdm import tqdm
from paddlespeech.cli.text import TextExecutor


class AddPunctuation(object):
    """
    This is a class that add punctuation to sentence

    This class adds punctuation to the content of the sentence in the csv and saves it to the original file

    Attributes:
        text_executor: Paddlespeech ...
        csv_list: Full list of pathname of the csv files

    """

    def __init__(self, csv_list: Union[list, set, tuple]):
        """This is initial function"""
        self.text_executor = TextExecutor()
        self.csv_list = csv_list

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

    def add_punc(self):
        """
        This is a function to add punctuation

        Args:

        Returns:
            None
        """
        if not self._judge(self.csv_list):
            sys.exit()
        for file in tqdm(self.csv_list, position=0, desc="file", leave=False, colour='green'):
            content = pd.read_csv(file, sep="\t")
            for index in tqdm(range(content.shape[0]), position=1, desc="content", leave=False, colour='green'):
                content.sentence[index] = self.text_executor(text=content.sentence[index], task='punc',
                                                             model='ernie_linear_p7_wudao', lang='zh', config=None,
                                                             ckpt_path=None, punc_vocab=None,
                                                             device=paddle.get_device())
            content.to_csv(file, index=False, sep='\t')


if __name__ == '__main__':
    text_executor = TextExecutor()
    text = text_executor(text="你好小明明天一起去钓鱼吗", task='punc',
                         model='ernie_linear_p7_wudao', lang='zh', config=None,
                         ckpt_path=None, punc_vocab=None,
                         device=paddle.get_device())
    print(text)
