## Estado atual:

main.py: Cadastro e login muito básico para lojas. Nenhuma autenticação.
produtos.py: adição e modificação de produtos com atributos nome, preço, quantidade, categoria. Sem integração com classe de loja (pra mostrar inventário segmentado por loja)

em ambos os arquivos, dados são armazenados em json.

## Próximos passos

- Ajeitar classes com os atributos certinhos que vamos usar
- Adicionar funcionalidade de inventário: criar, deletar, alterar itens
- Adicionar funcionalidade de acompanhar pedidos: depende da parte de regis para versão final
- Testes

Provavelmente não precisa de todos os requirements. 

### para baixar eles mesmo assim:

```pip install -r requirements.txt```

#### executar app

```uvicorn main:app --reload```

### Abrir rotas backend:

adicionar '/docs' no final da url gerada pelo comando anterior
