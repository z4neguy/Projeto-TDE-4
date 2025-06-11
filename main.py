import argparse
import os
import django
import csv
from datetime import date

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from escola.models import Professor, Aluno, Disciplina, Turma, Nota, Frequencia


# Funções de adição individuais
def add_professor(nome, email):
    professor = Professor(nome=nome, email=email)
    professor.save()
    print(f"Professor adicionado: {professor}")


def add_aluno(nome, matricula):
    aluno = Aluno(nome=nome, matricula=matricula)
    aluno.save()
    print(f"Aluno adicionado: {aluno}")


def add_disciplina(nome, professor_id):
    try:
        professor = Professor.objects.get(id=professor_id)
        disciplina = Disciplina(nome=nome, professor=professor)
        disciplina.save()
        print(f"Disciplina adicionada: {disciplina}")
    except Professor.DoesNotExist:
        print("Erro: Professor não encontrado.")


def add_turma(nome, disciplina_id):
    try:
        disciplina = Disciplina.objects.get(id=disciplina_id)
        turma = Turma(nome=nome, disciplina=disciplina)
        turma.save()
        print(f"Turma adicionada: {turma}")
    except Disciplina.DoesNotExist:
        print("Erro: Disciplina não encontrada.")


def add_nota(aluno_id, turma_id, nota):
    try:
        aluno = Aluno.objects.get(id=aluno_id)
        turma = Turma.objects.get(id=turma_id)
        nova_nota = Nota(aluno=aluno, turma=turma, valor=nota)
        nova_nota.save()
        print(f"Nota adicionada: {nova_nota}")
    except (Aluno.DoesNotExist, Turma.DoesNotExist):
        print("Erro: Aluno ou turma não encontrados.")


def add_frequencia(aluno_id, turma_id, data, presente):
    try:
        aluno = Aluno.objects.get(id=aluno_id)
        turma = Turma.objects.get(id=turma_id)
        data_formatada = date.fromisoformat(data)
        freq = Frequencia(aluno=aluno, turma=turma, data=data_formatada, presente=presente)
        freq.save()
        print(f"Frequência registrada: {freq}")
    except (Aluno.DoesNotExist, Turma.DoesNotExist):
        print("Erro: Aluno ou turma não encontrados.")
    except ValueError:
        print("Erro: Data inválida. Use o formato YYYY-MM-DD.")


def importar_csv_professores(arquivo):
    with open(arquivo, newline='', encoding='utf-8') as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            add_professor(
                nome=linha['nome'],
                email=linha['email']
            )


def importar_csv_alunos(arquivo):
    with open(arquivo, newline='', encoding='utf-8') as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            add_aluno(
                nome=linha['nome'],
                matricula=linha['matricula']
            )


def importar_csv_disciplinas(arquivo):
    with open(arquivo, newline='', encoding='utf-8') as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            try:
                professor = Professor.objects.get(email=linha['email_professor'])
                add_disciplina(
                    nome=linha['nome'],
                    professor_id=professor.id
                )
            except Professor.DoesNotExist:
                print(f"Professor com e-mail {linha['email_professor']} não encontrado.")


def importar_csv_turmas(arquivo):
    with open(arquivo, newline='', encoding='utf-8') as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            try:
                disciplina = Disciplina.objects.get(nome=linha['nome_disciplina'])
                add_turma(
                    nome=linha['nome'],
                    disciplina_id=disciplina.id
                )
            except Disciplina.DoesNotExist:
                print(f"Disciplina {linha['nome_disciplina']} não encontrada.")


def importar_csv_notas(arquivo):
    with open(arquivo, newline='', encoding='utf-8') as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            try:
                aluno = Aluno.objects.get(matricula=linha['matricula'])
                turma = Turma.objects.get(nome=linha['nome_turma'])
                add_nota(
                    aluno_id=aluno.id,
                    turma_id=turma.id,
                    nota=float(linha['nota'])
                )
            except (Aluno.DoesNotExist, Turma.DoesNotExist):
                print(f"Erro com aluno {linha['matricula']} ou turma {linha['nome_turma']}")


def importar_csv_frequencias(arquivo):
    with open(arquivo, newline='', encoding='utf-8') as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            try:
                aluno = Aluno.objects.get(matricula=linha['matricula'])
                turma = Turma.objects.get(nome=linha['nome_turma'])
                presente = linha['presente'].strip().lower() == 'true'
                add_frequencia(
                    aluno_id=aluno.id,
                    turma_id=turma.id,
                    data=linha['data'],
                    presente=presente
                )
            except Exception as e:
                print(f"Erro ao importar frequência: {e}")



def listar_professores():
    for p in Professor.objects.all():
        print(f"{p.id}: {p.nome} - {p.email}")


def listar_alunos():
    for a in Aluno.objects.all():
        print(f"{a.id}: {a.nome} - Matrícula: {a.matricula}")


def listar_disciplinas():
    for d in Disciplina.objects.all():
        print(f"{d.id}: {d.nome} - Professor: {d.professor.nome}")


def listar_turmas():
    for t in Turma.objects.all():
        print(f"{t.id}: {t.nome} - Disciplina: {t.disciplina.nome}")


def listar_notas():
    for n in Nota.objects.all():
        print(f"{n.id}: Aluno: {n.aluno.nome}, Turma: {n.turma.nome}, Nota: {n.valor}")


def listar_frequencias():
    for f in Frequencia.objects.all():
        print(f"{f.id}: Aluno: {f.aluno.nome}, Turma: {f.turma.nome}, Data: {f.data}, Presente: {f.presente}")


def main():
    parser = argparse.ArgumentParser(description="Sistema Escolar - CLI")
    subparsers = parser.add_subparsers(dest="comando")

    
    parser_prof = subparsers.add_parser("add-professor")
    parser_prof.add_argument("--nome", required=True)
    parser_prof.add_argument("--email", required=True)

    parser_aluno = subparsers.add_parser("add-aluno")
    parser_aluno.add_argument("--nome", required=True)
    parser_aluno.add_argument("--matricula", required=True)

    parser_disc = subparsers.add_parser("add-disciplina")
    parser_disc.add_argument("--nome", required=True)
    parser_disc.add_argument("--professor-id", type=int, required=True)

    parser_turma = subparsers.add_parser("add-turma")
    parser_turma.add_argument("--nome", required=True)
    parser_turma.add_argument("--disciplina-id", type=int, required=True)

    parser_nota = subparsers.add_parser("add-nota")
    parser_nota.add_argument("--aluno-id", type=int, required=True)
    parser_nota.add_argument("--turma-id", type=int, required=True)
    parser_nota.add_argument("--nota", type=float, required=True)

    parser_freq = subparsers.add_parser("add-frequencia")
    parser_freq.add_argument("--aluno-id", type=int, required=True)
    parser_freq.add_argument("--turma-id", type=int, required=True)
    parser_freq.add_argument("--data", type=str, default=str(date.today()))
    parser_freq.add_argument("--presente", type=str, choices=['true', 'false'], default='true')

    
    parser_csv_prof = subparsers.add_parser("add-professores-batch")
    parser_csv_prof.add_argument("--arquivo", required=True)

    parser_csv_aluno = subparsers.add_parser("add-alunos-batch")
    parser_csv_aluno.add_argument("--arquivo", required=True)

    parser_csv_disc = subparsers.add_parser("add-disciplinas-batch")
    parser_csv_disc.add_argument("--arquivo", required=True)

    parser_csv_turma = subparsers.add_parser("add-turmas-batch")
    parser_csv_turma.add_argument("--arquivo", required=True)

    parser_csv_nota = subparsers.add_parser("add-notas-batch")
    parser_csv_nota.add_argument("--arquivo", required=True)

    parser_csv_freq = subparsers.add_parser("add-frequencias-batch")
    parser_csv_freq.add_argument("--arquivo", required=True)

    # Comandos de listagem
    subparsers.add_parser("listar-professores")
    subparsers.add_parser("listar-alunos")
    subparsers.add_parser("listar-disciplinas")
    subparsers.add_parser("listar-turmas")
    subparsers.add_parser("listar-notas")
    subparsers.add_parser("listar-frequencias")

    args = parser.parse_args()

    # Roteamento dos comandos
    match args.comando:
        case "add-professor":
            add_professor(args.nome, args.email)
        case "add-aluno":
            add_aluno(args.nome, args.matricula)
        case "add-disciplina":
            add_disciplina(args.nome, args.professor_id)
        case "add-turma":
            add_turma(args.nome, args.disciplina_id)
        case "add-nota":
            add_nota(args.aluno_id, args.turma_id, args.nota)
        case "add-frequencia":
            presente_bool = args.presente.lower() == 'true'
            add_frequencia(args.aluno_id, args.turma_id, args.data, presente_bool)

        case "add-professores-batch":
            importar_csv_professores(args.arquivo)
        case "add-alunos-batch":
            importar_csv_alunos(args.arquivo)
        case "add-disciplinas-batch":
            importar_csv_disciplinas(args.arquivo)
        case "add-turmas-batch":
            importar_csv_turmas(args.arquivo)
        case "add-notas-batch":
            importar_csv_notas(args.arquivo)
        case "add-frequencias-batch":
            importar_csv_frequencias(args.arquivo)

        case "listar-professores":
            listar_professores()
        case "listar-alunos":
            listar_alunos()
        case "listar-disciplinas":
            listar_disciplinas()
        case "listar-turmas":
            listar_turmas()
        case "listar-notas":
            listar_notas()
        case "listar-frequencias":
            listar_frequencias()
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
