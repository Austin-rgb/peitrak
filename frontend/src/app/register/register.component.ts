import { Component } from '@angular/core';
import { AuthenticationService } from '../authentication.service';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})
export class RegisterComponent {
  username: string = ''
  password: string = ''
  constructor(private authService: AuthenticationService, private router: Router) {

  }
  register() {
    this.authService.token_refresh(this.username, this.password).subscribe(
      response => {
        localStorage.setItem('access_token', response.access)
        localStorage.setItem('refresh_token', response.refresh)
        this.router.navigate(['/'])
      },
      error => {
        console.log('registration failed', error)
      }
    )
  }
}
