# Resumo para estudar Linguagem de Programação

## 1 Bibliotecas e módulos

Um módulo é um arquivo Python que reúne código reutilizável. Uma biblioteca oferece recursos prontos; `import` dá acesso a eles. `dataclasses` e `collections` fazem parte da biblioteca padrão. Matplotlib é uma biblioteca externa para gráficos.

Uma classe define a estrutura dos objetos. `Livro` define título, autor, gênero e quantidade. Cada livro cadastrado é um objeto dessa classe. A lista `livros` reúne os objetos e as funções cadastram, filtram e procuram registros.

Uma lista de dicionários é uma alternativa: cada dicionário associa nomes de campos aos valores. Por exemplo, `[{"titulo": "Exemplo", "autor": "Ana", "ano": 2024}]`. O roteiro usa título, autor, gênero e quantidade na classe; sua questão final apresenta outro cenário com ano de publicação.

Validação impede cadastros sem título ou com quantidade negativa. Uma busca deve definir se compara o título inteiro ou procura trechos. Neste projeto, ela procura o título inteiro e ignora caixa e espaços nas extremidades.

Contar títulos e somar exemplares são operações diferentes. Dois títulos com 4 e 3 cópias são dois títulos e sete exemplares. O gráfico do projeto soma exemplares por gênero.

**Pratique:** acrescente um livro; busque com letras maiúsculas; tente cadastrar quantidade -1; explique por que um livro com zero cópias continua cadastrado mas não aparece como disponível.

## 2 Análise e visualização de dados

SQLite é um banco de dados local em arquivo. SQL cria tabelas e consulta registros. `commit()` confirma alterações. Parâmetros `?` separam os valores do texto SQL na inserção.

Pandas trabalha com um DataFrame, uma tabela com colunas e linhas. Antes de analisar, confira valores ausentes, duplicatas e tipos. Datas devem ser convertidas para permitir extração de mês; valores devem ser numéricos para somar.

`groupby()` reúne registros por uma chave; `sum()` soma valores em cada grupo. Receita total é a soma das vendas. Ticket médio é a média do valor dos registros de venda. Participação de uma categoria é sua receita dividida pela receita total, multiplicada por 100.

Matplotlib permite configurar eixos, títulos, cores e salvar gráficos. Seaborn facilita visualizações estatísticas. Gráficos de linha mostram evolução; barras facilitam comparar categorias. Eixos e unidades precisam ser identificados.

Na amostra do roteiro, receita é R$ 8.800,00 e Eletrônicos representa 69,32%. Isso não comprova lucro nem sazonalidade. Há somente 14 registros, sem custos ou quantidades, e os dados são de 2023.

**Pratique:** some receita por categoria; calcule ticket médio; explique a diferença entre faturamento e lucro; diga que dados adicionais você precisaria para sugerir uma promoção.

## 3 Machine Learning

Na aprendizagem supervisionada, o modelo recebe características e respostas conhecidas durante o treinamento. No Iris, `X` contém quatro medidas de cada flor e `y` identifica sua espécie. O modelo tenta aprender uma relação para classificar novas medidas.

Treino ajusta os pesos. Validação ajuda a escolher quando parar. Teste mede o resultado final em exemplos reservados. Nesta execução foram usados 96 exemplos de treino, 24 de validação e 30 de teste. `stratify` preserva a proporção das classes.

StandardScaler padroniza cada característica: subtrai a média e divide pelo desvio padrão. Use `fit_transform` somente no treino e `transform` nos outros conjuntos. Calcular os parâmetros com todo o conjunto permite que dados do teste influenciem o processo: isso é vazamento de dados.

Uma rede neural tem camadas de neurônios e pesos ajustáveis. ReLU é uma função de ativação das camadas ocultas. Softmax produz três valores cuja soma é um; a maior saída determina a classe prevista. Esses valores não garantem probabilidades perfeitamente calibradas.

Uma época é uma passagem pelos exemplos de treino. Batch é um grupo de exemplos usado em um passo de atualização. A função de perda mede o erro que o otimizador tenta reduzir. EarlyStopping interrompe quando a perda de validação deixa de melhorar e pode restaurar os melhores pesos.

Acurácia é a proporção de acertos. A matriz de confusão mostra quais classes foram confundidas: neste projeto, uma versicolor foi prevista como virginica. O resultado foi 29 acertos em 30 exemplos, ou 96,67%, nesta divisão específica.

Overfitting ocorre quando o modelo se adapta demais ao treino e generaliza mal. Bom desempenho no treino não basta; observe validação e teste. Nunca use o teste repetidamente para escolher a melhor configuração.

**Pratique:** explique por que separar os dados antes de ajustar o scaler; diferencie perda e acurácia; interprete a matriz de confusão; explique por que 96,67% em 30 flores não garante a mesma taxa em novas populações.

## Ordem de revisão

1. Leia o código de livros e identifique classe, lista, função e validação.
2. Acompanhe o caminho dos dados: SQLite → DataFrame → agrupamento → gráfico → interpretação.
3. Acompanhe o modelo: dados → divisão → padronização → rede → treino → teste → previsão.
4. Faça uma alteração pequena em cada notebook e compare a saída.
