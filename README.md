# Vimana Framework - Atualizações

## Novos Recursos

Este documento destaca as adições recentes ao Vimana Framework para uma tarefa sobre frameworks, focando em três novos hotspots que expandem significativamente as capacidades do framework.

### 1. API Security Auditor (Plugin Siddhi)
O novo plugin 'API Security Auditor' é uma adição poderosa ao nosso conjunto de ferramentas. Este plugin é projetado para auditar cabeçalhos de segurança em APIs, garantindo a presença de cabeçalhos essenciais como 'Content-Security-Policy' e 'X-Frame-Options'.

#### Uso:
Para usar este plugin, execute:
```
vimana run --plugin api_security_auditor --target http://example.com
```

### 2. Gerador de Relatórios de Auditoria (Script de Automação)
Introduzimos um script de automação para gerar relatórios de auditoria. Este script processa os resultados da auditoria e gera um relatório detalhado, facilitando a análise e a documentação.

#### Uso:
Execute o script `audit_report_generator.py` com os resultados da auditoria para obter um relatório formatado.

### 3. Integração com Ferramentas Externas (Extensões do Core)
Expandimos o núcleo do Vimana Framework com uma nova classe de integração para ferramentas externas. Isso permite a execução de ferramentas e scripts externos, aumentando a flexibilidade e as capacidades do framework.

#### Uso:
Utilize a classe `ExternalToolIntegration` para integrar e executar ferramentas externas conforme necessário.

## Conclusão

Estas adições ao Vimana Framework visam melhorar a eficiência e a eficácia das auditorias de segurança da informação. Encorajamos os usuários a experimentar esses novos recursos e contribuir com feedback para futuras melhorias.
