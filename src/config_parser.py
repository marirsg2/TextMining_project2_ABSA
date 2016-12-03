import configparser

config = configparser.ConfigParser()
config.read('config.ini')

if 'pickles' not in config:
    print ('Config file not right')

pickleFolder = config['pickles']['pickleFolder']
pickleFile = config['pickles']['pickleFile']
