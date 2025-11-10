#!/usr/bin/env python3
"""
Script para drone autônomo com Raspberry Pi + Pixhawk
Realiza: armar -> voar por 10 segundos -> pousar -> desarmar
"""

import time
import dronekit
from dronekit import connect, VehicleMode, LocationGlobalRelative

# Configurações de conexão
CONNECTION_STRING = "/dev/ttyACM0"  # ou "/dev/ttyAMA0" para serial GPIO
BAUDRATE = 57600

def connect_drone():
    """Conecta ao veículo"""
    print("Conectando ao veículo...")
    vehicle = connect(CONNECTION_STRING, baud=BAUDRATE, wait_ready=True)
    print(f"Conectado ao veículo: {vehicle.version}")
    return vehicle

def arm_and_takeoff(vehicle, target_altitude=5):
    """
    Arma o drone e decola para a altitude especificada
    """
    print("Verificando pré-condições para decolagem...")
    
    # Aguarda o GPS ficar pronto
    while not vehicle.is_armable:
        print("Aguardando veículo se tornar armável...")
        time.sleep(1)
    
    # Define modo GUIDED
    vehicle.mode = VehicleMode("GUIDED")
    time.sleep(2)
    
    # Arma o drone
    print("Armando motores...")
    vehicle.armed = True
    
    # Aguarda armar
    while not vehicle.armed:
        print("Aguardando armar...")
        time.sleep(1)
    
    print("Motores armados!")
    
    # Decola
    print(f"Decolando para {target_altitude} metros...")
    vehicle.simple_takeoff(target_altitude)
    
    # Aguarda atingir altitude
    while True:
        current_altitude = vehicle.location.global_relative_frame.alt
        if current_altitude >= target_altitude * 0.95:
            print(f"Altitude atingida: {current_altitude:.2f} metros")
            break
        time.sleep(1)

def fly_mission(vehicle, flight_time=10):
    """
    Mantém o drone voando por um tempo específico
    """
    print(f"Voando por {flight_time} segundos...")
    
    start_time = time.time()
    
    while time.time() - start_time < flight_time:
        remaining = flight_time - (time.time() - start_time)
        print(f"Tempo restante: {remaining:.1f} segundos")
        
        # Verifica status do veículo
        altitude = vehicle.location.global_relative_frame.alt
        battery = vehicle.battery
        print(f"Altitude: {altitude:.2f}m | Battery: {battery.voltage if battery else 'N/A'}V")
        
        time.sleep(1)
    
    print("Tempo de voo concluído!")

def land_and_disarm(vehicle):
    """
    Pousa o drone e desarma
    """
    print("Iniciando procedimento de pouso...")
    
    # Define modo LAND
    vehicle.mode = VehicleMode("LAND")
    
    # Aguarda pouso (altitude próxima de zero)
    while vehicle.location.global_relative_frame.alt > 0.5:
        print(f"Descendo... Altitude: {vehicle.location.global_relative_frame.alt:.2f}m")
        time.sleep(1)
    
    print("Drone pousado!")
    
    # Aguarda um pouco antes de desarmar
    time.sleep(2)
    
    # Desarma o drone
    print("Desarmando motores...")
    vehicle.armed = False
    
    # Aguarda desarmar
    while vehicle.armed:
        print("Aguardando desarmar...")
        time.sleep(1)
    
    print("Motores desarmados!")

def main():
    """Função principal"""
    vehicle = None
    
    try:
        # Conecta ao drone
        vehicle = connect_drone()
        
        # Executa a missão
        arm_and_takeoff(vehicle, target_altitude=5)
        fly_mission(vehicle, flight_time=10)
        land_and_disarm(vehicle)
        
        print("Missão concluída com sucesso!")
        
    except KeyboardInterrupt:
        print("Missão interrompida pelo usuário!")
        
    except Exception as e:
        print(f"Erro durante a missão: {e}")
        
    finally:
        # Fecha a conexão
        if vehicle:
            print("Fechando conexão...")
            vehicle.close()
        
        print("Programa finalizado.")

if __name__ == "__main__":
    main()