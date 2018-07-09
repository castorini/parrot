import argparse
import os

from pydub import AudioSegment

def main():
    parser = argparse.ArgumentParser(
        description="add silence at the beginning and end of all wav files in a directory")
    parser.add_argument('length', type=float,
        help='preferred length of silence (in second)', default=5)
    parser.add_argument('--directories', nargs='*',
        help='name of the directories', default=[])
    args = parser.parse_args()

    #Create silence
    silence = AudioSegment.silent(duration=args.length * 1000)

    for directory in args.directories:
        #Create a new directory
        path_name = directory + '_with_silence'
        if not os.path.exists(path_name):
            os.makedirs(path_name)
            print(path_name + ' directory is created!')

        #Append silence to each wav file
        for filename in os.listdir(directory):
            audio = AudioSegment.from_wav(directory + '/' + filename)
            new_audio = silence + audio + silence
            new_filename = path_name + '/' + filename.replace('.wav', '') + '_silence.wav'
            new_audio.export(new_filename, format="wav")

        print('all audios in ' + directory + ' are done!')


if __name__ == '__main__':
    main()
        