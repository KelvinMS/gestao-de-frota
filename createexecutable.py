import subprocess

commandBase1 = 'pyisntaller  --onefile --noconsole --windowed main.py'
def executar_comando(comando):
    try:
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
        print("Saída:")
        print(resultado.stdout)
        print("Erro:")
        print(resultado.stderr)
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    #comando = input("Digite o nome do arquivo: ")
    #comando = commandBase1+ comando
    #print('Comando para executar: ',comando)
    executar_comando(commandBase1)