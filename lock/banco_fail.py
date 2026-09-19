import threading
import time
import random

class ContaBancaria:
    def __init__(self, saldo_inicial):
        self.saldo = saldo_inicial
        # O Lock foi removido. A memória está desprotegida.
        self.historico = []

    def depositar(self, valor, nome_cliente):
        saldo_lido = self.saldo
        
        time.sleep(0.001) 
        
        self.saldo = saldo_lido + valor
        
        self.historico.append({
            "tipo": "DEPOSITO",
            "cliente": nome_cliente,
            "valor": valor,
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
                "status": "APROVADO"
            })
            print(f"[{nome_cliente}] \033[91m- SAQUE\033[0m    de R$ {valor:6.2f} | Saldo Global: R$ {self.saldo:7.2f}")
        else:
            self.historico.append({
                "tipo": "SAQUE",
                "cliente": nome_cliente,
                "valor": valor,
                "status": "RECUSADO"
            })
            print(f"[{nome_cliente}] \033[93mx RECUSADO\033[0m (R$ {valor:6.2f}) | Saldo Global: R$ {self.saldo:7.2f} (Insuficiente)")


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
        t = threading.Thread(target=simulador_cliente, args=(conta_main, f"Cliente_{i+1}", 20))
        threads_main.append(t)
        t.start()
        
    for t in threads_main:
        t.join()
        
    saldo_esperado = saldo_inicial_main
    total_depositos = 0.0
    total_saques = 0.0
    
    for transacao in conta_main.historico:
        if transacao["status"] == "APROVADO":
            if transacao["tipo"] == "DEPOSITO":
                saldo_esperado += transacao["valor"]
                total_depositos += transacao["valor"]
            elif transacao["tipo"] == "SAQUE":
                saldo_esperado -= transacao["valor"]
                total_saques += transacao["valor"]

    diferenca = abs(saldo_esperado - conta_main.saldo)
    
    print("\n" + "=" * 60)
    print("RELATÓRIO DE AUDITORIA FINAL (VULNERABILIDADE DETECTADA)")
    print("=" * 60)
    print(f"Saldo Inicial da Conta:   R$ {saldo_inicial_main:.2f}")
    print(f"Soma Total Depositada:  + R$ {total_depositos:.2f}")
    print(f"Soma Total Sacada:      - R$ {total_saques:.2f}")
    print("-" * 60)
    print(f"SALDO ESPERADO (Ideal):   \033[94mR$ {saldo_esperado:.2f}\033[0m")
    print(f"SALDO INCONSISTENTE:   \033[91mR$ {conta_main.saldo:.2f}\033[0m")
    print("=" * 60)
    print(f"DIVERGÊNCIA FINANCEIRA:   \033[93mR$ {diferenca:.2f}\033[0m")
    print("CAUSA: Condição de Corrida (Race Condition). Ausência de semáforo na região crítica.")