import { Component } from '@angular/core';

@Component({
  selector: 'app-transactions',
  standalone: true,
  imports: [],
  templateUrl: './transactions.component.html',
  styleUrl: './transactions.component.css'
})
export class TransactionsComponent {
  transactions = [
    {
      id:'1',
      amount:'100',
    },
    {
      id:'1',
      amount:'100',
    },
  ]
}
