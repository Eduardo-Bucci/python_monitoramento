import serial as sr
import time
import platform
import database.banco as banco

sistema = platform.system()

if(sistema == "Windows"):
    porta_sistema = "COM3"
elif(sistema == "Linux"):
    porta_sistema = "/dev/ttyUSB0"

porta:str = porta_sistema
baudrate:int = 9600
timeout:int = 2
arduino = None
ultimo_estado = None

try:
    arduino = sr.Serial(porta, baudrate, timeout=timeout)
    time.sleep(2)

    banco.criarTabela()
         
    if(arduino.is_open):
        print("Conexão com arduíno ta show papai")

    while True:

        if(arduino.in_waiting > 0):
            dadosBrutos = arduino.readline()
            try:
                dados = dadosBrutos.decode("utf-8").rstrip().split(",")
                dados = [int(i) for i in dados]
                print(dados)
                if( len(dados) == 5):
                    if(dados != ultimo_estado):
                        banco.inserirValores(*dados)
                        ultimo_estado = dados

            except ValueError:
                continue
       
        time.sleep(0.3)

except KeyboardInterrupt:
    print("Programa encerrado pelo usuário")

except Exception as e:
    print("Erro na conexão com arduíno\nErro:", e)

finally:
    if(arduino and arduino.is_open):
        arduino.close()
        print("Conexão com arduíno encerrada")
        