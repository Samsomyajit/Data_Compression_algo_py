"""
Python script for compressing files using the LZW algorithm.
This will have a high compression rate with files that have a high repetition of bytes (e.g.: GIF files).
"""

from argparse import ArgumentParser


def get_input_args():
    parser = ArgumentParser(
        "Python script for compressing files with the LZW algorithm.")
    parser.add_argument('--in_file', '-i', type=str,
                        required=True, help="The file to be compressed.")
    parser.add_argument('--out_file', '-o', type=str,
                        required=True, help="The destination output file.")
    return parser.parse_args()


def read_contents(in_file):
    with open(in_file, "rb") as inf:
        contents = inf.read()
        if len(contents) <= 0:
            print("This file is empty. Aborting operation...")
            exit(1)
        return contents


def lzw(in_file, out_file):

    # Read file contents
    original_contents = read_contents(in_file)

    # Initialize substring map
    substr_codes = {chr(c): c for c in range(256)}
    next_code = 256

    # Compress file
    compressed_contents = []
    current_substr = chr(original_contents[0])
    trailing_substr = ""

    for i in range(len(original_contents)):
        if i != len(original_contents)-1:
            trailing_substr += chr(original_contents[i+1])
        if (current_substr + trailing_substr) in substr_codes:
            current_substr += trailing_substr
        else:
            compressed_contents.append(substr_codes[current_substr])
            substr_codes[current_substr + trailing_substr] = next_code
            next_code += 1
            current_substr = trailing_substr
        trailing_substr = ""

    # Write compressed file
    with open(out_file, "w") as of:
        of.write(
            ",".join(list(map(lambda x: hex(x)[2:], compressed_contents))))


if __name__ == "__main__":
    args = get_input_args()
    # pass the file path to the lzw function
    lzw(args.in_file, args.out_file)
