import tempfile
import unittest
from pathlib import Path
from etl import processar

class TestETL(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent)
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
    def executar(self, texto):
        caminho = self.base/'entrada.csv'
        caminho.write_text(texto, encoding='utf-8')
        return processar(caminho, self.base/'teste.sqlite')
    def test_dinheiro_exato_e_reexecucao(self):
        texto = 'id,produto,quantidade,preco\n1,Mouse,3,0.10\n2,Mouse,1,0.20\n'
        self.assertEqual(self.executar(texto), [('Mouse', 4, 50)])
        self.assertEqual(self.executar(texto), [('Mouse', 4, 50)])
    def test_arquivo_invalido_nao_grava_parcialmente(self):
        self.executar('id,produto,quantidade,preco\n1,Mouse,1,10\n')
        with self.assertRaises(ValueError):
            self.executar('id,produto,quantidade,preco\n2,Teclado,1,15\n3,Mouse,-1,9\n')
        self.assertEqual(self.executar('id,produto,quantidade,preco\n'), [('Mouse', 1, 1000)])
    def test_rejeita_duplicatas_e_precos_invalidos(self):
        for linhas in ['1,A,1,1\n1,B,1,2\n', '1,A,1,NaN\n', '1,A,1,0.001\n']:
            with self.subTest(linhas=linhas), self.assertRaises(ValueError):
                self.executar('id,produto,quantidade,preco\n'+linhas)

if __name__=='__main__': unittest.main()
