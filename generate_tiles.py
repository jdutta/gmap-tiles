import json
import os
import subprocess

class Utils():

    @staticmethod
    def convert_utf8_to_str(input):
        if isinstance(input, dict):
            return {Utils.convert_utf8_to_str(key): Utils.convert_utf8_to_str(value) for key, value in input.iteritems()}
        elif isinstance(input, list):
            return [Utils.convert_utf8_to_str(element) for element in input]
        elif isinstance(input, unicode):
            return input.encode('utf-8')
        else:
            return input

    @staticmethod
    def read_config_file(filename):
        file = open(filename)
        str = file.read()
        str = str.replace('\n', '')
        return json.loads(str, object_hook=Utils.convert_utf8_to_str)


class GmapTileGenerator():

    _config = None

    def __init__(self, cfg_file):
        GmapTileGenerator._config = Utils.read_config_file(cfg_file)

    @staticmethod
    def _check_images_dir():
        dir = GmapTileGenerator._config['images-dir']
        if not os.path.exists(dir):
            os.makedirs(dir)
            return True
        return False

    @staticmethod
    def _get_image_filename(row_index, col_index):
        return 'tile-' + format(row_index, '02') + '-' + format(col_index, '02') + '.png'

    @staticmethod
    def generate_screenshots():
        if not GmapTileGenerator._check_images_dir():
            print 'Remove folder \'' + GmapTileGenerator._config['images-dir'] + '\' and retry.'
            return

        config = GmapTileGenerator._config
        zoom = config['zoom']
        start_coord = config['start-coord']
        end_coord = config['end-coord']
        row_index = 0
        latitude = start_coord['lat']
        while latitude > end_coord['lat']:
            longitude = start_coord['long']
            col_index = 0
            while longitude < end_coord['long']:
                url = config['url-template'].replace('__LAT__', str(latitude)).replace('__LONG__', str(longitude)).replace('__ZOOM__', str(zoom))
                image_file_path = config['images-dir'] + '/' + GmapTileGenerator._get_image_filename(row_index, col_index)
                curl_command = 'curl "' + url + '" > ' + image_file_path
                print 'Fetching tile at zoom: ' + str(zoom) + ' with latitude: ' + str(latitude) + ' and longitude: ' + str(longitude) + ', to image file: ' + image_file_path
                subprocess.call(curl_command, shell=True)
                longitude += config['increment']
                col_index += 1
            latitude -= config['increment']
            row_index += 1


sg = GmapTileGenerator('config.json')
sg.generate_screenshots()