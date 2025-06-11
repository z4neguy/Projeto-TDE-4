Ok como pedido devidamente no TDE4 fizemos, aqui tanto a questão de ligação do Banco com Django ORM para que os comandos especificados sejam executados, quanto a questão de importação de dados dos Arquivos CSV para o Banco, aqui abaixo estão especificados alguns comandos que podem ser usados qe foram pedidos:

python main.py add-professor --nome "Exemplo" --email "Exemplo.gmail.com"
python main.py add-aluno --nome "Exemplo" --matricula "Exemplo"
python main.py add-disciplina --nome "Exemplo" --professor-id "1"
python main.py add-turma --nome "Exemplo" --disciplina-id "1"
python main.py add-nota --aluno-id "1" --turma-id "1" --nota "8"
python main.py add-frequencia --aluno-id "1" --turma-id "1" --data "22-03-2008" --presente
"True"

python main.py add-professores-batch --arquivo csv/professor.csv
python main.py add-alunos-batch --arquivo csv/aluno.csv
python main.py add-disciplinas-batch --arquivo csv/disciplina.csv
python main.py add-turmas-batch --arquivo csv/turma.csv
python main.py add-notas-batch --arquivo csv/nota.csv
python main.py add-frequencias-batch --arquivo csv/frequencia.csv

python main.py listar-alunos 
python main.py listar-professores  
python main.py listar-turmas  
python main.py listar-disciplinas  
python main.py listar-notas --aluno-id < 
