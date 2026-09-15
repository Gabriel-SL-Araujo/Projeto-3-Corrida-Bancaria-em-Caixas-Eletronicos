import threading
import time
import random

NUM_ITERS = 10000
semaforo = threading.Semaphore(1)

saldo_global = 1000.0
historico_transacoes = []
valores = [5, 10, 20, 50, 100]

def atm():
    print("Iniciando as operações!")
    global saldo_global
    operacoes = [saque, deposito]
    
    for _ in range(NUM_ITERS):
        semaforo.acquire()
        
        try:
            saldo_temporario = saldo_global
            time.sleep(random.uniform(0.1, 1.0))
            
            operacao = operacoes[random.randint(0, 1)]
            valor = valores[random.randint(0, 4)]
            
            saldo_global = operacao(saldo_temporario, valor)
        finally:
            semaforo.release()

def saque(saldo_temporario, valor):
    saldo_temporario -= valor
    historico_transacoes.append(-valor)
    
    return saldo_temporario

def deposito(saldo_temporario, valor):
    saldo_temporario += valor
    historico_transacoes.append(valor)
    
    return saldo_temporario
    
    
if __name__ == "__main__":
    threads = []
    
    for _ in range(2):
        thread = threading.Thread(target=atm)
        threads.append(thread)
        thread.start()
        
    for thread in threads:
        thread.join()
    
    saldo_inicial = 1000.0
    soma_historico = sum(historico_transacoes)
    saldo_esperado = saldo_inicial + soma_historico
    
    print()
    print(f"Saldo Inicial: ${saldo_inicial:.2f}")
    print(f"Soma do Histórico de Transações: ${soma_historico:.2f}")
    print(f"Saldo Esperado: ${saldo_esperado:.2f}")
    print(f"Saldo atual: ${saldo_global:.2f}")