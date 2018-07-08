import argparse
import os

from pydub import AudioSegment

def main():
    parser = argparse.ArgumentParser(
        description = "split a .wav file into multiple .wav files with same length")
    parser.add_argument('filename', help='name of the wav file that will be splitted')
    parser.add_argument('length', type=int, default=5,
        help='preferred length to split (in second)')
    args = parser.parse_args()

    #Create a new directory for splitted wav files
    path_name = args.filename.replace('.wav', '') + '_splitted'
    if not os.path.exists(path_name):
        os.makedirs(path_name)
        print(path_name + ' directory is created!')

    #Slice audio
    audio = AudioSegment.from_wav(args.filename)
    n = audio.duration_seconds // args.length

    for i in range(0, (int)(n * args.length), args.length):
        new_audio = audio[(i * 1000): ((i + args.length) * 1000)]
        new_filename = path_name + '/' + path_name + '_' + str(i) + '.wav'
        new_audio.export(new_filename, format="wav")

if __name__ == '__main__':
    main()
