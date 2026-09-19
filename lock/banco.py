import threading
import time
import random

class ContaBancaria:
    def __init__(self, saldo_inicial):
        self.saldo = saldo_inicial
        self.lock = threading.Lock()  # Trava de segurança
        self.historico = []           # Extrato para fiscalização

    def depositar(self, valor, nome_cliente):
        # Bloqueio Exclusivo: Garante que leitura e escrita não sejam sobrepostas
        with self.lock:
            saldo_anterior = self.saldo
            self.saldo += valor
            
            # Registra o estado exato no momento da transação
            self.historico.append({
                "tipo": "DEPOSITO",
                "cliente": nome_cliente,
                "valor": valor,
                "saldo_anterior": saldo_anterior,
                "saldo_atual": self.saldo,
                "status": "APROVADO"
            })
            print(f"[{nome_cliente}] \033[92m+ DEPÓSITO\033[0m de R$ {valor:6.2f} | Saldo Global: R$ {self.saldo:7.2f}")

    def sacar(self, valor, nome_cliente):
        with self.lock:
            saldo_anterior = self.saldo
            
            if self.saldo >= valor:
                time.sleep(0.001)  # Simula latência de rede
                self.saldo -= valor
                
                self.historico.append({
                    "tipo": "SAQUE",
                    "cliente": nome_cliente,
                    "valor": valor,
                    "saldo_anterior": saldo_anterior,
                    "saldo_atual": self.saldo,
                    "status": "APROVADO"
                })
                print(f"[{nome_cliente}] \033[91m- SAQUE\033[0m    de R$ {valor:6.2f} | Saldo Global: R$ {self.saldo:7.2f}")
            else:
                self.historico.append({
                    "tipo": "SAQUE",
                    "cliente": nome_cliente,
                    "valor": valor,
                    "saldo_anterior": saldo_anterior,
                    "saldo_atual": self.saldo,
                    "status": "RECUSADO"
                })
                print(f"[{nome_cliente}] \033[93mx RECUSADO\033[0m (R$ {valor:6.2f}) | Saldo Global: R$ {self.saldo:7.2f} - (Saldo Insuficiente)")


def simulador_cliente(conta, nome_cliente, qtd_operacoes):
    """
    Simula o comportamento de um cliente fazendo operações aleatórias.
    """
    for _ in range(qtd_operacoes):
        # 1º Random: Escolhe a operação (0 = Depósito, 1 = Saque)
        operacao = random.randint(0, 1)
        
        # 2º Random: Define um valor monetário realista (entre R$ 10.00 e R$ 200.00)
        valor = round(random.uniform(10.0, 200.0), 2)
        
        if operacao == 0:
            conta.depositar(valor, nome_cliente)
        else:
            conta.sacar(valor, nome_cliente)
            
        # Simula o tempo que o usuário leva antes de fazer a próxima operação
        time.sleep(random.uniform(0.01, 0.05))

if __name__ == "__main__":
    saldo_inicial_main = 1000.0
    conta_main = ContaBancaria(saldo_inicial_main)
    
    threads_main = []
    
    print("Iniciando aplicação bancária (Modo Normal)...")
    
    # Criando 3 clientes aleatórios
    for i in range(3):
        t = threading.Thread(target=simulador_cliente, args=(conta_main, f"Cliente_{i+1}", 10))
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
    
    print("\n" + "=" * 65)
    print("PROVA MATEMÁTICA DE CONSERVAÇÃO DE CAPITAL (COM LOCK)")
    print("=" * 65)
    print(f"Saldo Inicial da Conta:   R$ {saldo_inicial_main:.2f}")
    print(f"Soma Total Depositada:    + R$ {total_depositos:.2f}")
    print(f"Soma Total Sacada:        - R$ {total_saques:.2f}")
    print("-" * 65)
    print(f"SALDO ESPERADO (Ideal):   \033[94mR$ {saldo_esperado:.2f}\033[0m")
    print(f"SALDO FINAL:        \033[94mR$ {conta_main.saldo:.2f}\033[0m")
    print("=" * 65)
    
    if diferenca == 0:
        print("\033[92m[VEREDITO] Capital conservado de forma invariável. Diferença: R$ 0.00\033[0m")
        print("O Semáforo (Lock) garantiu a integridade absoluta da memória.")
    else:
        print(f"\033[91m[FALHA] Divergência detectada: R$ {diferenca:.2f}\033[0m")
        
    print("Aplicação bancária finalizada.")