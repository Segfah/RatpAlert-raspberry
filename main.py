import requests
import time
from pynput import keyboard

# Variable global para el estado del botón
si_button_is_on = False

def play_alert_sound(bus_time):
    if bus_time == '5':
        print("¡Suena piiiiii!")
        global si_button_is_on
        si_button_is_on = False

def on_key_release(key):
    global si_button_is_on
    if key == keyboard.KeyCode.from_char('o'):
        si_button_is_on = True

# Poner que si falta menos de 4 minutops, una advertencia o simbolo de correr
def display_bus_times(bus_times):
    if len(bus_times) == 1:
        print("Último bus:")
        print(bus_times[0])
    else:
        if bus_times[0] == '0':
            print("Corre")
        else:
            print(bus_times[0])
        print(bus_times[1])

def main():
    listener = keyboard.Listener(on_release=on_key_release)
    listener.start()
    
    while True:
        api_url = "" # bus#numero
        
        
        try:
            response = requests.get(api_url)
            response.raise_for_status()

            data = response.json()
            bus_times = []

            for item in data['nextDepartures']['data']:
                if item['lineDirection'] == 'Gare de Lyon':
                    bus_times.append(item['time'])

            display_bus_times(bus_times)
            
            if si_button_is_on:
                play_alert_sound(bus_times[0])
                
        except requests.exceptions.RequestException as e:
            print("Error al llamar a la API:", e)
        
        time.sleep(60)

if __name__ == "__main__":
    main()