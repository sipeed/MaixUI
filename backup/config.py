import ujson
import sys

config_path = "/flash/config.json"

normal_brightness = 8

config_cache = None


def get_config():
    global config_cache
    if config_cache is None:
        conf = {}
        try:
            f = open(config_path, "rb")
            conf = ujson.load(f)
            f.close()
        except OSError:
            print("config file not exist, use default dict")
        except ValueError:
            print("invalid config file format, use default dict")
        if type(conf) is not dict:
            conf = {}
        config_cache = conf
    return config_cache


def save_config(key, value):
    config = get_config()
    config[key] = value
    save_config_to_file(config)


def save_config_to_file(config):
    try:
        f = open(config_path, "wb")
        ujson.dump(config, f)
        f.close()
    except OSError as e:
        sys.print_exception(e)
    print("save_config_to_file end")


def get_config_by_key(key):
    config = get_config()
    if key in config:
        return config[key]
    else:
        return None


def get_brightness():
    brightness_conf = get_config_by_key("brightness")
    return brightness_conf if brightness_conf is not None else normal_brightness
