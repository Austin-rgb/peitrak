import { NgClass, NgIf } from '@angular/common';
import { Component, Inject, OnInit } from '@angular/core';
import { LoginComponent } from "../login/login.component";
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-start-modal',
  standalone: true,
  imports: [
    NgClass,
    LoginComponent,
    NgIf,
    NgbModule,
  ],
  templateUrl: './start-modal.component.html',
  styleUrl: './start-modal.component.css'
})
export class StartModalComponent {
  title: string = 'Start'
  constructor() { }

}
