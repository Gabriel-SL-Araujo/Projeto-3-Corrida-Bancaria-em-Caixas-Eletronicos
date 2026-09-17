import threading
import time
import random

class ContaBancaria:
    def __init__(self, saldo_inicial):
        self.saldo = saldo_inicial
        # O Lock removido. A memória está desprotegida
        self.historico = []

    def depositar(self, valor, nome_cliente):
        saldo_lido = self.saldo
        
        time.sleep(0.001) 
        
        self.saldo = saldo_lido + valor
        
        self.historico.append({
            "tipo": "DEPOSITO",
            "cliente": nome_cliente,
            "valor": valor,
            "saldo_anterior": saldo_lido,
            "saldo_atual": self.saldo,
            "status": "APROVADO"
        })
        print(f"[{nome_cliente}] \033[92m+ DEPÓSITO\033[0m de R$ {valor:6.2f} | Saldo Global: R$ {self.saldo:7.2f}")

    def sacar(self, valor, nome_cliente):
        saldo_lido = self.saldo
        
        if saldo_lido >= valor:
            time.sleep(0.001) 
            
            self.saldo = saldo_lido - valor
            
            self.historico.append({
                "tipo": "SAQUE",
                "cliente": nome_cliente,
                "valor": valor,
                "saldo_anterior": saldo_lido,
                "saldo_atual": self.saldo,
                "status": "APROVADO"
            })
            print(f"[{nome_cliente}] \033[91m- SAQUE\033[0m    de R$ {valor:6.2f} | Saldo Global: R$ {self.saldo:7.2f}")
        else:
            self.historico.append({
                "tipo": "SAQUE",
                "cliente": nome_cliente,
                "valor": valor,
                "saldo_anterior": saldo_lido,
                "saldo_atual": self.saldo,
                "status": "RECUSADO"
            })
            print(f"[{nome_cliente}] \033[93mx RECUSADO\033[0m (R$ {valor:6.2f}) | Saldo insuficiente")


def simulador_cliente(conta, nome_cliente, qtd_operacoes):
    for _ in range(qtd_operacoes):
        operacao = random.randint(0, 1)
        valor = round(random.uniform(10.0, 50.0), 2)
        
        if operacao == 0:
            conta.depositar(valor, nome_cliente)
        else:
            conta.sacar(valor, nome_cliente)

if __name__ == "__main__":
    saldo_inicial_main = 1000.0
    conta_main = ContaBancaria(saldo_inicial_main)
    threads_main = []
    
    print("Iniciando aplicação bancária (Modo Corrompido/Sem Lock)...")
    
    for i in range(5):
        t = threading.Thread(target=simulador_cliente, args=(conta_main, f"Cliente_{i+1}", 2))
        threads_main.append(t)
        t.start()
        
    for t in threads_main:
        t.join()
        
    print("-" * 50)
    print("Aplicação bancária finalizada.")
    print(f"Saldo Inicial Esperado: R$ {saldo_inicial_main:.2f}")
    print(f"Saldo Final Calculado:  R$ {conta_main.saldo:.2f}")
    print("O saldo final será matematicamente incompatível com as operações devido à sobrescrita cega de memória.")