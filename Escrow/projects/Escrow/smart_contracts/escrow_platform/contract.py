from typing import TypeAlias
from algopy import *



Buyer: TypeAlias = Account
Escrow: TypeAlias = Account
MaybeEscrow: TypeAlias = Account

class EscrowFactory(ARC4Contract):
    """
    A smart contracts that creates an account and rekeys it to the sender.
    """

    @arc4.abimethod(create="require", allow_actions=[OnCompleteAction.DeleteApplication])
    def new_escrow(self)->arc4.Address:
        """
        creates an instance of a new account and rekeys it to the sender.

        Returns:
            arc4.Address: The escrow address.
        """
        return arc4.Address(itxn.Payment(receiver=Txn.sender, rekey_to=Txn.sender, fee=0).submit().sender)

ESCROW_FACTORY_APPROVAL = b'\n \x01\x01\x80\x04V\x1d/\xea6\x1a\x00\x8e\x01\x00\x01\x001\x19\x81\x05\x12D1\x18\x14D\x88\x00\x0b\x80\x04\x15\x1f|uLP\xb0"C\x8a\x00\x01\xb11\x00I\x81\x00\xb2\x01\xb2 \xb2\x07"\xb2\x10\xb3\xb4\x00\x89'
ESCROW_FACTORY_CLEAR = b"\n\x81\x01C"

@subroutine
def payment_into(sender: Account, /, *, receiver: Account, amount: UInt64)->None:
    """
    initiates a Payment from the sender to the receiver.

    Args:
        sender (Account): The account to initiate the payment
        receiver (Account): The account to receive the payment
        amount (UInt64): The amount of microAlgos to pay the receiver
    """
    itxn.Payment(
        sender=sender,
        receiver=receiver,
        amount=amount,
        fee=0

    ).submit()


@subroutine
def create_escrow(buyer_acount: Buyer) -> Escrow:
    """
    Creates a new escrow account for buyers and saves it in box storage.

    Args: 
        buyer_acount (Buyer): The buyers account

    Returns:
        Escrow: The escrow account.

    """
    # invoke the escrow factory contract to create a new vault
    address, _txn = arc4.abi_call(
        EscrowFactory.new_escrow,
        approval_program=ESCROW_FACTORY_APPROVAL,
        clear_state_program=ESCROW_FACTORY_CLEAR,
        on_completion=OnCompleteAction.DeleteApplication,
        fee=0
    )
    
    escrow = Account(address.bytes)

    # save (buyer, escrow) pair in box storage
    op.Box.put(buyer_acount.bytes, escrow.bytes)
    return escrow

@subroutine
def check_escrow(buyer_acount: Buyer)->MaybeEscrow:
    """
    checks if buyer's escrow exits

    Args:
        buyer_acount(Buyer): The buyer to find the escrow

    Returns:
        MaybeEscrow: The escrow address if found else zero address 
    """
    maybe_escrow, exists = op.Box.get(buyer_acount.bytes)
    if exists:
        return Account(maybe_escrow)
    else:
        return Global.zero_address

@subroutine
def reclaim_then_close_escrow(buyer_acount: Buyer, escrow: Escrow, receiver: Account) -> UInt64:
    """
    Closes the escrow and transfers it balances to the receiver

    Args:
        buyer_acount(Buyer): The buyer to close the escrow
        escrow(Escrow): The escrow to close
        receiver(Account): The account to transfer the funds to  
    
    Return:
        UInt64: The amount transferred to the receiver
    """
    _deleted = op.Box.delete(buyer_acount.bytes)
    
    return(
        itxn.Payment(
            sender=escrow,
            receiver=receiver,
            amount=escrow.balance,
            close_remainder_to=receiver,
            fee=0
        ).submit().amount

    )

@subroutine
def pay_then_close_escrow(
    buyer_acount: Buyer, 
    escrow: Escrow, receiver: Account, 
    company_address: Account, is_finance: bool) -> UInt64:

    """
    Closes the escrow and transfers it balances to the receiver

    Args:
        buyer_acount(Buyer): The buyer to close the escrow
        escrow(Escrow): The escrow to close
        receiver(Account): The account to transfer the funds to  
    
    Return:
        UInt64: The amount transferred to the receiver
    """
    _deleted = op.Box.delete(buyer_acount.bytes)
    
    if is_finance:
        charges = escrow.balance * UInt64(6//100)
        deduted_charges = escrow.balance - charges
        return(
        itxn.Payment(
            sender=escrow,
            receiver=receiver,
            amount=deduted_charges,
            close_remainder_to=company_address,
            fee=0
        ).submit().amount

        )
    else:
        charges = escrow.balance * UInt64(2//100)
        deduted_charges = escrow.balance - charges
        return(
        itxn.Payment(
            sender=escrow,
            receiver=receiver,
            amount=deduted_charges,
            close_remainder_to=company_address,
            fee=0
        ).submit().amount

        )
    
   


@subroutine
def pay_x_percentage(escrow: Escrow, receiver: Account)-> UInt64:
    """
    pay the seller x percentage from escrow on request

    Args:
        escrow(Escrow): The escrow to pay from
        receiver(Account): The account to transfer the funds to  
    """
    payable_percentage = escrow.balance * UInt64(30//100)
    return(
         itxn.Payment(
            sender=escrow,
            receiver=receiver,
            amount=payable_percentage,
            close_remainder_to=receiver,
            fee=0
        ).submit().amount

    )


class EscrowPlatform(ARC4Contract):
    """
    A Smart contracts for Decentralized Escrow management
    """
    #global variable
    invoice_id: String
    total_products_amount: UInt64
   
    
    @arc4.abimethod(create="require")
    def start_transaction(
        self,
        invoice_id: String,
        total_products_amount: UInt64,
       

    )->None:
        """
        Creates a new transactions

        Args:
            invoice_id (String): The invoice id to use to initiate the transaction
            total_products_amount (Uni64): The total amount of algos charge by the seller
           

        Return:
             None
        """
        assert total_products_amount >= Global.min_balance
        

        self.invoice_id = invoice_id
        self.total_products_amount = total_products_amount
        

    @arc4.abimethod
    def make_payment(self, buyer_payment: gtxn.PaymentTransaction, company_address: arc4.Address)->UInt64:
        """
        Buyers makes payment to the escrow

        Args:
            buyer_payment(gtxn.PaymentTransaction): The payment transfer to the escrow in microalgos

        Returns:
            UInt64: The total amount transferred by the buyer
        """
        charges_inclusive = self.total_products_amount * UInt64(2 // 100)
        assert buyer_payment.amount > UInt64(0)
        assert buyer_payment.receiver == Global.current_application_address, "Payment address must be the application address"
        assert Txn.sender == buyer_payment.sender, "making suere that the account that made the call is  indeed the buyers account"
        assert buyer_payment.amount == self.total_products_amount  + charges_inclusive, "payment must include charges"

        #find or create escrow
        escrow = check_escrow(buyer_payment.sender) or create_escrow(buyer_payment.sender)

        # Pay the money into the escrow
        amount_paid_to_escrow =  buyer_payment.amount - charges_inclusive
        payment_into(Global.current_application_address, receiver=escrow, amount=amount_paid_to_escrow)

        # pay profit into company's  address
        company_addr = Account(company_address.bytes)
        itxn.Payment(
            sender=Global.current_application_address,
            receiver=company_addr,
            amount=Global.current_application_address.balance,
            close_remainder_to=company_addr,
            fee=0
        ).submit().amount
        return escrow.balance



    @arc4.abimethod
    def claim_refund(self, shipping_status:String)-> UInt64:
        """
        Refund a buyer if the shipping is False

        Args:
            shipping_status(String): API endpoint from the shipping company
        
        Returns:
            UInt64: The amount of MicroAlgos refunded.

        """
        assert shipping_status != "shipped"

        escrow = check_escrow(Txn.sender)
        assert escrow
        return reclaim_then_close_escrow(Txn.sender, escrow, receiver=Txn.sender)
    
    @arc4.abimethod
    def withdraw_funds_from_escrow(self, 
        buyer_account: arc4.Address, 
        shipping_status: String, 
        company_address: arc4.Address,
        is_finance: bool )->UInt64:
        """
        deletes the buyer's escrow and transfers its balance to the application creator

        Args:
            buyer_account(arc4.Address): The buyer's address
            shipping_status(String): comfirming from the shipping company if the product is delievered
            company_address(arc4.Address): The address to send charges to
        """
        assert shipping_status == "delivered"
        assert Txn.sender == Global.creator_address
        buyer_acc = Account(buyer_account.bytes)
        company_addr = Account(company_address.bytes)
        escrow = check_escrow(buyer_acc)
        assert escrow

        seller_funds = pay_then_close_escrow(
            buyer_acc, 
            escrow, 
            receiver=Global.creator_address, 
            company_address=company_addr,
            is_finance=is_finance)
        return seller_funds


    @arc4.abimethod
    def request_invoice_financing(self, buyer_account: arc4.Address, shipping_status: String)->UInt64:
        """
        pays the seller some percentage of Algo's
        Args:
            buyer_account(arc4.Address): The buyer's address
            shipping_status(String): comfirming from the shipping company if the product is shipped
        """
        assert shipping_status == "shipped"
        assert Txn.sender == Global.creator_address

        buyer_acc = Account(buyer_account.bytes)
        escrow = check_escrow(buyer_acc)
        assert escrow
        requested_funds = pay_x_percentage(escrow, receiver=Global.creator_address)
        return requested_funds

