from django.db import models

class Professor(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)  # Adicione unique para evitar emails duplicados
    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True)  # Novo campo
    
    def __str__(self):
        return self.nome

class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=20, unique=True)  # Garante matrículas únicas
    email = models.EmailField(blank=True, null=True)  # Novo campo opcional
    
    def __str__(self):
        return f"{self.nome} ({self.matricula})"  # Melhor representação

class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    creditos = models.PositiveSmallIntegerField(default=4)  # Novo campo importante
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='disciplinas')  # Added related_name
    
    def __str__(self):
        return self.nome

class Turma(models.Model):
    nome = models.CharField(max_length=50)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name='turmas')  # Added related_name
    ano = models.PositiveSmallIntegerField()  # Novo campo importante
    semestre = models.PositiveSmallIntegerField()  # Novo campo importante
    
    class Meta:
        unique_together = ('disciplina', 'ano', 'semestre')  # Evita turmas duplicadas
    
    def __str__(self):
        return f"{self.nome} - {self.ano}/{self.semestre}"

class TurmaAluno(models.Model):  # Modelo que faltava para o relacionamento muitos-para-muitos
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    data_matricula = models.DateField(auto_now_add=True)
    
    class Meta:
        unique_together = ('turma', 'aluno')

class Nota(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='notas')
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='notas')
    valor = models.DecimalField(max_digits=4, decimal_places=2)  # Melhor que FloatField para notas
    data_lancamento = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('aluno', 'turma')  # Um aluno só tem uma nota por turma

class Frequencia(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='frequencias')
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='frequencias')
    data = models.DateField()
    presente = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('aluno', 'turma', 'data')  # Evita registros duplicados