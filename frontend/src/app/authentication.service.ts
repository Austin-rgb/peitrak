import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

interface TokenResponse {
  access: string;
  refresh: string;
}
@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {
  private apiUrl = 'http://localhost:8000/peitrak/api/'
  constructor(private http: HttpClient) { }
  token_obtain(username: string, password: string): Observable<TokenResponse> {
    return this.http.post<TokenResponse>(`${this.apiUrl}token/`, { username, password })
  }
  token_refresh(username: string, password: string): Observable<TokenResponse> {
    return this.http.post<TokenResponse>(`${this.apiUrl}token/refresh/`, { username, password })
  }
}
