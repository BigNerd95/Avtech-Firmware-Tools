#!/usr/bin/env python3

# Avtech Firmware Tool by BigNerd95

from argparse import ArgumentParser, FileType
from struct import pack, unpack
import sys



class Object(object):
    pass

def print_info(header_info):
    print('Product:', header_info.product)
    print('Description:', header_info.description)
    print('Version:', header_info.version)
    print('Checksum:', hex(header_info.checksum))

def parse_header(header_data):
    if len(header_data) == 200:
        headerUnpacked = unpack('I64s64s64sI', header_data)
        parsedHeader = Object()
        parsedHeader.magic = headerUnpacked[0]
        parsedHeader.product = str(headerUnpacked[1], 'ascii', 'ignore').split('\x00')[0]
        parsedHeader.description = str(headerUnpacked[2], 'ascii', 'ignore').split('\x00')[0]
        parsedHeader.version = str(headerUnpacked[3], 'ascii', 'ignore').split('\x00')[0]
        parsedHeader.checksum = headerUnpacked[4]
        return parsedHeader
    else:
        print('Error! File too short')
        sys.exit(1)

def create_header(product, description, version, checksum):
    return pack('I64s64s64sI', 200, bytes(product[:63], 'ascii'), bytes(description[:63], 'ascii'), bytes(version[:63], 'ascii'), checksum)

def calc_checksum(fileData):
    return sum(bytearray(fileData)) # calculates checksum

def split_file(file_data):
    return (file_data[:200], file_data[200:])

def read_file(input_file):
    file_data = input_file.read()
    input_file.close()
    return file_data

def write_file(output_file, file_data):
    output_file.write(file_data)
    output_file.close()



def fw_sign(input_file, output_file, product, description, version):
    print('** Sign firmware **')
    file_data = read_file(input_file)
    header_data, body_data = split_file(file_data)
    header_info = parse_header(header_data)
    if header_info.magic != 200:
        body_data = file_data
        checksum = calc_checksum(body_data)
        header_data = create_header(product, description, version, checksum)
        header_info = parse_header(header_data)
        print_info(header_info)
        write_file(output_file, header_data + body_data)
        print('Firmware signed successfully')
    else:
        print('Error! Signature not needed (firmware already signed)')
        sys.exit(1)


def fw_unsign(input_file, output_file):
    print('** Unsign firmware **')
    file_data = read_file(input_file)
    header_data, body_data = split_file(file_data)
    header_info = parse_header(header_data)
    if header_info.magic == 200:
        print_info(header_info)
        checksum = calc_checksum(body_data)
        if checksum == header_info.checksum:
            write_file(output_file, body_data)
            print('Firmware unsigned successfully')
        else:
            print('Error! Corrupted firmware (checksum does not match)')
            sys.exit(1)
    else:
        print('Error! Invalid firmware (not signed firmware)')
        sys.exit(1)


def fw_info(input_file):
    print('** Show firmware info **')
    file_data = read_file(input_file)
    header_data, body_data = split_file(file_data)
    header_info = parse_header(header_data)
    if header_info.magic == 200:
        print_info(header_info)
    else:
        print('Error! Invalid firmware (not signed firmware)')
        sys.exit(1)


def parse_cli():
    parser = ArgumentParser(description='** Avtech Firmware signer By BigNerd95 **')
    subparser = parser.add_subparsers(dest='subparser_name')

    signParser = subparser.add_parser('sign', help='Sign firmware')
    signParser.add_argument('-i', '--input', required=True, metavar='INPUT_FILE', type=FileType('rb'))
    signParser.add_argument('-o', '--output', required=True, metavar='OUTPUT_FILE', type=FileType('wb'))
    signParser.add_argument('-p', '--product', required=True, metavar='PRODUCT_NAME')
    signParser.add_argument('-d', '--description', required=True, metavar='FILE_DESCRIPTION')
    signParser.add_argument('-v', '--version', required=True, metavar='FILE_VERSION')

    unsignParser = subparser.add_parser('unsign', help='Unsign firmware')
    unsignParser.add_argument('-i', '--input', required=True, metavar='INPUT_FILE', type=FileType('rb'))
    unsignParser.add_argument('-o', '--output', required=True, metavar='OUTPUT_FILE', type=FileType('wb'))

    infoParser = subparser.add_parser('info', help='Show firmware info')
    infoParser.add_argument('-i', '--input', required=True, metavar='INPUT_FILE', type=FileType('rb'))
    
    if len(sys.argv) < 2:
        parser.print_help()

    return parser.parse_args()


def main():
    args = parse_cli()
    if args.subparser_name == 'sign':
        fw_sign(args.input, args.output, args.product, args.description, args.version)
    elif args.subparser_name == 'unsign':
        fw_unsign(args.input, args.output)
    elif args.subparser_name == 'info':
        fw_info(args.input)
    
if __name__ == '__main__':
    main()
