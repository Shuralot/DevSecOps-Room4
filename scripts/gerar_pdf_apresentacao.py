import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Header (páginas > 1)
        if self._pageNumber > 1:
            self.drawString(36, 805, "TaskFlow — Roteiro de Apresentação | Atividade 1 (DevSecOps)")
            self.drawRightString(A4[0] - 36, 805, "Grupo Room 4 · Shuralot/DevSecOps-Room4")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(36, 800, A4[0] - 36, 800)

        # Footer
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(A4[0] - 36, 25, page_str)
        self.drawString(36, 25, "Confidencial / Uso Acadêmico — Duração total: ~10 minutos cronometrados")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(36, 35, A4[0] - 36, 35)
        self.restoreState()

def build_pdf(output_paths):
    doc = SimpleDocTemplate(
        output_paths[0],
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=46,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    c_primary = colors.HexColor("#0f172a")     # Slate 900
    c_secondary = colors.HexColor("#1e40af")   # Blue 800
    c_accent = colors.HexColor("#0284c7")      # Sky 600
    c_dark = colors.HexColor("#1e293b")        # Slate 800
    c_muted = colors.HexColor("#475569")       # Slate 600
    c_bg_box = colors.HexColor("#f8fafc")      # Slate 50
    c_border = colors.HexColor("#e2e8f0")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=c_primary,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=c_muted,
        spaceAfter=12
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=c_secondary,
        spaceBefore=10,
        spaceAfter=6
    )

    slide_badge_style = ParagraphStyle(
        'SlideBadge',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.white
    )

    slide_title_style = ParagraphStyle(
        'SlideTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=c_primary
    )

    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12.5,
        textColor=c_dark
    )

    bold_label = ParagraphStyle(
        'BoldLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=c_secondary
    )

    script_text = ParagraphStyle(
        'ScriptText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#0f172a")
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=c_dark
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=c_dark
    )

    story = []

    # === CAPA / CABEÇALHO ===
    story.append(Paragraph("TaskFlow — Roteiro de Apresentação Alinhado", title_style))
    story.append(Paragraph("<b>Atividade 1: Lab de Esteira Segura</b> | Grupo Room 4 · Repositório: <code>Shuralot/DevSecOps-Room4</code> · Duração: 10 minutos cronometrados", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_secondary, spaceBefore=0, spaceAfter=8))

    # Tabela de Apresentação Individual
    story.append(Paragraph("Estrutura da Apresentação (Condução Integral)", section_heading))
    
    summary_data = [
        [
            Paragraph("Apresentador Principal", table_header),
            Paragraph("Slides do PDF", table_header),
            Paragraph("Foco Temático", table_header),
            Paragraph("Tempo Estimado", table_header)
        ],
        [
            Paragraph("<b>Júlio Santos</b> (@Shuralot)", table_cell),
            Paragraph("01 ao 08 (Integral)", table_cell),
            Paragraph("Abertura, Pipelines CI/CD, Correções no app.py, Hardening Docker, Demo do Gate e Conclusão", table_cell),
            Paragraph("0:00–10:00 (10 min)", table_cell)
        ],
        [
            Paragraph("<i>Diego Buarque, Filipe Almeida e Equipe</i>", table_cell),
            Paragraph("Coautores", table_cell),
            Paragraph("Desenvolvimento conjunto das esteiras e suporte técnico nas arguições da banca", table_cell),
            Paragraph("Suporte / Q&A", table_cell)
        ]
    ]

    t_summary = Table(summary_data, colWidths=[130, 85, 220, 88])
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_secondary),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_box])
    ]))
    story.append(t_summary)
    story.append(Spacer(1, 8))

    # Checklist Pré-Apresentação
    story.append(Paragraph("Checklist Operacional Pré-Apresentação (Obrigatório)", section_heading))
    checklist_text = """
    <b>1. Visibilidade & Colaboradores:</b> Repositório privado com <code>@HardSource</code> como colaborador com permissão de leitura.<br/>
    <b>2. Proteção da Branch main:</b> PR obrigatório, aprovação do <code>CODEOWNERS</code> e 5 checks obrigatórios ativados (<code>CI - build lint testes</code>, <code>SAST - Semgrep</code>, <code>Segredos - Gitleaks</code>, <code>SCA - pip-audit</code>, <code>Container - build e Trivy</code>).<br/>
    <b>3. Ambiente Preparado:</b> Deixar abas abertas no navegador: PR da falha controlada, logs do GitHub Actions, código <code>app.py</code> e <code>docs/hardening.md</code>.
    """
    story.append(Paragraph(checklist_text, body_style))
    story.append(Spacer(1, 10))

    # Função auxiliar para renderizar cada slide
    def render_slide(slide_num, tag_bloco, tempo, titulo, responsavel, o_que_mostrar, fala, pontos_chave):
        badge_header = [
            [
                Paragraph(f"SLIDE {slide_num:02d} | {tag_bloco} ({tempo})", slide_badge_style),
                Paragraph(f"Responsável: <b>{responsavel}</b>", slide_badge_style)
            ]
        ]
        t_badge = Table(badge_header, colWidths=[260, 263])
        t_badge.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), c_secondary),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))

        content_rows = [
            [Paragraph(f"<b>Tema:</b> {titulo}", slide_title_style)],
            [Paragraph(f"<b>O que mostrar em tela:</b> {o_que_mostrar}", body_style)],
            [Paragraph(f"<b>Fala Sugerida (Script):</b><br/>{fala}", script_text)],
            [Paragraph(f"<b>Pontos Técnicos / Decisões:</b> {pontos_chave}", body_style)]
        ]
        t_content = Table(content_rows, colWidths=[523])
        t_content.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), c_bg_box),
            ('BOX', (0, 0), (-1, -1), 0.5, c_border),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('LINEBELOW', (0, 0), (-1, -2), 0.5, c_border)
        ]))

        return KeepTogether([t_badge, t_content, Spacer(1, 8)])

    # === SLIDES 01 a 08 ===
    story.append(Paragraph("Roteiro Slide a Slide (Alinhado ao PDF de Apresentação)", section_heading))

    # Slide 1
    story.append(render_slide(
        1, "CONTEXTO", "0:00–0:30",
        "TaskFlow — Esteira Segura de CI",
        "Júlio Santos",
        "Slide 1 do PDF ou página inicial do repositório no GitHub (Shuralot/DevSecOps-Room4).",
        "“Boa noite professor. Somos o Grupo Room 4. Nosso objetivo foi transformar a TaskFlow em uma aplicação com segurança embutida em uma esteira de CI no GitHub Actions. Nosso foco não foi apenas rodar scanners, mas construir quality gates de verdade, onde o Pull Request é o portão de controle e vulnerabilidades bloqueiam o merge na main. Dividimos a apresentação entre os membros reais da equipe para demonstrar código, pipelines, containers e a demonstração prática do gate.”",
        "Destacar que o repositório é privado e o professor @HardSource está adicionado como leitor."
    ))

    # Slide 2
    story.append(render_slide(
        2, "ESTEIRA", "0:30–1:30",
        "Verificações antes da Integração",
        "Júlio Santos",
        "Pasta .github/workflows/ (ci.yml, sast.yml, sca.yml, container.yml) e .github/CODEOWNERS.",
        "“Estruturamos a esteira em 4 workflows independentes e modulares: CI com checagem de hashes e lint, SAST com Semgrep e Gitleaks, SCA com pip-audit e Dependabot, e Container com build e Trivy. Em todos os pipelines aplicamos o princípio do privilégio mínimo com permissions: contents: read e fixamos todas as GitHub Actions por hash SHA completo para neutralizar ataques na cadeia de suprimentos. A branch main exige a aprovação de todos esses 5 checks para liberar qualquer merge.”",
        "Explicar que pipeline que falha não adianta se a main não tiver proteção ativa obrigando os checks."
    ))

    # Slide 3
    story.append(render_slide(
        3, "CÓDIGO", "1:30–2:30",
        "Correções Exigidas na Aplicação",
        "Júlio Santos",
        "Arquivo app.py (funções create_app, create-user, login, tasks e busca).",
        "“Em vez de mascarar regras dos scanners, corrigimos o código na fonte: no app.py, substituímos todas as consultas concatenadas por consultas SQL parametrizadas com placeholders ?, impedindo que a entrada do usuário modifique a instrução do banco. Eliminamos senhas em texto puro usando hashing com salt (generate_password_hash e check_password_hash da Werkzeug). E a SECRET_KEY foi completamente retirada do repositório: ela é lida estritamente de TASKFLOW_SECRET_KEY do ambiente, falhando imediatamente se não for definida.”",
        "Mencionar também a inclusão de proteção CSRF com CSRFProtect e validação de senhas com mínimo de 12 caracteres."
    ))

    # Slide 4
    story.append(render_slide(
        4, "DOCKER", "2:30–3:30",
        "Hardening do Container",
        "Júlio Santos",
        "Arquivo Dockerfile e script scripts/docker-run-seguro.sh.",
        "“Corrigimos as 6 falhas críticas da imagem original: 1) Trocamos a base genérica latest por Python 3.12 Alpine fixada por versão e digest SHA256; 2) Removemos a execução como root, criando usuário dedicado 10001:10001; 3) Removemos ADMIN_PASSWORD da imagem; 4) Substituímos o servidor Flask de desenvolvimento pelo Gunicorn de produção; 5) Desligamos o modo debug; 6) Travamos dependências por hashes. No runtime, nosso docker-run-seguro.sh roda o container em read-only, com cap-drop=ALL e no-new-privileges.”",
        "Destacar a escolha por Alpine para reduzir a superfície de ataque e o apk upgrade para atualizar pacotes do SO."
    ))

    # Quebra de página para manter organização visual
    story.append(PageBreak())

    # Slide 5
    story.append(render_slide(
        5, "EVIDÊNCIAS LOCAIS", "3:30–4:30",
        "Resultados Registrados",
        "Júlio Santos",
        "Arquivo docs/hardening.md, docs/evidencias/resumo.json e .gitleaksignore.",
        "“Registramos com transparência as métricas antes e depois: no Semgrep local com as regras p/python, p/flask e p/security-audit, tínhamos 10 achados no código original e zero no código corrigido. No scan de imagem com o Trivy para severidades HIGH e CRITICAL, caímos de 388 ocorrências na imagem base original para zero na imagem final. No Gitleaks com fetch-depth: 0, detectamos chaves públicas GPG da base oficial Python; em vez de desligar a regra, tratamos no .gitleaksignore pontualmente pelos fingerprints exatos, mantendo o gate ativo.”",
        "Ressaltar que zero HIGH/CRITICAL é o retrato do scan na data e não uma garantia absoluta perpétua; por isso Dependabot e scans contínuos são vitais."
    ))

    # Slide 6
    story.append(render_slide(
        6, "EXECUTAR NO GITHUB", "4:30–6:30",
        "PR com Vulnerabilidade Controlada (Demo ao Vivo)",
        "Júlio Santos",
        "Aba Pull Requests no GitHub, log do Semgrep no GitHub Actions e botão de Merge bloqueado.",
        "“Demonstramos agora o shift-left na prática: abrimos este Pull Request de teste contendo uma consulta SQL concatenada com dados de formulário no login. Ao disparar o pipeline, o job do Semgrep executou e a flag --error fez a esteira falhar com exit-code 1, indicando a vulnerabilidade exata no log. Voltando à tela do Pull Request, vejam que a branch protection da main impediu completamente o merge. A esteira atuou como barreira bloqueante antes que a vulnerabilidade chegasse à produção.”",
        "Enfatizar a diferença entre o pipeline falhar (Semgrep reprova) e o merge ser bloqueado (GitHub branch protection)."
    ))

    # Slide 7
    story.append(render_slide(
        7, "EXECUTAR NO GITHUB", "6:30–8:30",
        "Correção no Mesmo PR",
        "Júlio Santos",
        "Commit corretivo no mesmo PR, execução verde do Actions e botão de Merge liberado.",
        "“No mesmo Pull Request, submetemos o commit corretivo restaurando a consulta parametrizada com placeholders. O GitHub Actions executou automaticamente a suíte de validações. O Semgrep rodou e foi aprovado com zero achados. Com os 5 required checks verdes e a validação do CODEOWNERS aprovada, a proteção de branch do GitHub desbloqueou o botão de Merge. O desenvolvedor corrigiu o problema sem desativar a segurança, comprovando a eficácia do Quality Gate.”",
        "Mostrar que nenhum scan foi pulado e nenhuma flag de bypass foi utilizada."
    ))

    # Slide 8
    story.append(render_slide(
        8, "ENCERRAMENTO", "8:30–10:00",
        "Aprendizado e Conferência Final",
        "Júlio Santos",
        "Slide 8 do PDF, arquivo docs/resumo-atividade.md e tabela de status checks.",
        "“Para encerrar, nosso aprendizado mais importante foi que ferramentas isoladas não resolvem segurança: a proteção real decorre da disciplina de governança da branch main exigindo os quality gates. Aprendemos também a importância da transparência: corrigir falhas em vez de usar supressões artificiais como # nosemgrep ou --exit-zero. Cumprimos todos os requisitos do enunciado: repositório privado com professor leitor, branch protection ativa, código corrigido, container seguro e evidências reprodutíveis. Estamos à disposição da banca.”",
        "Todos os membros ficam a postos para responder perguntas da banca."
    ))

    # Perguntas Frequentes da Banca
    story.append(PageBreak())
    story.append(Paragraph("Guia Rápido para Perguntas da Banca / Professor", section_heading))
    qa_data = [
        [Paragraph("Pergunta Provável", table_header), Paragraph("Resposta Rápida e Firme", table_header)],
        [
            Paragraph("<b>O que realmente impede o merge?</b>", table_cell),
            Paragraph("A regra de proteção de branch do GitHub (Required Status Checks). O pipeline falha via exit-code, e o GitHub não habilita o merge sem aprovação de todos os 5 checks.", table_cell)
        ],
        [
            Paragraph("<b>Por que fetch-depth: 0 no Gitleaks?</b>", table_cell),
            Paragraph("Para analisar o histórico completo do Git. O checkout padrão baixa só o último commit; apagar um segredo de um arquivo não o apaga dos commits anteriores.", table_cell)
        ],
        [
            Paragraph("<b>Para que serve --require-hashes no pip?</b>", table_cell),
            Paragraph("Garante integridade e combate ataques de Supply Chain: o hash SHA256 do pacote baixado deve bater exatamente com o lockfile pré-auditado.", table_cell)
        ],
        [
            Paragraph("<b>Zero no Trivy significa 100% seguro?</b>", table_cell),
            Paragraph("Não. Significa zero CVEs HIGH/CRITICAL conhecidas na data do scan. Como novas vulnerabilidades surgem continuamente, Dependabot e rebuilds regulares são essenciais.", table_cell)
        ]
    ]
    t_qa = Table(qa_data, colWidths=[150, 373])
    t_qa.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_secondary),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_box])
    ]))
    story.append(t_qa)

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    
    # Copiar para os caminhos adicionais se houver
    import shutil
    for extra_path in output_paths[1:]:
        shutil.copyfile(output_paths[0], extra_path)

if __name__ == "__main__":
    out1 = os.path.abspath("docs/Roteiro-Apresentacao-TaskFlow.pdf")
    out2 = os.path.abspath(os.path.expanduser(r"~\Downloads\TaskFlow-Roteiro-Apresentacao.pdf"))
    build_pdf([out1, out2])
    print(f"PDFs gerados com sucesso:\n- {out1}\n- {out2}")
