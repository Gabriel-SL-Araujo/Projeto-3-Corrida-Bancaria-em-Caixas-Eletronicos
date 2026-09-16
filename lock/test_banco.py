import threading

# Importando as classes e funções do nosso arquivo principal (banco.py)
from banco import ContaBancaria, simulador_cliente

def test_fiscalizacao_transacoes_concorrentes():
    """
    Cenário de teste para garantir que o Lock previne Race Conditions.
    """
    saldo_inicial = 1000.0
    conta = ContaBancaria(saldo_inicial)
    
    threads = []
    num_clientes = 5
    operacoes_por_cliente = 10
    total_operacoes_esperadas = num_clientes * operacoes_por_cliente

    
    # Disparando as threads dos clientes simultaneamente
    for i in range(num_clientes):
        t = threading.Thread(target=simulador_cliente, args=(conta, f"Test-Cliente-{i+1}", operacoes_por_cliente))
        threads.append(t)
        t.start()
        
    # Aguardando todos os clientes terminarem
    for t in threads:
        t.join()

    print("\n--- INICIANDO AUDITORIA (FISCALIZAÇÃO) ---")
    
    # Recalculando o saldo do zero baseado exclusivamente no histórico
    saldo_esperado = saldo_inicial
    total_depositos = 0
    total_saques = 0
    
    for t in conta.historico:
        if t["status"] == "APROVADO":
            if t["tipo"] == "DEPOSITO":
                saldo_esperado += t["valor"]
                total_depositos += t["valor"]
            elif t["tipo"] == "SAQUE":
                saldo_esperado -= t["valor"]
                total_saques -= t["valor"]
                
        # Arredondamento necessário para evitar falhas de ponto flutuante no Python
        saldo_esperado = round(saldo_esperado, 2)

    # Relatório final
    print(f"Saldo Inicial....: R$ {saldo_inicial:7.2f}")
    print(f"Total Depositado.: R$ {total_depositos:7.2f}")
    print(f"Total Sacado.....: R$ {total_saques:7.2f}")
    print("-" * 35)
    print(f"Saldo Global.....: R$ {conta.saldo:7.2f}")
    print(f"Saldo Esperado...: R$ {saldo_esperado:7.2f}")
    
    # 1. Verifica se nenhuma transação se perdeu no limbo
    assert len(conta.historico) == total_operacoes_esperadas, "Erro: O número de transações no histórico não bate com as requisições."
    
    # 2. Verifica se a matemática bate
    assert round(conta.saldo, 2) == saldo_esperado, "Erro Crítico: Condição de Corrida detectada! O saldo global divergiu da matemática do extrato."