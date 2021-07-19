import sys, os, codecs
from colorama import Fore

def imprime(msj, tipo = ''):
    msj = str(msj)
    if tipo == "err":
        simb = f"{Fore.RED}[!] ERROR:\t"
    elif tipo == "inf":
        simb = f"{Fore.CYAN}[+] INFO:\t"
    else:
        simb = f'{Fore.GREEN} >>\t'
    print(simb + msj)

def comprueba_apktool():
    os.system("ls | grep apktool > comprueba")
    linea = open("comprueba","r").readlines()
    if linea:
        imprime("apktool está instalado","inf")
    else:
        imprime("apktool no está instalado, intento instalarlo ... ","err")
        imprime("Descargando APKTOOL ","inf")
        os.system("wget https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.4.1.jar")
    os.system("rm -rf comprueba")

def comprueba_java():
    os.system("which java > comprueba")
    linea = open("comprueba","r").readlines()
    if linea:
        imprime("Java está instalado","inf")
    else:
        imprime("Java no está instalado\n Dame permisos de root y te lo instalo","err")
        os.system("sudo apt update && sudo apt install openjdk-11-jre")
    os.system("rm -rf comprueba")

def comprueba_dex2jar():
    os.system("which d2j-dex2jar > comprueba")
    linea = open("comprueba","r").readlines()
    if linea:
        imprime("dex2jar está instalado","inf")
    else:
        imprime("dex2jar no está instalado\nDame permisos de root y te lo instalo","err")
        os.system("sudo apt update && sudo apt install dex2jar")
    os.system("rm -rf comprueba")

def comprueba_decompilador():
    os.system("which jd-gui > comprueba")
    linea = open("comprueba","r").readlines()
    if linea:
        imprime("jd-gui está instalado","inf")
    else:
        imprime("jd-gui no está instalado\nDame permisos de root y te lo instalo","err")
        os.system("sudo apt update && sudo apt install jd-gui")
    os.system("rm -rf comprueba")

def comprueba_dependencias():
    comprueba_dex2jar()
    comprueba_decompilador()
    comprueba_java()
    comprueba_apktool()


def comprobar_numero_magico(file):   
    valido = False
    magicos_apk = ["504B0304"]    
    with open(file,"rb") as f:
        numero_magico = codecs.decode(codecs.encode(f.read(4),"hex"),"utf-8")
        numero_magico = numero_magico.upper()
        f.close()
    for magico in magicos_apk:
        if magico == numero_magico:
            valido = True
    return valido

def comprobar_archivo(file):
    valido = False
    if os.path.isfile(file):
        valido = comprobar_numero_magico(file)    
    else:
        imprime(f"El archivo {file} no existe.","err")
        exit()
    return valido

def main():
    try:
        apk = sys.argv[1]
        jar = apk.replace(".apk",".jar")
        directorio_salida = jar.replace(".jar","")
        orden_apktool = "java -jar $(pwd)/apktool_2.4.1.jar"
        if comprobar_archivo(apk):
            comprueba_dependencias()
            os.system(f"d2j-dex2jar {apk} -o $(pwd)/{jar}" )
            os.system(f"{orden_apktool} d {apk} -o $(pwd)/{directorio_salida}")
            imprime(f"{apk} decompilado en {directorio_salida}","inf")
            imprime(f"Si desea leer el codigo en Java abre el jar extraido con jd-gui, ¿ Desea abrir la herramienta ?[S/n]","inf")
            r = input(f"{Fore.MAGENTA}>>>>>\t")
            if len(r) == 0 or r[0].upper() == 'S':
                os.system(f"jd-gui {jar} ")
        else:
            imprime("NECESITO UN APK ","err")

    except IndexError:
        imprime("Debe de introducir un archivo APK válido como argumento","err")
        imprime(f"Uso  (python3 {sys.argv[0]} <APK>)","inf")

if __name__ == '__main__':
    main()