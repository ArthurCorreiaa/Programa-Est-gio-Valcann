import logging
from shutil import copy
from pathlib import Path
from datetime import datetime, timedelta


# Definindo as propriedades do log de execução
logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="log_de_execucao.txt", 
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s: %(message)s",
    datefmt="%d/%m/%Y | %H:%M:%S",
    encoding="utf-8"
    )


# Caminho por onde puxaremos os dados
diretorio_origem = Path("/home")/"valcann"/"backupsFrom" 
# Caminho do arquivo onde serão salvos os dados de entrada
log_backup_from = Path("/home")/"valcann"/"backupsFrom.log" 
# Caminho para para onde seré enviada a listagem de dados
diretorio_destino = Path("/home")/"valcann"/"backupsTo" 
# Caminho do arquivo onde será salvo o resultado final
log_backup_to = Path("/home")/"valcann"/"backupsTo.log"


# Cria o cabeçalho dos logs
def cria_cabecalho():
    return "nome                | tamanho    | data de criação      | data de última modificação \n" + 80 * "-" + "\n"


# Retorna informações dos arquivos
def informa_dados_arquivo(arquivo): 
    # Nome do arquivo (sem extensão do tipo de arquivo)
    nome = arquivo.name
    # Tamanho do arquivo em bytes 
    tamanho = arquivo.stat().st_size 
    # Data de criação do arquivo
    data_criacao = datetime.fromtimestamp(arquivo.stat().st_ctime)
    # Data da última modificação        
    data_modificacao = datetime.fromtimestamp(arquivo.stat().st_mtime)
    
    # Retorna as informações obtidas acima 
    return nome, tamanho, data_criacao, data_modificacao


# Verifica o tempo de existência do arquivo. Se for maior que 3 dias (completos), será excluído, caso contrário, será copiado para backupsTo
def copia_ou_remove(arquivo, tempo, diretorio_destino):
    if (datetime.now() - tempo) > timedelta(days=3):
        logging.info("Deletando o arquivo: %s.", arquivo)
        arquivo.unlink()
    else:
        logging.info("Copiando %s para %s.", arquivo, diretorio_destino)
        copy(arquivo, diretorio_destino)


# Abrindo e editando (ou criando caso ainda não exista) o arquivo de log de backupsFroms
def cria_volume_temporario(log_from, diretorio_origem, diretorio_destino):
    logging.info("Criando volume temporário.")
    # Veifica se o diretório para onde estão sendo enviados os arquivos e seus diretórios pai existem
    diretorio_destino.mkdir(parents=True, exist_ok=True)
    with open(log_from, "w") as log:
        # Cria um cabeçalho no arquivo log_backup_from
        log.write(cria_cabecalho())
        # Itera por cada elemento no diretório
        for arquivo in diretorio_origem.iterdir():
            # Confere se o elemento analisado é um arquivo e salva seus dados apenas se a condição for verdadeira
            if arquivo.is_file():
                nome, tamanho, data_criacao, data_modificacao = informa_dados_arquivo(arquivo)
                # Adiciona os dados de maneira formatada ao log
                logging.info("Salvando os dados do arquivo %s em %s.", nome, log_from)
                log.write(f"{nome:<20} | {tamanho:>10} | {data_criacao.strftime("%d/%m/%Y %H:%M:%S"):>20} | {data_modificacao.strftime("%d/%m/%Y %H:%M:%S"):>28}\n")

            diferenca_tempo = datetime.now() - data_criacao
            logging.info("Tempo de existência de %s: %s", nome, diferenca_tempo)
            copia_ou_remove(arquivo, data_criacao, diretorio_destino)


#Abrindo e editando (ou criando caso ainda não exista) o log de backupsTo
def cria_volume_final(log_to, diretorio):
    logging.info("Criando volume final.")
    # Abrindo e editando (ou criando caso não exista ainda) o arquivo de log de backupsTo
    with open(log_to, "w") as log:    
        # Cria um cabeçalho no arquivo log_backup_to
        log.write(cria_cabecalho())
        # Itera por cada elemento no diretório
        for arquivo in diretorio.iterdir():
            # Confere se o elemento analisado é um arquivo e salva seus dados apenas se a condição for verdadeira
            if arquivo.is_file():
                nome, tamanho, data_criacao, data_modificacao = informa_dados_arquivo(arquivo)
                # Adiciona os dados de maneira formatada ao log 
                logging.info("Salvando os dados do arquivo %s em %s.", nome, log_to)
                log.write(f"{nome:<20} | {tamanho:>10} | {data_criacao.strftime("%d/%m/%Y %H:%M:%S"):>20} | {data_modificacao.strftime("%d/%m/%Y %H:%M:%S"):>28}\n")

def main():
    try:
        cria_volume_temporario(log_backup_from, diretorio_origem, diretorio_destino)
        cria_volume_final(log_backup_to, diretorio_destino)
        logging.info("Execução do programa concluída.")
        print("Execução do programa concluída.")
    except Exception as erro:
        logging.error("Ocorreu um erro: %s", erro)
        print(f"Ocorreu um erro: {erro}.")


if __name__ == "__main__":
    main()
    