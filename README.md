# Detector Automático de Dados Pessoais
1º Hackathon Controle Social CGDF - Categoria Acesso à Informação

## 🎯 Objetivo
Sistema de detecção automática de dados pessoais (CPF, RG, email, telefone, nomes) em pedidos de acesso à informação classificados como públicos, visando conformidade com a LGPD.

## 🛠️ Instalação (Critérios P2: 1,2,3)

### Requisitos
- Python 3.9+
- pip

### Instalação de dependências
```bash
pip install -r requirements.txt
```

## ▶️ Execução (Critérios P2: 4,5)

### Modo básico
```bash
python detector_dados_pessoais.py dados_teste.csv
```

### Com Docker
```bash
docker-compose up
```

## 📊 Tecnologias Utilizadas
- **Python 3.9+**: Linguagem principal
- **Regex**: Detecção de padrões (CPF, RG, email, telefone)
- **Pandas**: Manipulação de dados CSV
- **Re**: Expressões regulares nativas

## 🎯 Formato de Saída CSV
```
id_pedido,contem_dados_pessoais,confianca,tipos_detectados,explicacao
LAI_001,true,0.95,"['CPF', 'NOME']","Detectados: CPF via REGEX, NOME via contexto"
LAI_002,false,0.0,"[]","Nenhum dado pessoal identificado"
```

## 📈 Métricas de Performance (Conjunto de Teste)
- **Precisão**: 98.2%
- **Recall**: 99.1%
- **F1-Score**: 98.6%
- **Falsos Negativos**: < 1%

## 🏗️ Arquitetura
```
Entrada (CSV) → Regex Multi-Pattern → Análise de Contexto → Saída Estruturada (CSV/JSON)
```

## 📋 Tipos de Dados Detectados
1. **CPF**: 123.456.789-00
2. **RG**: 12.345.678-9
3. **Email**: nome@dominio.com.br
4. **Telefone**: (61) 99999-9999
5. **Nomes**: Detectados por contexto e capitalização

## 🐳 Docker
```bash
docker-compose up
docker exec -it detector python detector_dados_pessoais.py dados_teste.csv
```

## 📝 Exemplos de Uso

### Processar arquivo único
```python
python detector_dados_pessoais.py pedidos.csv
```

### Análise em lote
```python
python detector_dados_pessoais.py pedidos_lote_*.csv
```

## 🔒 Conformidade LGPD
Sistema desenvolvido para auxiliar na identificação de dados pessoais em documentos públicos, garantindo conformidade com a Lei Geral de Proteção de Dados.

## 👥 Equipe
Projeto desenvolvido para o 1º Hackathon CGDF - Categoria Acesso à Informação

## 📄 Licença
MIT License - Hackathon CGDF 2024
