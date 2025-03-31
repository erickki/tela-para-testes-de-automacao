import flet as ft
import pandas as pd
import datetime

FONTE = "JetBrains Mono"

def tela(page: ft.Page):
    
    page.title = "Programa."
    page.bgcolor = "#16161a"
    page.window.width= 1920
    page.window.height = 1080
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.alignment = ft.alignment.center
    page.window.maximized = True
    page.padding = 10
    page.window.center()

    def carregar_dados():
        df = pd.read_excel("banco_de_dados.xlsx")
        return df

    def atualizar_tabela():
        df = carregar_dados()
        linhas_novas = [ft.DataRow(
                                cells=[
                                        ft.DataCell(
                                                content=ft.TextField(value=str(df.iloc[i, j]),
                                                text_align=ft.TextAlign.CENTER,
                                                show_cursor=False,
                                                border_color=ft.colors.TRANSPARENT,
                                                text_style=ft.TextStyle(size=18, font_family=FONTE, color="#fffffe"),
                                                read_only=True)
                                        )
                                        for j in range(len(df.columns))
                                ]
                        )
                        for i in range(len(df))
                        ]
        tabela.rows = linhas_novas
        page.update()

    def cadastrar_produto(e):
        df = carregar_dados()
        novo_id = len(df)
        nome = nome_produto.content.value.strip()
        descricao = nome_descricao.content.value.strip()
        status_produto = "Pode ser vendido" if status.content.value else "Não pode ser vendido"
        log = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        if not nome or not descricao:
            page.snack_bar = ft.SnackBar(ft.Text(
                                            value="Preencha todos os campos!", 
                                            text_align=ft.TextAlign.START,
                                            font_family=FONTE,
                                            size=20,
                                            weight=ft.FontWeight.BOLD,
                                            color="#fffffe"
                                        ), 
                                        bgcolor="#b62c2c"
                                        )
            page.snack_bar.open = True
            page.update()
            return
        nova_linha = pd.DataFrame([[
            novo_id, nome, descricao, status_produto, log]],
            columns=["ID", "Nome", "Descrição", "Status", "LOG"])
        df = pd.concat([df, nova_linha], ignore_index=True)
        df.to_excel("banco_de_dados.xlsx", index=False)
        atualizar_tabela()
        nome_produto.content.value = ""
        nome_descricao.content.value = ""
        status.content.value = False
        page.update()

    def filtrar_produto(e):
        df = carregar_dados()
        filtro = nome_produto.content.value.strip()
        if filtro:
            df = df[df["Nome"].str.contains(filtro, na=False)]
        linhas_novas = [ft.DataRow(
            cells=[
                ft.DataCell(
                    content=ft.TextField(
                                value=str(df.iloc[i, j]),
                                text_align=ft.TextAlign.CENTER,
                                show_cursor=False,
                                border_color=ft.colors.TRANSPARENT,
                                text_style=ft.TextStyle(size=18, font_family=FONTE, color="#fffffe"),
                                read_only=True,
                            )
                )
                    for j in range(len(df.columns))
            ]
        )
        for i in range(len(df))
        ]
        tabela.rows = linhas_novas
        page.update()

    def excluir_produto(e):
        df = carregar_dados()
        nome = nome_produto.content.value.strip()
        if not nome:
            page.snack_bar = ft.SnackBar(ft.Text(
                                            value="Digite o nome do produto para excluir!", 
                                            text_align=ft.TextAlign.START,
                                            font_family=FONTE,
                                            size=20,
                                            weight=ft.FontWeight.BOLD,
                                            color="#fffffe"
                                        ), 
                                        bgcolor="#b62c2c"
                                        )
            page.snack_bar.open = True
            page.update()
            return
        df = df[df["Nome"] != nome]
        df.to_excel("banco_de_dados.xlsx", index=False)
        atualizar_tabela()
        nome_produto.content.value = ""
        page.update()

    nome_produto = ft.Container(
        content=ft.TextField(
            text_align=ft.TextAlign.START,
            show_cursor=True,
            cursor_color="#7f5af0",
            cursor_width=2,
            selection_color="#2cb67d",
            text_size=18,
            label="Nome do Produto",
            color="#7f5af0",
            bgcolor="#16161a",
            border_radius=10,
            border_width=2,
            border_color="#fffffe",
            width=364, height=50,
            text_style=ft.TextStyle(size=18, font_family=FONTE, color="#7f5af0"),
            label_style=ft.TextStyle(size=20,font_family=FONTE, color="#fffffe", weight=ft.FontWeight.BOLD)
        )
    )

    nome_descricao = ft.Container(
        content=ft.TextField(
            text_align=ft.TextAlign.START,
            show_cursor=True,
            cursor_color="#7f5af0",
            cursor_width=2,
            selection_color="#2cb67d",
            text_size=18,
            label="Nome da Descrição",
            color="#7f5af0",
            bgcolor="#16161a",
            border_radius=10,
            border_width=2,
            border_color="#fffffe",
            width=364,
            height=50,
            text_style=ft.TextStyle(size=18, font_family=FONTE, color="#7f5af0"),
            label_style=ft.TextStyle(size=20, font_family=FONTE, color="#fffffe", weight=ft.FontWeight.BOLD)
        )
    )

    status = ft.Container(
        content=ft.Switch(
            label="O Produto pode ser vendido?",
            label_position=ft.LabelPosition.LEFT,
            label_style=ft.TextStyle(size=18,  font_family=FONTE, color="#fffffe", weight=ft.FontWeight.BOLD),
            active_color="#7f5af0", width=364, height=50
        ),
        alignment=ft.alignment.center
    )

    botao_cadastrar = ft.Container(
        ft.Text(
            value="Cadastrar",
            text_align=ft.TextAlign.CENTER,
            font_family=FONTE,
            size=20,
            weight=ft.FontWeight.BOLD,
            color="#fffffe"
        ),
        alignment=ft.alignment.center,
        bgcolor="#2cb67d",
        border_radius=15,
        width=150,
        height=30,
        on_click=cadastrar_produto
    )

    botao_filtrar = ft.Container(
        ft.Text(
            value="Filtrar",
            text_align=ft.TextAlign.CENTER,
            font_family=FONTE,
            size=20,
            weight=ft.FontWeight.BOLD,
            color="#fffffe"
        ),
        alignment=ft.alignment.center,
        bgcolor="#2c73b6",
        border_radius=15,
        width=150,
        height=30,
        on_click=filtrar_produto
    )

    botao_excluir = ft.Container(
        ft.Text(
            value="Excluir",
            text_align=ft.TextAlign.CENTER,
            font_family=FONTE,
            size=20,
            weight=ft.FontWeight.BOLD,
            color="#fffffe"
        ),
        alignment=ft.alignment.center,
        bgcolor="#b62c2c",
        border_radius=15,
        width=150,
        height=30,
        on_click=excluir_produto
    )

    fundo1 = ft.Container(
        ft.Column(
            [
                nome_produto,
                nome_descricao,
                status,
                botao_cadastrar,
                botao_filtrar,
                botao_excluir
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        alignment=ft.alignment.center,
        width=384,
        height=1080,
        bgcolor="#16161a"
    )

    df = carregar_dados()

    def calcular_largura_colunas(df):
        larguras_colunas = {}
        fator_ajuste = 10
        for coluna in df.columns:
            max_length = max(df[coluna].astype(str).apply(len), default=0)
            larguras_colunas[coluna] = max(100, max_length * fator_ajuste) * 1.5
        return larguras_colunas
    
    larguras_colunas = calcular_largura_colunas(df)
    
    linhas_dados = [ft.DataRow(
        cells=[
            ft.DataCell(
                content=ft.TextField(value=str(df.iloc[i, j]),
                text_align=ft.TextAlign.CENTER,
                show_cursor=False,
                border_color=ft.colors.TRANSPARENT,
                text_style=ft.TextStyle(size=18, font_family=FONTE, color="#fffffe"),
                read_only=True)
                )
                for j in range(len(df.columns))
        ]
    )
    for i in range(len(df))
    ]

    colunas_dados = [ft.DataColumn(
        label=ft.Text(
                value=col,
                text_align=ft.TextAlign.CENTER,
                font_family=FONTE,
                size=20,
                weight=ft.FontWeight.BOLD,
                color="#7f5af0",
                width=larguras_colunas[col])
        )
        for col in list(df.columns)
        ]

    tabela = ft.DataTable(
            columns=colunas_dados,
            rows=linhas_dados
    )

    fundo2 = ft.Container(
        ft.Column(
            [
                tabela, ft.Container(expand=True)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        alignment=ft.alignment.center,
        width=1536,
        height=1080,
        bgcolor="#16161a"
    )

    tela_geral = ft.Container(
        ft.Row(
            [
                fundo1, fundo2
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        ),
        alignment=ft.alignment.center
    )

    page.add(tela_geral)

ft.app(target=tela)