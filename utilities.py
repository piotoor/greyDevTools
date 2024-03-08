def write_to_bin_file(out_path, data):
    try:
        with open(out_path, 'wb') as bin_file:
            try:
                # print("Saving {}...".format(sbf))
                bin_file.write(bytearray(data))
            except (IOError, OSError):
                print("Error writing to file")
    except (FileNotFoundError, PermissionError, OSError) as e:
        print("Error opening file: ", e)


def read_from_bin_file(out_path, data):
    try:
        with open(out_path, 'rb') as bin_file:
            try:
                # print("Reading {}...".format(sbf))
                data = bin_file.read()
            except (IOError, OSError):
                print("Error reading from file")
    except (FileNotFoundError, PermissionError, OSError) as e:
        print("Error opening file: ", e)

