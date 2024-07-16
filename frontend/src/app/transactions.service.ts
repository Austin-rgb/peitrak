import { Injectable } from '@angular/core';
@Injectable({
  providedIn: 'root'
})

export class TransactionsService {
  url = 'http:localhost:8000/api'
  constructor() { }
  async getTransactions():Promise<Array<Transaction>>{
    let transactions:Transaction[] = [
      {
        id:'1',
        amount:100,
      },
      {
        id:'2',
        amount:200,
      },
      {
        id:'3',
        amount:300,
      },
    ]
    return transactions
  }
  async cancelTransaction(id:string):Promise<boolean>{
    return true
  }
  async sendTransaction(destination:string,amount: any):Promise<boolean>{
    console.log(amount)
    return true
  }
  async rejectTransaction(id:string):Promise<boolean>{
    return true
  }
}
export class Transaction {
  id: string = '';
  amount: number = .0;
}

