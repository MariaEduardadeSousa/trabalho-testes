
import unittest
from sistema import Estoque, EmailService, Pedido
 
class TesteEstoque(unittest.TestCase):
    #-----------------------------------------------------
    def setUp(self):
        self.estoque=Estoque()
        self.email=EmailService()
        self.pedido=Pedido(self.estoque, self.email)
 
    def tearDown(self):
        self.estoque = None
    #-----------------------------------------------------
    #teste com valores invalidos
     #teste produto com id invalido
    def test_buscar_invalido(self):
        with self.assertRaises(ValueError):
         self.estoque.buscar(100)
    def test_baixar_invalido(self):
        with self.assertRaises(ValueError):
            self.estoque.baixar(1,10000)
    def test_adc_item_invalido(self):
        with self.assertRaises(ValueError):
            self.pedido.adicionar_item(1,-9)
    def test_frete_distancia_invalido(self):
        with self.assertRaises(ValueError):
          self.pedido.calcular_frete(-10)
    def test_finalizar_pedido_vazio(self):
        with self.assertRaises(ValueError):
            self.pedido.finalizar("ana@email.com",100,None)
    def test_baixar_quantidade_negativa(self):
        with self.assertRaises(ValueError):
            self.estoque.baixar(1,-5)
    #-----------------------------------------------------
    def test_adc_item(self):
        self.assertIsNone(self.pedido.adicionar_item(1,3))
        #funcao nao tem retorno
        self.assertEqual(1,len(self.pedido.itens))
 
    def test_calcular_desconto(self):
        self.assertEqual(0,self.pedido.calcular_desconto(cupom=None))
        #funcao retorna 0
 
    def test_distancia(self):
        self.assertEqual(15,self.pedido.calcular_frete(10))
 
    def test_cupom_valido(self):
        self.pedido.adicionar_item(1,1)
        self.assertAlmostEqual(300.0,self.pedido.calcular_desconto("DESCONTO10"))
 
    def test_desconto_cupom_invalido_pedido_pequeno(self):
        self.pedido.adicionar_item(2,1)
        self.assertEqual(0,self.pedido.calcular_desconto("CUPOMFALSO"))
 
    def test_desconto_cupom_invalido_pedido_grande(self):
        self.pedido.adicionar_item(1,1)
        self.assertAlmostEqual(150.0,self.pedido.calcular_desconto("CUPOMFALSO"))
 
    def test_desconto_borda_500(self):
        self.pedido.adicionar_item(2,5)
        self.assertAlmostEqual(25.0,self.pedido.calcular_desconto())
 
    def test_frete_borda_11km(self):
        self.pedido.adicionar_item(2,1)
        self.assertEqual(30,self.pedido.calcular_frete(11))
 
    def test_frete_gratis_subtotal_300(self):
        self.pedido.adicionar_item(2,3)
        self.assertEqual(0,self.pedido.calcular_frete(100))
 
    def test_subtotal_varios_itens(self):
        self.pedido.adicionar_item(1,1)
        self.pedido.adicionar_item(2,2)
        self.assertEqual(3200,self.pedido.calcular_subtotal())
 
    def test_finalizar_sucesso(self):
        self.pedido.adicionar_item(1,1)
        resultado=self.pedido.finalizar("ana@email.com",10)
        self.assertEqual("confirmado",resultado["status"])
        self.assertAlmostEqual(2850.0,resultado["total"])
 
if __name__ == "__main__":
    unittest.main()