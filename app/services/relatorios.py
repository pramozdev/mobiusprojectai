"""
Sistema de Geração de Relatórios
Exportação para PDF e Excel de clientes e contratos
"""

from app.utils.imports import (
    os, io, datetime, date, timedelta, Flask, send_file, jsonify, text,
    pd, letter, A4, SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
    getSampleStyleSheet, ParagraphStyle, colors, inch, pdfmetrics, TTFont
)
from app.models import db, Client, Contract

class RelatorioGenerator:
    """Classe para geração de relatórios em PDF e Excel"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Configura estilos personalizados para PDF"""
        # Estilo para título
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            textColor=colors.darkblue,
            alignment=1  # Centralizado
        )
        
        # Estilo para subtítulo
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=20,
            textColor=colors.darkgray
        )
    
    def gerar_relatorio_clientes_excel(self, formato='excel'):
        """Gera relatório de clientes em Excel ou PDF"""
        try:
            # Buscar dados dos clientes
            clientes = Client.query.all()
            
            if not clientes:
                return None, "Nenhum cliente encontrado"
            
            # Preparar dados para DataFrame
            dados_clientes = []
            for cliente in clientes:
                # Contar contratos do cliente
                num_contratos = Contract.query.filter_by(client_id=cliente.id).count()
                # Calcular valor total dos contratos
                valor_total = db.session.query(db.func.sum(Contract.value)).filter_by(client_id=cliente.id).scalar() or 0
                
                dados_clientes.append({
                    'ID': cliente.id,
                    'Nome': cliente.name,
                    'Email': cliente.email,
                    'Telefone': cliente.phone or '',
                    'CNPJ/CPF': cliente.cnpj_cpf,
                    'Endereço': cliente.address or '',
                    'Cidade': cliente.city or '',
                    'Estado': cliente.state or '',
                    'Setor': cliente.sector or '',
                    'Nº Contratos': num_contratos,
                    'Valor Total': f"R$ {valor_total:,.2f}",
                    'Data Cadastro': cliente.created_at.strftime('%d/%m/%Y') if cliente.created_at else '',
                    'Última Atualização': cliente.updated_at.strftime('%d/%m/%Y') if cliente.updated_at else ''
                })
            
            df = pd.DataFrame(dados_clientes)
            
            if formato == 'excel':
                return self._exportar_excel(df, 'clientes')
            else:
                return self._exportar_pdf_clientes(dados_clientes)
                
        except Exception as e:
            return None, f"Erro ao gerar relatório: {str(e)}"
    
    def gerar_relatorio_contratos_excel(self, formato='excel'):
        """Gera relatório de contratos em Excel ou PDF"""
        try:
            # Buscar dados dos contratos com informações do cliente
            contratos = db.session.query(
                Contract, Client
            ).join(Client, Contract.client_id == Client.id).all()
            
            if not contratos:
                return None, "Nenhum contrato encontrado"
            
            dados_contratos = []
            for contrato, cliente in contratos:
                # Calcular dias até vencimento
                dias_ate_vencimento = (contrato.end_date - date.today()).days if contrato.end_date else 0
                
                # Status do contrato
                status_display = contrato.status
                if dias_ate_vencimento < 0 and contrato.status == 'Ativo':
                    status_display = 'Vencido'
                elif dias_ate_vencimento <= 30 and contrato.status == 'Ativo':
                    status_display = 'A Vencer'
                
                dados_contratos.append({
                    'ID': contrato.id,
                    'Nº Contrato': contrato.contract_number,
                    'Cliente': cliente.name,
                    'Descrição': contrato.description,
                    'Valor': f"R$ {contrato.value:,.2f}",
                    'Data Início': contrato.start_date.strftime('%d/%m/%Y') if contrato.start_date else '',
                    'Data Fim': contrato.end_date.strftime('%d/%m/%Y') if contrato.end_date else '',
                    'Dias até Vencimento': dias_ate_vencimento,
                    'Status': status_display,
                    'Método Pagamento': contrato.payment_method or '',
                    'Frequência': contrato.payment_frequency or '',
                    'Data Renovação': contrato.renewal_date.strftime('%d/%m/%Y') if contrato.renewal_date else '',
                    'Data Cadastro': contrato.created_at.strftime('%d/%m/%Y') if contrato.created_at else '',
                    'Última Atualização': contrato.updated_at.strftime('%d/%m/%Y') if contrato.updated_at else ''
                })
            
            df = pd.DataFrame(dados_contratos)
            
            if formato == 'excel':
                return self._exportar_excel(df, 'contratos')
            else:
                return self._exportar_pdf_contratos(dados_contratos)
                
        except Exception as e:
            return None, f"Erro ao gerar relatório: {str(e)}"
    
    def gerar_relatorio_resumo_geral(self, formato='excel'):
        """Gera relatório resumo com estatísticas gerais"""
        try:
            # Estatísticas de clientes
            total_clientes = Client.query.count()
            
            # Estatísticas de contratos
            total_contratos = Contract.query.count()
            valor_total = db.session.query(db.func.sum(Contract.value)).scalar() or 0
            
            # Contratos por status
            contratos_ativos = Contract.query.filter_by(status='Ativo').count()
            contratos_concluidos = Contract.query.filter_by(status='Concluído').count()
            contratos_suspensos = Contract.query.filter_by(status='Suspenso').count()
            contratos_cancelados = Contract.query.filter_by(status='Cancelado').count()
            
            # Contratos vencidos
            hoje = date.today()
            contratos_vencidos = Contract.query.filter(Contract.end_date < hoje, Contract.status == 'Ativo').count()
            
            # Contratos para renovação (próximos 30 dias)
            data_renovacao = hoje + timedelta(days=30)
            contratos_renovar = Contract.query.filter(
                Contract.renewal_date <= data_renovacao,
                Contract.renewal_date >= hoje,
                Contract.status == 'Ativo'
            ).count()
            
            # Top 5 clientes por valor
            top_clientes = db.session.query(
                Client.name,
                db.func.sum(Contract.value).label('total_valor'),
                db.func.count(Contract.id).label('num_contratos')
            ).join(Contract, Client.id == Contract.client_id)\
            .group_by(Client.id, Client.name)\
            .order_by(db.desc('total_valor'))\
            .limit(5).all()
            
            # Contratos por setor
            contratos_setor = db.session.query(
                Client.sector,
                db.func.count(Contract.id).label('num_contratos'),
                db.func.sum(Contract.value).label('total_valor')
            ).join(Contract, Client.id == Contract.client_id)\
            .group_by(Client.sector)\
            .order_by(db.desc('total_valor')).all()
            
            if formato == 'excel':
                # Criar DataFrames separados para cada seção
                dados_resumo = {
                    'Estatísticas Gerais': pd.DataFrame([
                        ['Total de Clientes', total_clientes],
                        ['Total de Contratos', total_contratos],
                        ['Valor Total dos Contratos', f"R$ {valor_total:,.2f}"],
                        ['Contratos Ativos', contratos_ativos],
                        ['Contratos Concluídos', contratos_concluidos],
                        ['Contratos Suspensos', contratos_suspensos],
                        ['Contratos Cancelados', contratos_cancelados],
                        ['Contratos Vencidos', contratos_vencidos],
                        ['Contratos para Renovação', contratos_renovar]
                    ], columns=['Métrica', 'Valor']),
                    
                    'Top 5 Clientes': pd.DataFrame([
                        [cliente[0], f"R$ {cliente[1]:,.2f}", cliente[2]]
                        for cliente in top_clientes
                    ], columns=['Cliente', 'Valor Total', 'Nº Contratos']),
                    
                    'Contratos por Setor': pd.DataFrame([
                        [setor[0] or 'Não Informado', setor[1], f"R$ {setor[2]:,.2f}"]
                        for setor in contratos_setor
                    ], columns=['Setor', 'Nº Contratos', 'Valor Total'])
                }
                
                return self._exportar_excel_multiplanilha(dados_resumo, 'resumo_geral')
            else:
                return self._exportar_pdf_resumo({
                    'estatisticas': [
                        ('Total de Clientes', total_clientes),
                        ('Total de Contratos', total_contratos),
                        ('Valor Total dos Contratos', f"R$ {valor_total:,.2f}"),
                        ('Contratos Ativos', contratos_ativos),
                        ('Contratos Concluídos', contratos_concluidos),
                        ('Contratos Suspensos', contratos_suspensos),
                        ('Contratos Cancelados', contratos_cancelados),
                        ('Contratos Vencidos', contratos_vencidos),
                        ('Contratos para Renovação', contratos_renovar)
                    ],
                    'top_clientes': [(c[0], f"R$ {c[1]:,.2f}", c[2]) for c in top_clientes],
                    'setores': [(s[0] or 'Não Informado', s[1], f"R$ {s[2]:,.2f}") for s in contratos_setor]
                })
                
        except Exception as e:
            return None, f"Erro ao gerar relatório: {str(e)}"
    
    def _exportar_excel(self, df, nome_arquivo):
        """Exporta DataFrame para Excel"""
        try:
            output = io.BytesIO()
            
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Dados', index=False)
                
                # Obter o workbook e worksheet para formatação
                workbook = writer.book
                worksheet = writer.sheets['Dados']
                
                # Formatos
                header_format = workbook.add_format({
                    'bold': True,
                    'text_wrap': True,
                    'valign': 'top',
                    'fg_color': '#D7E4BC',
                    'border': 1
                })
                
                money_format = workbook.add_format({'num_format': 'R$ #,##0.00'})
                
                # Aplicar formato ao cabeçalho
                for col_num, value in enumerate(df.columns.values):
                    worksheet.write(0, col_num, value, header_format)
                
                # Ajustar largura das colunas
                for i, col in enumerate(df.columns):
                    max_len = max(
                        df[col].astype(str).map(len).max(),
                        len(col)
                    ) + 2
                    worksheet.set_column(i, i, max_len)
                
                # Aplicar formato de moeda às colunas de valor
                for i, col in enumerate(df.columns):
                    if 'Valor' in col or 'valor' in col.lower():
                        worksheet.set_column(i, i, None, money_format)
            
            output.seek(0)
            
            # Gerar nome do arquivo com timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"relatorio_{nome_arquivo}_{timestamp}.xlsx"
            
            return output, filename
            
        except Exception as e:
            return None, f"Erro ao exportar Excel: {str(e)}"
    
    def _exportar_excel_multiplanilha(self, dados_dict, nome_arquivo):
        """Exporta múltiplas planilhas para Excel"""
        try:
            output = io.BytesIO()
            
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                for nome_planilha, df in dados_dict.items():
                    df.to_excel(writer, sheet_name=nome_planilha, index=False)
                    
                    # Formatação
                    workbook = writer.book
                    worksheet = writer.sheets[nome_planilha]
                    
                    header_format = workbook.add_format({
                        'bold': True,
                        'text_wrap': True,
                        'valign': 'top',
                        'fg_color': '#D7E4BC',
                        'border': 1
                    })
                    
                    # Aplicar formato ao cabeçalho
                    for col_num, value in enumerate(df.columns.values):
                        worksheet.write(0, col_num, value, header_format)
                    
                    # Ajustar largura das colunas
                    for i, col in enumerate(df.columns):
                        max_len = max(
                            df[col].astype(str).map(len).max(),
                            len(col)
                        ) + 2
                        worksheet.set_column(i, i, max_len)
            
            output.seek(0)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"relatorio_{nome_arquivo}_{timestamp}.xlsx"
            
            return output, filename
            
        except Exception as e:
            return None, f"Erro ao exportar Excel multiplanilha: {str(e)}"
    
    def _finalizar_pdf(self, doc, output, nome_base, story):
        """Finaliza a geração do PDF e retorna o arquivo com timestamp"""
        try:
            doc.build(story)
            output.seek(0)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"relatorio_{nome_base}_{timestamp}.pdf"
            
            return output, filename
            
        except Exception as e:
            return None, f"Erro ao exportar PDF: {str(e)}"
    
    def _exportar_pdf_clientes(self, dados_clientes):
        """Exporta relatório de clientes para PDF"""
        try:
            output = io.BytesIO()
            doc = SimpleDocTemplate(output, pagesize=A4)
            story = []
            
            # Título
            title = Paragraph("Relatório de Clientes", self.title_style)
            story.append(title)
            story.append(Spacer(1, 12))
            
            # Data de geração
            data_geracao = f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
            story.append(Paragraph(data_geracao, self.styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Tabela de dados
            if dados_clientes:
                # Cabeçalho da tabela
                headers = ['ID', 'Nome', 'Email', 'Telefone', 'CNPJ/CPF', 'Cidade', 'Estado', 'Setor', 'Contratos', 'Valor Total']
                
                # Dados da tabela
                table_data = [headers]
                for cliente in dados_clientes:
                    row = [
                        str(cliente['ID']),
                        cliente['Nome'][:30],  # Limitar tamanho
                        cliente['Email'][:25],
                        cliente['Telefone'] or '',
                        cliente['CNPJ/CPF'],
                        cliente['Cidade'][:20] if cliente['Cidade'] else '',
                        cliente['Estado'] or '',
                        cliente['Setor'][:15] if cliente['Setor'] else '',
                        str(cliente['Nº Contratos']),
                        cliente['Valor Total']
                    ]
                    table_data.append(row)
                
                # Criar tabela
                table = Table(table_data, repeatRows=1)
                
                # Estilo da tabela
                style = TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                ])
                
                table.setStyle(style)
                story.append(table)
            
            # Rodapé
            story.append(Spacer(1, 20))
            total_clientes = len(dados_clientes)
            footer = Paragraph(f"Total de Clientes: {total_clientes}", self.styles['Normal'])
            story.append(footer)
            
            return self._finalizar_pdf(doc, output, "clientes", story)
            
        except Exception as e:
            return None, f"Erro ao exportar PDF: {str(e)}"
    
    def _exportar_pdf_contratos(self, dados_contratos):
        """Exporta relatório de contratos para PDF"""
        try:
            output = io.BytesIO()
            doc = SimpleDocTemplate(output, pagesize=A4)
            story = []
            
            # Título
            title = Paragraph("Relatório de Contratos", self.title_style)
            story.append(title)
            story.append(Spacer(1, 12))
            
            # Data de geração
            data_geracao = f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
            story.append(Paragraph(data_geracao, self.styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Tabela de dados
            if dados_contratos:
                # Cabeçalho da tabela
                headers = ['ID', 'Contrato', 'Cliente', 'Valor', 'Início', 'Fim', 'Status', 'Pagamento']
                
                # Dados da tabela
                table_data = [headers]
                for contrato in dados_contratos:
                    row = [
                        str(contrato['ID']),
                        contrato['Nº Contrato'][:15],
                        contrato['Cliente'][:25],
                        contrato['Valor'],
                        contrato['Data Início'],
                        contrato['Data Fim'],
                        contrato['Status'],
                        contrato['Método Pagamento'][:15] if contrato['Método Pagamento'] else ''
                    ]
                    table_data.append(row)
                
                # Criar tabela
                table = Table(table_data, repeatRows=1)
                
                # Estilo da tabela
                style = TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                ])
                
                table.setStyle(style)
                story.append(table)
            
            # Rodapé
            story.append(Spacer(1, 20))
            total_contratos = len(dados_contratos)
            footer = Paragraph(f"Total de Contratos: {total_contratos}", self.styles['Normal'])
            story.append(footer)
            
            return self._finalizar_pdf(doc, output, "contratos", story)
            
        except Exception as e:
            return None, f"Erro ao exportar PDF: {str(e)}"
    
    def _exportar_pdf_resumo(self, dados):
        """Exporta relatório resumo para PDF"""
        try:
            output = io.BytesIO()
            doc = SimpleDocTemplate(output, pagesize=A4)
            story = []
            
            # Título
            title = Paragraph("Relatório Resumo - Sistema de Gestão", self.title_style)
            story.append(title)
            story.append(Spacer(1, 12))
            
            # Data de geração
            data_geracao = f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
            story.append(Paragraph(data_geracao, self.styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Estatísticas Gerais
            subtitle1 = Paragraph("Estatísticas Gerais", self.subtitle_style)
            story.append(subtitle1)
            story.append(Spacer(1, 12))
            
            # Tabela de estatísticas
            stats_data = [['Métrica', 'Valor']]
            stats_data.extend(dados['estatisticas'])
            
            stats_table = Table(stats_data)
            stats_style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
            ])
            stats_table.setStyle(stats_style)
            story.append(stats_table)
            
            story.append(Spacer(1, 20))
            
            # Top 5 Clientes
            subtitle2 = Paragraph("Top 5 Clientes por Valor", self.subtitle_style)
            story.append(subtitle2)
            story.append(Spacer(1, 12))
            
            # Tabela top clientes
            clientes_data = [['Cliente', 'Valor Total', 'Nº Contratos']]
            clientes_data.extend(dados['top_clientes'])
            
            clientes_table = Table(clientes_data)
            clientes_style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
            ])
            clientes_table.setStyle(clientes_style)
            story.append(clientes_table)
            
            story.append(Spacer(1, 20))
            
            # Contratos por Setor
            subtitle3 = Paragraph("Contratos por Setor", self.subtitle_style)
            story.append(subtitle3)
            story.append(Spacer(1, 12))
            
            # Tabela setores
            setores_data = [['Setor', 'Nº Contratos', 'Valor Total']]
            setores_data.extend(dados['setores'])
            
            setores_table = Table(setores_data)
            setores_style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
            ])
            setores_table.setStyle(setores_style)
            story.append(setores_table)
            
            return self._finalizar_pdf(doc, output, "resumo_geral", story)
            
        except Exception as e:
            return None, f"Erro ao exportar PDF resumo: {str(e)}"

    def gerar_relatorio_financeiro_excel(self, dados_financeiros):
        """Gera relatório financeiro completo em Excel"""
        try:
            nome_arquivo = f"relatorio_financeiro_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            with pd.ExcelWriter(f"{nome_arquivo}.xlsx", engine='xlsxwriter') as writer:
                workbook = writer.book

                # Aba de Contratos
                contratos_df = pd.DataFrame(dados_financeiros['contracts'])
                contratos_df.to_excel(writer, sheet_name='Contratos', index=False)

                # Aba de Pagamentos
                pagamentos_df = pd.DataFrame(dados_financeiros['payments'])
                pagamentos_df.to_excel(writer, sheet_name='Pagamentos', index=False)

                # Aba de Faturas
                faturas_df = pd.DataFrame(dados_financeiros['invoices'])
                faturas_df.to_excel(writer, sheet_name='Faturas', index=False)

                # Aba de Resumo Financeiro
                resumo_data = {
                    'Métrica': [
                        'Total de Contratos',
                        'Contratos Ativos',
                        'Valor Total de Contratos',
                        'Total Pago',
                        'Valor Pendente',
                        'Total de Faturas',
                        'Faturas Pagas',
                        'Faturas Pendentes'
                    ],
                    'Valor': [
                        len(dados_financeiros['contracts']),
                        len([c for c in dados_financeiros['contracts'] if c.get('status') == 'Ativo']),
                        sum(c.get('value', 0) for c in dados_financeiros['contracts']),
                        sum(p.get('amount', 0) for p in dados_financeiros['payments']),
                        sum(c.get('value', 0) for c in dados_financeiros['contracts']) - sum(p.get('amount', 0) for p in dados_financeiros['payments']),
                        len(dados_financeiros['invoices']),
                        len([i for i in dados_financeiros['invoices'] if i.get('status') == 'Pago']),
                        len([i for i in dados_financeiros['invoices'] if i.get('status') != 'Pago'])
                    ]
                }
                resumo_df = pd.DataFrame(resumo_data)
                resumo_df.to_excel(writer, sheet_name='Resumo', index=False)

            output = io.BytesIO()
            with open(f"{nome_arquivo}.xlsx", 'rb') as f:
                output.write(f.read())

            os.remove(f"{nome_arquivo}.xlsx")
            output.seek(0)

            return output, f"{nome_arquivo}.xlsx"

        except Exception as e:
            print(f"Erro ao gerar relatório financeiro Excel: {e}")
            return None, str(e)

    def gerar_relatorio_financeiro_pdf(self, dados_financeiros):
        """Gera relatório financeiro completo em PDF"""
        try:
            nome_arquivo = f"relatorio_financeiro_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            doc = SimpleDocTemplate(f"{nome_arquivo}.pdf", pagesize=letter)
            story = []

            # Título
            title_style = ParagraphStyle(
                'Title',
                parent=getSampleStyleSheet()['Heading1'],
                fontSize=16,
                spaceAfter=30,
                alignment=1
            )
            story.append(Paragraph("Relatório Financeiro Completo", title_style))
            story.append(Spacer(1, 12))

            # Resumo Executivo
            story.append(Paragraph("Resumo Executivo", getSampleStyleSheet()['Heading2']))
            story.append(Spacer(1, 12))

            resumo_data = [
                ["Total de Contratos", str(len(dados_financeiros['contracts']))],
                ["Contratos Ativos", str(len([c for c in dados_financeiros['contracts'] if c.get('status') == 'Ativo']))],
                ["Valor Total de Contratos", f"R$ {sum(c.get('value', 0) for c in dados_financeiros['contracts']):,.2f}"],
                ["Total Pago", f"R$ {sum(p.get('amount', 0) for p in dados_financeiros['payments']):,.2f}"],
                ["Valor Pendente", f"R$ {(sum(c.get('value', 0) for c in dados_financeiros['contracts']) - sum(p.get('amount', 0) for p in dados_financeiros['payments'])):,.2f}"],
            ]

            resumo_table = Table(resumo_data, colWidths=[200, 150])
            resumo_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(resumo_table)
            story.append(Spacer(1, 20))

            # Construir PDF
            doc.build(story)

            output = io.BytesIO()
            with open(f"{nome_arquivo}.pdf", 'rb') as f:
                output.write(f.read())

            os.remove(f"{nome_arquivo}.pdf")
            output.seek(0)

            return output, f"{nome_arquivo}.pdf"

        except Exception as e:
            print(f"Erro ao gerar relatório financeiro PDF: {e}")
            return None, str(e)

    def gerar_relatorio_dashboard_excel(self, dados_dashboard):
        """Gera relatório do dashboard em Excel"""
        try:
            nome_arquivo = f"relatorio_dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            with pd.ExcelWriter(f"{nome_arquivo}.xlsx", engine='xlsxwriter') as writer:
                # Aba de Métricas
                metricas_df = pd.DataFrame([dados_dashboard['metricas']])
                metricas_df.to_excel(writer, sheet_name='Métricas', index=False)

                # Aba de Top Clientes
                top_clientes_df = pd.DataFrame(dados_dashboard['top_clientes'])
                top_clientes_df.to_excel(writer, sheet_name='Top Clientes', index=False)

                # Aba de Valor por Setor
                valor_setor_df = pd.DataFrame(dados_dashboard['valor_setor'])
                valor_setor_df.to_excel(writer, sheet_name='Valor por Setor', index=False)

                # Aba de Valor por Região
                valor_regiao_df = pd.DataFrame(dados_dashboard['valor_regiao'])
                valor_regiao_df.to_excel(writer, sheet_name='Valor por Região', index=False)

            output = io.BytesIO()
            with open(f"{nome_arquivo}.xlsx", 'rb') as f:
                output.write(f.read())

            os.remove(f"{nome_arquivo}.xlsx")
            output.seek(0)

            return output, f"{nome_arquivo}.xlsx"

        except Exception as e:
            print(f"Erro ao gerar relatório dashboard Excel: {e}")
            return None, str(e)

    def gerar_relatorio_dashboard_pdf(self, dados_dashboard):
        """Gera relatório do dashboard em PDF"""
        try:
            nome_arquivo = f"relatorio_dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            doc = SimpleDocTemplate(f"{nome_arquivo}.pdf", pagesize=letter)
            story = []

            # Título
            title_style = ParagraphStyle(
                'Title',
                parent=getSampleStyleSheet()['Heading1'],
                fontSize=16,
                spaceAfter=30,
                alignment=1
            )
            story.append(Paragraph("Relatório do Dashboard", title_style))
            story.append(Spacer(1, 12))

            # Métricas Principais
            story.append(Paragraph("Métricas Principais", getSampleStyleSheet()['Heading2']))
            story.append(Spacer(1, 12))

            metricas = dados_dashboard['metricas']
            metricas_data = [
                ["Total de Contratos", str(metricas.get('total_contratos', 0))],
                ["Contratos Ativos", str(metricas.get('ativos', 0))],
                ["Contratos Vencidos", str(metricas.get('vencidos', 0))],
                ["Valor Total", f"R$ {metricas.get('valor_total', 0):,.2f}"],
            ]

            metricas_table = Table(metricas_data, colWidths=[200, 150])
            metricas_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(metricas_table)

            # Construir PDF
            doc.build(story)

            output = io.BytesIO()
            with open(f"{nome_arquivo}.pdf", 'rb') as f:
                output.write(f.read())

            os.remove(f"{nome_arquivo}.pdf")
            output.seek(0)

            return output, f"{nome_arquivo}.pdf"

        except Exception as e:
            print(f"Erro ao gerar relatório dashboard PDF: {e}")
            return None, str(e)

    def gerar_relatorio_auditoria_excel(self, dados_auditoria):
        """Gera relatório de auditoria em Excel"""
        try:
            nome_arquivo = f"relatorio_auditoria_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            audit_logs_df = pd.DataFrame(dados_auditoria['audit_logs'])
            audit_logs_df.to_excel(f"{nome_arquivo}.xlsx", index=False)

            output = io.BytesIO()
            with open(f"{nome_arquivo}.xlsx", 'rb') as f:
                output.write(f.read())

            os.remove(f"{nome_arquivo}.xlsx")
            output.seek(0)

            return output, f"{nome_arquivo}.xlsx"

        except Exception as e:
            print(f"Erro ao gerar relatório auditoria Excel: {e}")
            return None, str(e)

    def gerar_relatorio_auditoria_pdf(self, dados_auditoria):
        """Gera relatório de auditoria em PDF"""
        try:
            nome_arquivo = f"relatorio_auditoria_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            doc = SimpleDocTemplate(f"{nome_arquivo}.pdf", pagesize=letter)
            story = []

            # Título
            title_style = ParagraphStyle(
                'Title',
                parent=getSampleStyleSheet()['Heading1'],
                fontSize=16,
                spaceAfter=30,
                alignment=1
            )
            story.append(Paragraph("Relatório de Auditoria", title_style))
            story.append(Spacer(1, 12))

            # Período
            periodo = dados_auditoria['period']
            story.append(Paragraph(f"Período: {periodo['start']} - {periodo['end']}", getSampleStyleSheet()['Normal']))
            story.append(Spacer(1, 12))

            # Tabela de logs
            headers = ['Data/Hora', 'Usuário', 'Ação', 'Tabela', 'Registro']
            table_data = [headers]

            for log in dados_auditoria['audit_logs'][:50]:  # Limitar a 50 registros para o PDF
                table_data.append([
                    log['created_at'],
                    log['user_name'],
                    log['action'],
                    log['table_name'],
                    str(log['record_id'])
                ])

            audit_table = Table(table_data, colWidths=[80, 100, 60, 80, 60])
            audit_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(audit_table)

            # Construir PDF
            doc.build(story)

            output = io.BytesIO()
            with open(f"{nome_arquivo}.pdf", 'rb') as f:
                output.write(f.read())

            os.remove(f"{nome_arquivo}.pdf")
            output.seek(0)

            return output, f"{nome_arquivo}.pdf"

        except Exception as e:
            print(f"Erro ao gerar relatório auditoria PDF: {e}")
            return None, str(e)
