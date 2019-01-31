'''
Ulauncher extension main  class
'''

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction


class SlashesExtension(Extension):

    def __init__(self):
        super(SlashesExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

    def show_empty_results(self):
        '''
        Show error message
        '''
        return RenderResultListAction([
            ExtensionResultItem(
                icon='images/icon.png',
                name='Clipboard is empty',
                on_enter=HideWindowAction())])

    def show_clipboard_list(self, text):
        '''
        Show the list of possible clipboard conversions
        '''
        text = text.strip()
        items = [
            {
                'name': 'Straight slashes (/)',
                'result': text.replace('\\', '/'),
            },
            {
                'name': 'Backward slashes (\\)',
                'result': text.replace('/', '\\'),
            },
            {
                'name': 'Escaped backward slashes (\\\\)',
                'result': text.replace('/', '\\').replace('\\', '\\\\'),
            },
            {
                'name': 'Unescaped backward slashes (\\)',
                'result': text.replace('\\\\', '\\'),
            },
            {
                'name': 'Unescaped straight slashes (/)',
                'result': text.replace('\\\\', '\\').replace('\\', '/'),
            },
            {
                'name': 'Add double quotes',
                'result': '"' + text + '"',
            },
            {
                'name': 'Add single quotes',
                'result': "'" + text + "'",
            },
            {
                'name': 'Remove quotes',
                'result': text.replace('"', '').replace("'", ''),
            },
        ]
        results_list = []
        for item in items:
            results_list.append(
                ExtensionResultItem(
                    icon='images/icon.png',
                    name=item.get('name'),
                    description=item.get('result'),
                    on_enter=CopyToClipboardAction(item.get('result'))))
        return RenderResultListAction(results_list)


class KeywordQueryEventListener(EventListener):
    '''
    Handles Keyboard input
    '''

    def on_event(self, event, extension):
        '''
        Handle the event
        '''
        argument = event.get_argument()
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        text = clipboard.wait_for_text()
        if not text:
            return extension.show_empty_results()
        return extension.show_clipboard_list(text)


if __name__ == '__main__':
    SlashesExtension().run()
