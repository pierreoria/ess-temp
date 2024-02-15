## Estado atual:

main.py: Cadastro e login muito básico para lojas. Nenhuma autenticação.
produtos.py: adição e modificação de produtos com atributos nome, preço, quantidade, categoria. Sem integração com classe de loja (pra mostrar inventário segmentado por loja)

em ambos os arquivos, dados são armazenados em json.

## Próximos passos

- Segmentar conteúdo por loja: só aparecer produtos da loja atualmente logada
- Adicionar funcionalidade de acompanhar pedidos
- Assegurar compatibilidade com todas as outras features: padrão de Classe, padrão de json
- Testes

Provavelmente não precisa de todos os requirements. 

### para baixar eles mesmo assim:

```pip install -r requirements.txt```

#### executar app

```uvicorn main:app --reload```

### Abrir rotas backend:

adicionar '/docs' no final da url gerada pelo comando anterior
