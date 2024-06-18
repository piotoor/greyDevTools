import logging
import os

def write_to_bin_file(out_path, data):
    greyLogger.debug("start")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    try:
        with open(out_path, 'w+b') as bin_file:
            try:
                # print("Saving {}...".format(sbf))
                bin_file.write(bytearray(data))
            except (IOError, OSError) as e:
                greyLogger.error(e)
    except (FileNotFoundError, PermissionError, OSError) as e:
        greyLogger.error(e)


def read_from_bin_file(in_path):
    greyLogger.debug("start")
    try:
        with open(in_path, 'rb') as bin_file:
            try:
                # print("Reading {}...".format(sbf))
                data = bin_file.read()
                return data
            except (IOError, OSError) as e:
                greyLogger.error(e)
                raise
    except (FileNotFoundError, PermissionError, OSError) as e:
        greyLogger.error(e)
        raise


greyLogger = logging.getLogger("greyDevTools")
greyLogger.setLevel(level=logging.ERROR)
fh = logging.StreamHandler()
fh_formatter = logging.Formatter('%(asctime)s %(levelname)6s %(lineno)5d:%(filename)s%(funcName)45s() - %(message)s')
fh.setFormatter(fh_formatter)
greyLogger.addHandler(fh)
