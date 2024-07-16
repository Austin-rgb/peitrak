import { Component, inject } from '@angular/core';
import { NgFor } from '@angular/common';
import { CommonModule } from '@angular/common';
import { TransactionsService } from '../transactions.service';
import { Transaction } from "../transactions.service";
import { MatButtonModule } from '@angular/material/button'
import { MatTableModule } from '@angular/material/table'
@Component({
  selector: 'app-transactions',
  standalone: true,
  imports: [
    NgFor,
    CommonModule,
    MatButtonModule,
    MatTableModule
  ],
  templateUrl: './transactions.component.html',
  styleUrl: './transactions.component.css'
})
export class TransactionsComponent {
  transactions: Transaction[] = []
  displayedColumns: string[] = ['id', 'amount', 'sent_on']
  trnsactionsService: TransactionsService = inject(TransactionsService)
  constructor() {
    this.trnsactionsService.getTransactions().then((data) => {
      this.transactions = data
    })
  }
}
