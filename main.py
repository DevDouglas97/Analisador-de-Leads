from api.cnpjws import ConsultaCNPJ
from api.openrouter import AnalisadorIA

def main():
    print("=" * 50)
    print("  ANALISADOR DE LEADS COM IA (CNPJ.ws + OpenRouter)")
    print("=" * 50 + "\n")

    # 1. Coleta de dados do usuário
    cnpj = input("Digite o CNPJ do Lead: ").strip()
    if not cnpj:
        print(" O CNPJ é obrigatório.")
        return

    mensagem_lead = input("\nQual a mensagem/dor relatada pelo Lead?: ").strip()
    if not mensagem_lead:
        print(" A mensagem do lead é obrigatória para qualificação.")
        return

    orcamento = input("Orçamento estimado (Pressione ENTER se não informado): ").strip()
    if not orcamento:
        orcamento = "Não informado"

    # 2. Consulta à CNPJ.ws
    print("\n 1. Buscando dados da empresa na CNPJ.ws...")
    consulta = ConsultaCNPJ(cnpj)
    empresa = consulta.consultar()

    if not empresa:
        print("Não foi possível obter os dados da empresa. Encerrando o processo.")
        return

    print(f"Empresa localizada: {empresa.razao_social}")
    print(f"   • Porte: {empresa.porte or 'N/A'}")
    print(f"   • Cidade/UF: {empresa.endereco.cidade} - {empresa.endereco.uf}")

    # 3. Análise com a IA via OpenRouter
    print("\n2. Enviando dados para o Analisador de IA na OpenRouter...")
    analisador = AnalisadorIA()
    analise = analisador.analisar_lead_com_empresa(
        empresa=empresa,
        mensagem_lead=mensagem_lead,
        orcamento=orcamento
    )

    # 4. Exibição dos resultados
    if analise:
        print("\n" + "=" * 50)
        print(" RESULTADO DA QUALIFICAÇÃO DO LEAD")
        print("=" * 50)
        
        score = analise.get('score', 'N/A')
        classificacao = analise.get('classificacao', 'N/A')
        print(f"• Score de Qualificação: {score}/100 [{classificacao.upper()}]")
        print(f"• Resumo da Empresa: {analise.get('resumo_empresa', 'N/A')}\n")

        print("• Motivos da Pontuação:")
        for motivo in analise.get('motivos_qualificacao', []):
            print(f"  - {motivo}")

        print(f"\n• Recomendação para Vendas:\n  {analise.get('recomendacao_vendas', 'N/A')}")
        print("=" * 50)
    else:
        print("Ocorreu uma falha ao gerar a análise com a IA.")

if __name__ == "__main__":
    main()