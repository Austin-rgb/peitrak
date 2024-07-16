import { Injectable } from '@angular/core';
@Injectable({
  providedIn: 'root'
})

export class TransactionsService {
  url = 'http:localhost:8000/api'
  constructor() { }
  async getTransactions(): Promise<Array<Transaction>> {
    let transactions: Transaction[] = [
      {
        id: '1',
        amount: 100,
        sent: false,
        sent_on: 'today'
      },
      {
        id: '2',
        amount: 200,
        sent: false,
        sent_on: 'today'
      },
      {
        id: '3',
        amount: 300,
        sent: false,
        sent_on: 'today'
      },
    ]
    return transactions
  }
  async cancelTransaction(id: string): Promise<boolean> {
    console.log('cancelled transaction')
    return true
  }
  async sendTransaction(destination: string, amount: any): Promise<boolean> {
    console.log(amount)
    return true
  }
  async rejectTransaction(id: string): Promise<boolean> {
    console.log(`rejected transaction ${id}`)
    return true
  }
  async receiveTransaction(id: string, pin: number): Promise<boolean> {
    console.log(`received transaction ${id}`)
    return true
  }
}
export interface Transaction {
  id: string;
  amount: number;
  sent: boolean;
  sent_on: string;
}

