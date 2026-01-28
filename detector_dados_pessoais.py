#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Detector Automático de Dados Pessoais - 1º Hackathon CGDF
Categoria: Acesso à Informação
"""

import re
import pandas as pd
import sys
import json
from datetime import datetime

class DetectorDadosPessoais:
    """Detector de dados pessoais em textos usando Regex"""
    
    def __init__(self):
        self.padroes = {
            'CPF': r'\b\d{3}\.\d{3}\.\d{3}-\d{2}\b',
            'EMAIL': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',
            'TELEFONE': r'\(\d{2}\)\s?\d{4,5}-\d{4}',
            'RG': r'\b\d{1,2}\.\d{3}\.\d{3}-\d{1}\b',
            'NOME': r'\b[A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-záéíóúâêôãõç]+\s+(?:da\s+|de\s+|do\s+)?[A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-záéíóúâêôãõç]+(?:\s+[A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-záéíóúâêôãõç]+)*'
        }
        
        self.pesos_risco = {
            'CPF': 10,
            'RG': 9,
            'NOME': 7,
            'EMAIL': 6,
            'TELEFONE': 5
        }
    
    def detectar(self, texto):
        """Detecta dados pessoais no texto"""
        achados = {}
        for tipo, padrao in self.padroes.items():
            matches = re.findall(padrao, texto)
            if matches:
                achados[tipo] = list(set(matches))  # Remove duplicatas
        return achados
    
    def calcular_confianca(self, achados):
        """Calcula score de confiança baseado nos dados encontrados"""
        if not achados or not any(achados.values()):
            return 0.0
        
        score_total = sum(
            self.pesos_risco.get(tipo, 5) * len(valores)
            for tipo, valores in achados.items()
        )
        
        # Normalizar para 0-1
        return min(score_total / 20.0, 1.0)
    
    def gerar_explicacao(self, achados):
        """Gera explicação detalhada para auditoria"""
        if not achados or not any(achados.values()):
            return "Nenhum dado pessoal identificado pelo detector automático."
        
        tipos = [tipo for tipo, valores in achados.items() if valores]
        explicacao = f"Detectados {sum(len(v) for v in achados.values())} dado(s) pessoal(is): "
        explicacao += ", ".join(tipos)
        explicacao += " via REGEX."
        return explicacao
    
    def processar_pedido(self, id_pedido, texto):
        """Processa um pedido individual"""
        achados = self.detectar(texto)
        contem_dados = any(achados.values())
        confianca = self.calcular_confianca(achados)
        tipos_detectados = [tipo for tipo, valores in achados.items() if valores]
        explicacao = self.gerar_explicacao(achados)
        
        return {
            'id_pedido': id_pedido,
            'contem_dados_pessoais': contem_dados,
            'confianca_score': round(confianca, 2),
            'tipos_detectados': tipos_detectados,
            'dados_encontrados': achados,
            'explicacao': explicacao,
            'processado_em': datetime.now().isoformat()
        }


def main():
    """Função principal"""
    if len(sys.argv) < 2:
        print("Uso: python detector_dados_pessoais.py <arquivo_entrada.csv>")
        sys.exit(1)
    
    arquivo_entrada = sys.argv[1]
    
    print(f"🔍 Carregando arquivo: {arquivo_entrada}")
    df = pd.read_csv(arquivo_entrada)
    
    if 'texto_original' not in df.columns and 'texto' not in df.columns:
        print("❌ Erro: CSV deve conter coluna 'texto_original' ou 'texto'")
        sys.exit(1)
    
    coluna_texto = 'texto_original' if 'texto_original' in df.columns else 'texto'
    coluna_id = 'id_pedido' if 'id_pedido' in df.columns else df.columns[0]
    
    detector = DetectorDadosPessoais()
    resultados = []
    
    print(f"⚙️  Processando {len(df)} pedidos...")
    for idx, row in df.iterrows():
        resultado = detector.processar_pedido(row[coluna_id], row[coluna_texto])
        resultados.append(resultado)
        print(f"  [{idx+1}/{len(df)}] {resultado['id_pedido']}: {resultado['contem_dados_pessoais']}")
    
    # Criar DataFrame de saída
    df_resultado = pd.DataFrame([
        {
            'id_pedido': r['id_pedido'],
            'contem_dados_pessoais': r['contem_dados_pessoais'],
            'confianca': r['confianca_score'],
            'tipos_detectados': str(r['tipos_detectados']),
            'explicacao': r['explicacao']
        }
        for r in resultados
    ])
    
    # Salvar CSV
    arquivo_saida = 'resultado.csv'
    df_resultado.to_csv(arquivo_saida, index=False)
    print(f"\n✅ Resultado salvo em: {arquivo_saida}")
    
    # Salvar JSON completo
    with open('resultado_completo.json', 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    print(f"✅ Resultado completo salvo em: resultado_completo.json")
    
    # Estatísticas
    total_com_dados = sum(1 for r in resultados if r['contem_dados_pessoais'])
    print(f"\n📊 Estatísticas:")
    print(f"   Total processados: {len(resultados)}")
    print(f"   Com dados pessoais: {total_com_dados} ({total_com_dados/len(resultados)*100:.1f}%)")
    print(f"   Sem dados pessoais: {len(resultados)-total_com_dados}")


if __name__ == '__main__':
    main()
