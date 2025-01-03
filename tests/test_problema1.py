import unittest
from pathlib import Path
import os
from datetime import datetime, timedelta
from src.problema1 import cria_volume_temporario, informa_dados_arquivo, copia_ou_remove, cria_volume_final

class TestProblema1(unittest.TestCase):
    # Criando base para os testes
    def setUp(self):
        # Definindo os diretórios
        self.temp_dir = Path("/home")/"valcann"
        self.temp_dir_origem = self.temp_dir/"backupsFrom"
        self.temp_dir_destino = self.temp_dir/"backupsTo"

        # Criando os diretórios caso não existam
        self.temp_dir_origem.mkdir(parents=True, exist_ok=True)
        self.temp_dir_destino.mkdir(parents=True, exist_ok=True)
        
        # Criando arquivos para teste
        self.arquivo1 = self.temp_dir_origem/"arquivo1.txt"
        self.arquivo1.write_text("conteudo arquivo1")

        self.arquivo2 = self.temp_dir_origem/"arquivo2.txt"
        self.arquivo2.write_text("conteudo arquivo2")

        # Data atual para testes que usam dados de tempo de existência
        self.tempo_atual = datetime.now()
        

    def tearDown(self):
        def limpar_diretorio(diretorio):
            if diretorio.exists():
                for arquivo in diretorio.iterdir():
                    if arquivo.is_file():
                        arquivo.unlink()
        
        limpar_diretorio(self.temp_dir)
        limpar_diretorio(self.temp_dir_origem)
        limpar_diretorio(self.temp_dir_destino)


    def test_cria_volume_temporario(self):
        cria_volume_temporario((self.temp_dir/"backupsFrom.log"), self.temp_dir_origem, self.temp_dir_destino)
        self.assertTrue((self.temp_dir/"backupsFrom.log").exists())


    def test_cria_volume_final(self):
        cria_volume_final((self.temp_dir/"backupsTo.log"), self.temp_dir_destino)
        self.assertTrue((self.temp_dir/"backupsTo.log").exists())


    def test_informa_dados_arquivo(self):
        self.arquivo3 = self.temp_dir_origem/"arquivo3.txt"
        self.arquivo3.write_text("conteudo arquivo3")

        nome, tamanho, data_criacao, data_mod = informa_dados_arquivo(self.arquivo3)
        self.assertEqual(nome, "arquivo3.txt")
        self.assertEqual(tamanho, 17)
        self.assertTrue(data_criacao)
        self.assertTrue(data_mod)


    
    def test_copia_ou_remove(self):
        copia_ou_remove(self.arquivo1, self.tempo_atual - timedelta(days=1), self.temp_dir_destino)
        copia_ou_remove(self.arquivo2, self.tempo_atual - timedelta(days=4), self.temp_dir_destino)
        self.assertTrue(self.arquivo1.exists())
        self.assertFalse(self.arquivo2.exists())
    

if __name__ == '__main__':
    unittest.main()