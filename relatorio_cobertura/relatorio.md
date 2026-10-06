



6. Qual foi o caso de teste mais importante? Por quê?

Foi o test_baixar_quantidade_negativa. Ele foi o único que revelou um defeito real no sistema: Estoque.baixar(1, -5) não é rejeitado e ainda aumenta o estoque. Os outros testes confirmam que as regras funcionam, mas esse mostrou um comportamento incorreto que passaria despercebido, e que poderia gerar estoque inventado em um sistema real.

7. Qual valor de borda apresentou maior risco?

O subtotal de R$ 300, por causa da regra >= 300 do frete grátis. Um erro de operador (> no lugar de >=) mudaria o resultado exatamente nesse valor, e o frete passaria de 0 para 15, 30 ou 50. Por isso o test_frete_gratis_subtotal_300 usa subtotal exatamente 300. Outras bordas testadas foram: distância 10 e 11 km (faixas de frete), 31 km, subtotal 500 (desconto de 5%) e quantidade igual ao estoque mais 1.

8. Quais dependências foram isoladas e por quê?

O Estoque e o EmailService foram identificados como dependências. O EmailService é o que mais precisa ser isolado, pois em um sistema real enviaria um e-mail de verdade, tornando o teste lento e dependente de rede. Na versão apresentada, o método enviar() apenas simula o envio e retorna True. Portanto, os testes utilizam essa versão simulada, sem substituição por Mock ou Stub. O Estoque utiliza um dicionário em memória, que é recriado no setUp() para cada teste, assegurando a independência dos testes.

9. Qual a diferença entre Stub e Mock no seu projeto?
Um stub oferece uma resposta controlada para a unidade em teste (por exemplo, um enviar() que sempre retorna True). Um mock também substitui a dependência, porém possibilita a verificação da interação: se foi invocada, quantas vezes e com quais argumentos (por exemplo, assert_called_once_with(...)). Em resumo, o stub responde, enquanto o mock observa. Neste projeto, como foi utilizada a dependência simulada do próprio sistema, nenhum dos dois foi empregado nos testes.

10. 
Não. Medindo a execução do sistema.py com os 17 testes, 75 das 77 linhas foram executadas. Ficaram de fora duas linhas:
o raise ValueError("Estoque insuficiente") dentro de Pedido.adicionar_item (nenhum teste adiciona uma quantidade maior que o estoque);
o return 50 de Pedido.calcular_frete (nenhum teste usa distância acima de 30 km com frete cobrado).
Como resultado, os branches também não estão completos: falta o lado verdadeiro da quantidade > produto["estoque"] em adicionar_item e o último caminho do frete (distância > 30).