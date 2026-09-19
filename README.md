# Projeto 3 – Corrida Bancária em Caixas Eletrônicos

Projeto desenvolvido para a disciplina de **Programação Paralela e Distribuída (UNICAP)** com o objetivo de demonstrar problemas de concorrência em sistemas financeiros e mecanismos de sincronização utilizados para preservar a integridade dos dados.

## Objetivo

Simular um cenário bancário no qual múltiplas operações acessam uma mesma conta compartilhada, permitindo observar os impactos da concorrência sobre o saldo e a consistência das transações.

## Estrutura do Projeto

### Lock

Implementação utilizando `Lock` para proteger a região crítica responsável pelo acesso e alteração do saldo da conta compartilhada.

### Mutex

Demonstração comparativa entre um cenário sem proteção e um cenário protegido por `Mutex`, evidenciando os efeitos da sincronização sobre a consistência dos dados.

### Semáforo

Implementação utilizando `Semaphore` para sincronizar eventos entre threads e coordenar a execução de operações concorrentes.

## Conceitos Abordados

* Concorrência
* Threads
* Condição de Corrida
* Exclusão Mútua
* Integridade Transacional
* Mutex
* Lock
* Semáforos

## Integrantes

* Arthur Filipe
* Gabriel Araújo
* Gregório de Albuquerque
* Noemi Soares
* Ricardo Nery
