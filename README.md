# ETL de vendas - projeto de portfólio

Projeto demonstrativo criado com auxílio de IA no Codex. Não representa entrega a cliente ou experiência em uma empresa. Os dados de exemplo são fictícios.

Executar com Python 3.10 ou superior (biblioteca padrão):

    python etl.py exemplo.csv --banco vendas.sqlite
    python -m unittest -v

O programa valida todas as linhas antes da gravação, rejeita IDs repetidos no mesmo CSV, usa Decimal na leitura de preços e armazena dinheiro em centavos inteiros. Reexecutar a importação atualiza IDs existentes, evitando somar a mesma venda duas vezes. O resumo considera todo o banco acumulado; importar um arquivo novo não apaga vendas anteriores.

Limites: demonstração local, sem autenticação, importação completa em memória e apenas uma moeda. Não é um sistema fiscal ou financeiro de produção.
