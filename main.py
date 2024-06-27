import mido
from pynput.keyboard import Controller, Key

lastcontrolnum = 0

def map_midi_to_keyboard(midi_port):
    global lastcontrolnum
    keyboard = Controller()
    for msg in midi_port:
        if msg.type == 'note_on':
            keyboard.press('f')
        elif msg.type == 'note_off':
            keyboard.release('f')
        if msg.type == 'control_change':
            print(msg.control, msg.value)
            """
            if msg.control >= 70:
                if msg.value < 30:
                    keyboard.press(Key.left)
                elif msg.value > 70:
                    keyboard.press(Key.right)
                else:
                    keyboard.release(Key.left)
                    keyboard.release(Key.right)
            """
            if msg.control >= 70: #akai mpk mini knob
                if msg.value > lastcontrolnum:
                    keyboard.press(Key.right)
                    keyboard.release(Key.left)
                    lastcontrolnum = msg.value
                elif msg.value < lastcontrolnum:
                    keyboard.press(Key.left)
                    keyboard.release(Key.right)
                    lastcontrolnum = msg.value
                elif msg.value == 0:
                    #left
                    keyboard.press(Key.left)
                    keyboard.release(Key.right)
                elif msg.value == 127:
                    #right
                    keyboard.press(Key.right)
                    keyboard.release(Key.left)
                else:
                    keyboard.release(Key.left)
                    keyboard.release(Key.right)
                    
            
            

if __name__ == "__main__":
    print("Available MIDI ports:")
    for i, port_name in enumerate(mido.get_input_names()):
        print(f"{i + 1}: {port_name}")
    print("Enter the MIDI port index: ")
    midi_port_index = int(input())
    try:
        midi_port = mido.open_input(mido.get_input_names()[midi_port_index - 1])
    except OSError:
        print("MIDI port not found. (or already in use) Please check if the port name is correct.")
        exit()
    except Exception as e:
        print(f"An error occurred: {e}")
        exit()
    print("Mapping MIDI keys to 'F' key")

    try:
        map_midi_to_keyboard(midi_port)
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        midi_port.close()
