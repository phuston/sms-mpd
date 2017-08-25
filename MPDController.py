__author__ = "Patrick Huston"
__version__ = "0.1"
__email__ = "patrick@students.olin.edu"

from contextlib import contextmanager
from mpd import MPDClient
import time

class MPDController:
    """
    Handles all MPD client connection control
    """

    def __init__(self):
        self.client = MPDClient()
        self.client.timeout = 20
        self.client.idletimeout = None

    @contextmanager
    def connection(self):
        try:
            self.client.connect('localhost', 6600)
            yield
        finally:
            self.client.close()
            self.client.disconnect()

    def handle_sms_request(self, request):
        state = request.cookies.get('state', 'none')
    
        route_state_func = {
            "none": self.handle_base_state,
            "search": self.handle_search_state
        }.get(state)

        return route_state_func(request)

    def handle_base_state(self, request):
        command, arguments = self.sanitize_message(request.form['Body'])
        if arguments:
            return self.handle_multi_base_state(command, arguments)
        else:
            return self.handle_single_base_state(command)
        
    def handle_search_state(self, request):
        selection = request.form['Body']
        return "YEEE"

    def handle_single_base_state(self, command):
        command_func = {
            "play": self.play,
            "pause": self.pause,
            "next": self.client.next,
            "previous": self.client.previous,
            "volup": self.increase_volume,
            "voldown": self.decrease_volume,
            "getiton": self.initiate_get_it_on,
            "champions": self.initiate_champions
        }.get(command, None)
        
        if command_func:
            return self.do_mpd(command_func)
        else:
            print "Command failed: {}".format(command)
            return "Command not found. Text HELP or bother Patrick"

    def handle_multi_base_state(self, command, arguments):
        command_func = {
            "play": self.handle_play_command
        }.get(command, None)

        if command_func:
            return command_func(arguments)
        else:
            print "Command failed: {}".format(command)
            return "Command not found. Text HELP or bother Patrick"

    def handle_play_command(self, track_description):
        return

    def do_mpd(self, mpd_func):
        try:
            with self.connection():
                mpd_func()
            return "Success!"
        except Exception as error:
            print error
            return "Something broke. Tell Patrick to fix it. If you care, here's the error: {}".format(error)

    def sanitize_message(self, raw_message):
        message_arr = raw_message.lower().split(" ")
        command = message_arr[0]
        arguments = message_arr[1:] if (len(message_arr) > 1) else None
        return command, arguments

    def describe_commands(self):
        "Help yoself bitch!"

    def play(self):
        self.client.pause(0)

    def pause(self):
        self.client.pause(1)

    def increase_volume(self):
        self.client.setvol(int(self.client.status()['volume']) + 10)

    def decrease_volume(self):
        self.client.setvol(int(self.client.status()['volume']) - 10)

    def initiate_get_it_on(self):
        self.initiate_special_track("spotify:track:39l1UORIhuHvUWfxG53tRZ", "local:track:getiton.mp3")

    def initiate_champions(self):
        self.initiate_champions("spotify:track:7ccI9cStQbQdystvc6TvxD", "local:track:getiton.mp3")

    def initiate_special_track(self, spotify_uri, local_uri):
        self.client.stop()
        self.client.clear()
        self.client.add(local_uri)
        self.client.add(spotify_uri)
        self.client.play()
