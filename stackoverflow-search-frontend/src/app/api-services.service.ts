import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'http://localhost:8000/core02/search';

  constructor(private http: HttpClient) {}

  search(query: string, page: number, abc?:string): Observable<any> {
    const url = `${this.apiUrl}/?q=${query}&page=${page}`;
    return this.http.get(url);
  }
}
