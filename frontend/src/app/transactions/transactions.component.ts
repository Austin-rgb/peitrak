import { Component, inject } from '@angular/core';
import { NgFor } from '@angular/common';
import { CommonModule } from '@angular/common';
import { TransactionsService } from '../transactions.service';
import { Transaction } from "../transactions.service";
@Component({
  selector: 'app-transactions',
  standalone: true,
  imports: [NgFor,CommonModule],
  templateUrl: './transactions.component.html',
  styleUrl: './transactions.component.css'
})
export class TransactionsComponent {
  transactions:Transaction[] = []
  trnsactionsService:TransactionsService = inject(TransactionsService)
  constructor(){
    this.trnsactionsService.getTransactions().then((data)=>{
      this.transactions=data
    })
  }
}
