import { Component, Input } from '@angular/core';
import { TransactionsService, Transaction } from '../transactions.service';

@Component({
  selector: 'app-transaction',
  standalone: true,
  imports: [],
  templateUrl: './transaction.component.html',
  styleUrl: './transaction.component.css'
})
export class TransactionComponent {
  @Input() transaction_id: string = 'null'
  @Input() amount: number = .0
  @Input() sent_on: string = 'null'
  transactionService: TransactionsService = new TransactionsService()
  cancel() {
    this.transactionService.cancelTransaction(this.transaction_id)

  }
  reject() {
    this.transactionService.rejectTransaction(this.transaction_id)

  }
  receive() {
    this.transactionService.receiveTransaction(this.transaction_id, 1234)

  }
}
