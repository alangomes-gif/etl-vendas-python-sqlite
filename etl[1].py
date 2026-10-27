import csv
import sqlite3
from decimal import Decimal, InvalidOperation
from pathlib import Path


def processar(entrada, banco):
    """Valida vendas CSV e gera um resumo SQLite em uma transação."""
    registros = []
    ids = set()
    with Path(entrada).open(encoding='utf-8-sig', newline='') as arquivo:
        leitor = csv.DictReader(arquivo)
        if not {'id', 'produto', 'quantidade', 'preco'}.issubset(leitor.fieldnames or []):
            raise ValueError('Colunas necessárias: id,produto,quantidade,preco')
        for linha, venda in enumerate(leitor, 2):
            try:
                identificador = venda['id'].strip()
                produto = venda['produto'].strip()
                quantidade = int(venda['quantidade'])
                preco = Decimal(venda['preco'].replace(',', '.'))
                if not preco.is_finite() or preco < 0 or quantidade <= 0 or not produto or not identificador:
                    raise ValueError()
                if preco.as_tuple().exponent < -2:
                    raise ValueError()
                if identificador in ids:
                    raise ValueError('ID duplicado')
                ids.add(identificador)
                registros.append((identificador, produto, quantidade, int(preco * 100)))
            except (ValueError, InvalidOperation, AttributeError):
                raise ValueError(f'Venda inválida na linha {linha}') from None
    conexao = sqlite3.connect(banco)
    try:
        with conexao:
            conexao.execute('CREATE TABLE IF NOT EXISTS vendas(id TEXT PRIMARY KEY, produto TEXT, quantidade INTEGER, preco_centavos INTEGER)')
            conexao.executemany('INSERT INTO vendas VALUES(?,?,?,?) ON CONFLICT(id) DO UPDATE SET produto=excluded.produto, quantidade=excluded.quantidade, preco_centavos=excluded.preco_centavos', registros)
        return conexao.execute('SELECT produto, SUM(quantidade), SUM(quantidade*preco_centavos) FROM vendas GROUP BY produto ORDER BY produto').fetchall()
    finally:
        conexao.close()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='ETL demonstrativo de vendas CSV para SQLite')
    parser.add_argument('csv')
    parser.add_argument('--banco', default='vendas.sqlite')
    argumentos = parser.parse_args()
    for produto, unidades, centavos in processar(argumentos.csv, argumentos.banco):
        print(f'{produto}: {unidades} unidades, R$ {Decimal(centavos)/100:.2f}')
