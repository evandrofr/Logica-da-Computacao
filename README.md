# Lógica da Computação
Repositório privado para a entrega das atividades da disciplina de Lógica da Computação. 

Para utilizar o compilador basta utilizar o comando abaixo em seu prompt de comando:<br>

`python main.py "<operações>"`

Exemplo:<br>

`python main.py "(22+18)/2 - 15*2"`

## Diagrama Sintático
<img src="Imagens/diagrama_term_expression.png">
<img src="Imagens/diagrama_factor.png">

## EBNF
```
EXPRESSION = TERM, {("+"|"-"), TERM};
TERM = FACTOR, {("*"|"/"), FACTOR};
FACTOR = ("+"|"-"), FACTOR | "(", EXPRESSION, ")" | NUM;
```
