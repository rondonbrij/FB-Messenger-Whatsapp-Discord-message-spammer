#!/usr/bin/env Python3
import PySimpleGUI as sg
import queue
import threading
import settings
import unsend

def long_operation_thread():
    unsend.start_unsend()

# The UI
def the_gui():
    # sets theme
    sg.ChangeLookAndFeel('DarkBlue9')
    gui_queue = queue.Queue()

    # Output Console
    output = [
        [sg.Frame(layout=[
            [sg.Output(size=(42, 8), pad=(0, 0))],
        ], title='Output', title_color="#ffffff")], ]

    # Main Layout
    layout = [
        [sg.Frame(layout=[
            [sg.Text('Choose Platform:', size=(17, 1), font=("Roboto", 8)),
             sg.InputCombo(('Messenger',), default_value="Messenger", key="source", size=(25, 1))],
            [sg.Text('Friend Name:', size=(17, 1), font=("Roboto", 8)),
             sg.InputText('', key="friend_name", size=(27, 1))],
            [sg.Text('Username/Email:', size=(17, 1), font=("Roboto", 8)),
             sg.InputText('', key="username_email", size=(27, 1))],
            [sg.Text('Password:', size=(17, 1), font=("Roboto", 8)),
             sg.InputText('', key="password", password_char='*', size=(27, 1))],
            [sg.Text('Delay (seconds):', size=(17, 1), font=("Roboto", 8)),
             sg.Spin(values=('0', '.5', '1', '1.5', '2', '2.5', '3'), key="delay", initial_value='1', size=(6, 1), tooltip="wait time between actions")],
        ],
            title='Login', title_color="#ffffff"), sg.Column(output)],

        [sg.Button('Run', size=(10, 1), key="Run"), sg.Button('Exit', size=(10, 1))]
    ]

    # Window options
    window = sg.Window('Made with love - by Henry Albuquerque', layout, default_element_size=(40, 1), grab_anywhere=False,
                       location=(5, 5))

    while True:
        event, values = window.read(timeout=1000)
        if event in (None, 'Exit'):
            break
        elif event == 'Run':
            window['Run'].update(disabled=True)
            settings.password = values['password']
            settings.username_email = values['username_email']
            settings.friend_name = values['friend_name']
            settings.source = values['source']
            settings.delay = values['delay']

            # Calls the long_operation_thread
            try:
                threading.Thread(target=long_operation_thread,
                                 args=(), daemon=True).start()
            except Exception as e:
                print('Error')

        # Checks for incoming messages from threads
        try:
            message = gui_queue.get_nowait()
        except queue.Empty:
            message = None
        if message:
            print('Got a message back from the thread: ', message)

    window.close()

if __name__ == '__main__':
    the_gui()
    print('Exiting Program')
