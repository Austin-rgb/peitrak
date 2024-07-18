import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { TransactionsComponent } from './transactions/transactions.component';
import { LoginComponent } from "./login/login.component";
import { StartModalComponent } from "./start-modal/start-modal.component";
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { RegisterComponent } from "./register/register.component";

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    RouterOutlet,
    TransactionsComponent,
    LoginComponent,
    RegisterComponent
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'peitrak';
  constructor(private modalService: NgbModal) { }
  open(modal: any) {
    this.modalService.open(modal)
  }
}
