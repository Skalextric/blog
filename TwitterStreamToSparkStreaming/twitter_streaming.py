from twitter_keys import *

from twython import Twython
from twython import TwythonStreamer

from socket import socket

twitter = Twython(consumer_key, consumer_secret, access_token, access_token_secret)
twitter.verify_credentials()


class MyStreamer(TwythonStreamer):

    def __init__(self, app_key, consumer_secret, access_token, acces_token_secret, file, socket_output):
        super(MyStreamer, self).__init__(app_key, consumer_secret, access_token, acces_token_secret)
        self.file = file
        self.socket = socket_output

    def on_success(self, data):
        #print(data)
        location = '' if data['user']['location'] is None else data['user']['location']
        dats = data['user']['screen_name'] + " => " + location + ":\n" + data['text'] + "\n"
        self.file.write(dats)
        self.socket.send(dats.encode())
        print(dats)

    def on_error(self, status_code, data):
        print(status_code)

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        # self.disconnect()


output_file = open("streaming.txt", 'w')
socket_output = socket()
socket_output.bind(('localhost', 9999))
socket_output.listen(5)
print("Server waiting...")
conn, addr = socket_output.accept()
print("Connecting to {}".format(addr))

stream = MyStreamer(consumer_key, consumer_secret, access_token, access_token_secret, output_file, conn)
stream.statuses.filter(track='python')
