

from datetime import date
from flask import Flask, render_template, request

app = Flask(__name__)


def calcular_idade(nascimento):
    hoje = date.today()
    return hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))


@app.route('/')
def home():
    return 'Flask funcionando!'


@app.route('/inscricao', methods=['GET', 'POST'])
def inscricao():
    if request.method == 'POST':
        
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        telefone = request.form.get('telefone', '').strip()
        genero = request.form.get('genero')
        curso = request.form.get('curso')
        github = request.form.get('github', '').strip()
        camiseta = request.form.get('camiseta')
        cor_cracha = request.form.get('cor_cracha')
        chegada = request.form.get('chegada')
        restricao = request.form.get('restricao', '').strip()
        motivacao = request.form.get('motivacao', '').strip()
        evento_id = request.form.get('evento_id')

        
        senha = request.form.get('senha', '')
        confirma_senha = request.form.get('confirma_senha', '')

        
        periodo_txt = request.form.get('periodo', '')
        periodo = int(periodo_txt) if periodo_txt.isdigit() else None

        experiencia_txt = request.form.get('experiencia', '')
        experiencia = int(experiencia_txt) if experiencia_txt.isdigit() else None

        
        try:
            nascimento = date.fromisoformat(request.form.get('nascimento', ''))
            idade = calcular_idade(nascimento)
        except ValueError:
            nascimento = None
            idade = None

        
        linguagens = request.form.getlist('linguagens')
        areas = request.form.getlist('areas')

        
        aceite = request.form.get('aceite') is not None
        newsletter = request.form.get('newsletter') is not None

        
        foto = request.files.get('foto')
        foto_nome = foto.filename if foto and foto.filename else None

        
        dados = {
            'nome': nome,
            'email': email,
            'nascimento': nascimento,
            'idade': idade,
            'telefone': telefone,
            'genero': genero,
            'curso': curso,
            'periodo': periodo,
            'experiencia': experiencia,
            'linguagens': linguagens,
            'areas': areas,
            'github': github,
            'camiseta': camiseta,
            'cor_cracha': cor_cracha,
            'chegada': chegada,
            'restricao': restricao,
            'foto': foto_nome,
            'motivacao': motivacao,
            'aceite': aceite,
            'newsletter': newsletter,
            'evento_id': evento_id,
        }
                
        erros = []

        if len(nome) < 3:
            erros.append('O nome deve ter pelo menos 3 caracteres.')

        if '@' not in email:
            erros.append('O e-mail deve conter @.')

        if len(senha) < 6:
            erros.append('A senha deve ter pelo menos 6 caracteres.')

        if senha != confirma_senha:
            erros.append('A senha e a confirmação não são iguais.')

        if idade is None:
            erros.append('Data de nascimento inválida.')
        elif idade < 16:
            erros.append('Você precisa ter pelo menos 16 anos.')

        if periodo is None or not (1 <= periodo <= 10):
            erros.append('O período deve ser um número de 1 a 10.')

        if not linguagens:
            erros.append('Selecione pelo menos uma linguagem.')

        if not aceite:
            erros.append('Você precisa aceitar o regulamento.')

        if len(motivacao) > 500:
            erros.append('A motivação pode ter no máximo 500 caracteres.')

        
        if erros:
            return render_template('inscricao.html', erros=erros, form=request.form)

    
        return render_template('confirmacao.html', dados=dados)

    return render_template('inscricao.html', form=request.form)


if __name__ == '__main__':
    app.run(debug=True)
