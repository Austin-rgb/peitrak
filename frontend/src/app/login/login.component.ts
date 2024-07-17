import { Component } from '@angular/core';
import { AuthenticationService } from '../authentication.service';
import { Router } from '@angular/router';
import { error } from 'console';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  username: string = ''
  password: string = ''
  constructor(private authService: AuthenticationService, private router: Router) {

  }
  login() {
    this.authService.token_obtain(this.username, this.password).subscribe(
      response => {
        localStorage.setItem('access_token', response.access)
        localStorage.setItem('refresh_token', response.refresh)
        this.router.navigate(['/'])
      },
      error => {
        console.log('login failed', error)
      }
    )
  }
}
