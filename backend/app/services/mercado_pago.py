"""Serviço de integração com Mercado Pago"""
import requests
from datetime import datetime, timedelta
from decimal import Decimal
from typing import List, Dict, Any, Optional


class MercadoPagoService:
    """Serviço para integração com API do Mercado Pago"""
    
    BASE_URL = "https://api.mercadopago.com"
    
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    
    def get_account_balance(self) -> Dict[str, Any]:
        """Obtém saldo da conta Mercado Pago"""
        url = f"{self.BASE_URL}/users/me/balance"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro ao consultar saldo: {str(e)}")
    
    def get_payment_methods(self) -> List[Dict[str, Any]]:
        """Lista métodos de pagamento disponíveis"""
        url = f"{self.BASE_URL}/v1/payment_methods"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro ao consultar métodos: {str(e)}")
    
    def search_payments(
        self,
        begin_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Busca pagamentos/recebimentos em um período
        
        Formatos de data: ISO 8601 (2024-01-01T00:00:00.000-03:00)
        """
        url = f"{self.BASE_URL}/v1/payments/search"
        
        # Definir período padrão (últimos 30 dias)
        if not end_date:
            end = datetime.now()
            end_date = end.strftime("%Y-%m-%dT%H:%M:%S.000-03:00")
        
        if not begin_date:
            begin = datetime.now() - timedelta(days=30)
            begin_date = begin.strftime("%Y-%m-%dT%H:%M:%S.000-03:00")
        
        params = {
            "limit": limit,
            "offset": offset,
            "range": "date_created",
            "begin_date": begin_date,
            "end_date": end_date
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data.get("results", [])
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro ao buscar pagamentos: {str(e)}")
    
    def get_all_payments_period(
        self,
        days: int = 30
    ) -> List[Dict[str, Any]]:
        """Obtém todos os pagamentos de um período (com paginação automática)"""
        end = datetime.now()
        begin = end - timedelta(days=days)
        
        begin_date = begin.strftime("%Y-%m-%dT%H:%M:%S.000-03:00")
        end_date = end.strftime("%Y-%m-%dT%H:%M:%S.000-03:00")
        
        all_payments = []
        offset = 0
        limit = 100
        
        while True:
            payments = self.search_payments(begin_date, end_date, limit, offset)
            
            if not payments:
                break
            
            all_payments.extend(payments)
            
            # Se retornou menos que o limite, acabou
            if len(payments) < limit:
                break
            
            offset += limit
        
        return all_payments
    
    def convert_to_transacao(
        self,
        payment: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Converte um pagamento Mercado Pago para formato de transação do sistema"""
        try:
            # Extrair dados básicos
            mp_id = payment.get("id")
            status = payment.get("status")
            status_detail = payment.get("status_detail")
            
            # Só processar pagamentos aprovados
            if status != "approved":
                return None
            
            # Determinar tipo (entrada ou saída)
            operation_type = payment.get("operation_type", "")
            
            if operation_type in ["order_payment", "recurring_payment"]:
                # Pagamento que você fez
                tipo = "saida"
            elif operation_type in ["regular_payment", "payment"]:
                # Pagamento que você recebeu
                tipo = "entrada"
            else:
                # Analisar pelo valor
                transaction_amount = payment.get("transaction_amount", 0)
                if transaction_amount < 0:
                    tipo = "saida"
                    transaction_amount = abs(transaction_amount)
                else:
                    tipo = "entrada"
            
            # Extrair valor
            valor = Decimal(str(payment.get("transaction_amount", 0)))
            if valor < 0:
                valor = abs(valor)
            
            # Extrair descrição
            description = payment.get("description", "")
            if not description:
                description = payment.get("external_reference", "Transação Mercado Pago")
            
            # Extrair data
            date_created = payment.get("date_created", "")
            if date_created:
                try:
                    # Converter ISO 8601 para date
                    dt = datetime.fromisoformat(date_created.replace("Z", "+00:00"))
                    data = dt.date().isoformat()
                except:
                    data = datetime.now().date().isoformat()
            else:
                data = datetime.now().date().isoformat()
            
            # Determinar categoria baseada na descrição
            categoria = self._detectar_categoria(description, operation_type)
            
            # Forma de pagamento para observação
            payment_method = payment.get("payment_method_id", "")
            payment_type = payment.get("payment_type_id", "")
            
            observacao = f"Mercado Pago - ID: {mp_id}"
            if payment_method:
                observacao += f" - Método: {payment_method}"
            
            return {
                "descricao": description or "Transação Mercado Pago",
                "valor": float(valor),
                "tipo": tipo,
                "data": data,
                "categoria": categoria,
                "is_fixa": False,
                "is_recorrente": operation_type == "recurring_payment",
                "observacoes": observacao
            }
            
        except Exception as e:
            print(f"Erro ao converter pagamento {payment.get('id')}: {e}")
            return None
    
    def _detectar_categoria(self, description: str, operation_type: str) -> str:
        """Detecta categoria baseada na descrição"""
        desc_lower = description.lower() if description else ""
        
        # Transferências Pix
        if "pix" in desc_lower or "transferencia" in desc_lower:
            return "transferencia"
        
        # Pagamentos recorrentes/assinaturas
        if operation_type == "recurring_payment":
            return "assinatura"
        
        # Serviços streaming
        if any(x in desc_lower for x in ["netflix", "spotify", "youtube", "prime", "disney"]):
            return "assinatura"
        
        # Alimentação
        if any(x in desc_lower for x in ["ifood", "rappi", "uber eats", "restaurante", "mercado"]):
            return "alimentacao"
        
        # Transporte
        if any(x in desc_lower for x in ["uber", "99", "taxi", "onibus", "combustivel"]):
            return "transporte"
        
        # Serviços
        if any(x in desc_lower for x in ["internet", "luz", "agua", "gas", "telefone"]):
            return "moradia"
        
        # Recebimentos
        if operation_type in ["regular_payment", "payment"]:
            return "recebimento"
        
        return "outros"
    
    def sync_transacoes(
        self,
        days: int = 30
    ) -> List[Dict[str, Any]]:
        """Sincroniza transações do Mercado Pago para o sistema"""
        payments = self.get_all_payments_period(days)
        
        transacoes = []
        for payment in payments:
            transacao = self.convert_to_transacao(payment)
            if transacao:
                transacoes.append(transacao)
        
        return transacoes


def get_mercadopago_service(access_token: str) -> MercadoPagoService:
    """Factory para criar serviço Mercado Pago"""
    return MercadoPagoService(access_token)
