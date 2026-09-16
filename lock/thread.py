import threading
import time

class ContaBancaria:
    def __init__(self, saldo_inicial):
        self.saldo = saldo_inicial
        self.lock = threading.Lock()

    def sacar(self, valor, nome_cliente):
        print(f"[{nome_cliente}] Solicitando saque de R$ {valor}...")

        with self.lock:
            print(f"[{nome_cliente}] Acessando a conta. Saldo disponível: R$ {self.saldo}")

            if self.saldo >= valor:
                time.sleep(0.1)

                self.saldo -= valor
                print(f"[{nome_cliente}] Saque de R$ {valor} APROVADO! Saldo restante: R$ {self.saldo}")
            else:
                print(f"[{nome_cliente}] Saque de R$ {valor} RECUSADO. Saldo insuficiente.")

conta = ContaBancaria(saldo_inicial=100)

thread1 = threading.Thread(target=conta.sacar, args=(50, "Cliente A "))
thread2 = threading.Thread(target=conta.sacar, args=(80, "Cliente B "))

thread1.start()
thread2.start()

thread1.join()
thread2.join()