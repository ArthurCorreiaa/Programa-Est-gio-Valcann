# Parto de uma suposição: Os diretórios existem. Caso eu precise levar em consideração que eles possam não
# ter sido criados ainda, preciso fazer uma adaptação de verificação de existência e de criação dos diretórios
# para não ter erros.

# Formatação do arquivo de saída: Atualmente tem pipes dividindo entre um dado e outro, mas dependendo de seus
# tamanhos os espaçamentos serão diferentes e nada padronizados. Para uso em alguns scipts seria possível
# ser feito o uso sem demais complicações, até mesmo sem o uso dos pipes, porém seriam arquivos de baixa 
# legibilidade. É possível fazer formatação desses arquivos para que saiam de uma forma mais adequada
# para serem apenas abertos e lidos.

# Sempre que rodo gradle-test no tst de eda existe um retorno visual no terminal
# de que o que os testes foram executados e se passei ou não. Queria saber se devo dar algum retorno para
# o usuário de que o programa terminou sua execução ou algo do tipo.

# Analisar possibildiade de adicionar um try-catch para garantir tratamento de erros
    

import shutil
from pathlib import Path
from datetime import datetime, timedelta

# Caminho por onde puxaremos os dados
diretorio_origem = Path("/home/valcann/backupsFrom") 
# Caminho do arquivo onde serão salvos os dados de entrada
log_backup_from = Path("/home/valcann/backupsFrom.log") 
# Caminho para para onde seré enviada a listagem de dados
diretorio_destino = Path("/home/valcann/backupsTo") 
# Caminho do arquivo onde será salvo o resultado final
log_backup_to = Path("/home/valcann/backupsTo.log")


# Retorna informações dos arquivos
def informa_dados_arquivo(arquivo): 
    # Nome do arquivo (sem extensão do tipo de arquivo)
    nome = arquivo.name
    # Tamanho do arquivo em bytes 
    tamanho = arquivo.stat().st_size 

    # Data de criação do arquivo
    data_criacao = datetime.fromtimestamp(arquivo.stat().st_ctime)
    # data_criacao = datetime.fromtimestamp(arquivo.stat().st_birthtime) <<< CONFERIR QUAL DOS 2 USAR!!!
    # Enquanto st_birthtime mostra sua data de criação, não funciona em sistema linux,
    # st_ctime mostra a última alteração nos metadados (como nome e permissões do arquivo)

    # Data da última modificação        
    data_modificacao = datetime.fromtimestamp(arquivo.stat().st_mtime)
    
    # Retorna as informações obtidas acima com a data formatada para dd/mm/yyyy HH:MM:SS
    return nome, tamanho, data_criacao.strftime("%d/%m/%Y %H:%M:%S"), data_modificacao.strftime("%d/%m/%Y %H:%M:%S")

# Cria o cabeçalho dos logs
def cria_cabecalho():
    return "nome                | tamanho    | data de criação      | data de última modificação \n" + 80 * "-" + "\n"

# Abrindo e editando (ou criando caso não exista ainda) o arquivo de log de backupsFroms
with open(log_backup_from, "w")  as log_origem:
    # Cria um cabeçalho no arquivo log_backup_from
    log_origem.write(cria_cabecalho())
    # Itera por cada elemento no diretório
    for arquivo in diretorio_origem.iterdir():
        # Confere se o elemento analisado é um arquivo e salva seus dados apenas se a condição for verdadeira
        if arquivo.is_file():
            # nome = arquivo.name
            # tamanho = arquivo.stat().st_size
            # data_criacao = datetime.fromtimestamp(arquivo.stat().st_birthtime)/st_ctime   
            # data_modificacao = datetime.fromtimestamp(arquivo.stat().st_mtime)
            nome, tamanho, data_criacao, data_modificacao = informa_dados_arquivo(arquivo)
            # Adiciona os dados de maneira formatada ao log
            log_origem.write(f"{nome:< 20} | {tamanho:> 10} | {data_criacao:> 20} | {data_modificacao:> 28}\n")


        # Verifica o tempo de existência do arquivo. Se for maior que 3 dias (completos), será excluído, caso contrário, será copiado para backupsTo
        diferenca_tempo = datetime.now() - data_criacao
        if (diferenca_tempo > timedelta(days=3)):
            arquivo.unlink()
        else:
            # Veifica se o diretório para onde estão sendo enviados os arquivos e seus diretórios pai existem
            diretorio_destino.mkdir(parents=True, exist_ok=True)
            shutil.copy(arquivo, diretorio_destino)

# Abrindo e editando (ou criando caso não exista ainda) o arquivo de log de backupsTo
with open(log_backup_to, "w") as log_to:    
    # Cria um cabeçlho no arquivo log_backup_to
    log_to.write(cria_cabecalho())
    # Itera por cada elemento no diretório
    for arquivo in diretorio_destino.iterdir():
        # Confere se o elemento analisado é um arquivo e salva seus dados apenas se a condição for verdadeira
        if arquivo.is_file():
            nome, tamanho, data_criacao, data_modificacao = informa_dados_arquivo(arquivo)
            # Adiciona os dados de maneira formatada ao log 
            log_to.write(f"{nome:< 20} | {tamanho:> 10} | {data_criacao:> 20} | {data_modificacao:> 28}\n")
