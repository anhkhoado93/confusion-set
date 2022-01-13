import argparse



if __name__ == '__main__':
    my_parser = argparse.ArgumentParser(description='preprocess pipeline')
    my_parser.add_argument('-nt',
                        '--normalize-tonemark',
                        action='store_false',
                        help='convert all tonemark to default style [VietnameseTextNormalizer]')
    my_parser.add_argument('-nu',
                        '--normalize-unicode',
                        action='store_false',
                        help='composite unicode to ... unicode [VietnameseTextNormalizer]')
    my_parser.add_argument('-rb',
                            '--remove-badword',
                            action='store_false',
                            help='remove all sentences with bad words')
    my_parser.add_argument('-ru',
                            '--remove-unacceptable',
                            action='store_false',
                            help='remove all unacceptable character like html tag, emoji [VietnameseTextNormalizer]')
    my_parser.add_argument('--save-non-viet',
                            action='store_false',
                            help='save all non-Viet words in a file')
    my_parser.add_argument('-mu',
                            '--maximum-unknown',
                            type=int,
                            required=True,
                            action="store",
                            help='maximum non-Viet word in a sentence')

    args = my_parser.parse_args()

