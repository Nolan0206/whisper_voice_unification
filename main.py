from colorama import init
import warnings
import argparse


from src import *

init(autoreset=True)
warnings.filterwarnings('ignore')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='whisper_voice_unification')
    parser.add_argument('--catalog', default=None, required=True, help='txt<catalog or dir<catalog')
    parser.add_argument('-convert', '--convert', default=False, action='store_true', help='convert or not')
    parser.add_argument('-punc', '--punc', default=False, action='store_true', help='add punctuation or not')
    parser.add_argument('--voice_path', default=None, type=str, help='Name of the parent folder where all '
                                                                     'converted voices are stored')
    parser.add_argument('--csv_path', default=None, type=str, help='Name of the parent folder where all csv are stored')

    args = parser.parse_args()
    if args.convert:
        if args.voice_path is None or args.csv_path is None:
            parser.error('With convert, a path value is required')
    show_argparse(args)

    file_list = read_config(args.catalog)
    if file_list is None:
        print(Fore.RED + "There are no documents to process")
        sys.exit()
    else:
        print(file_list)

    if args.convert:
        convert = VoiceFormatConvert(file_list, args.voice_path)
        csv_list = convert.opus_to_mp3(args.csv_path)
        if args.punc:
            punc = AddPunctuation(csv_list)
            punc.add_punc()
    elif args.punc:
        punc = AddPunctuation(file_list)
        punc.add_punc()
    else:
        print("Nothing is happening, please use", Fore.RED + "python main.py -h")

