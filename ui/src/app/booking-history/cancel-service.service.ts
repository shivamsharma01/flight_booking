import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CancelServiceService {

  constructor(private _http:HttpClient) { }

  cancelTicket(cancelObj:any): Observable<any> {
    return this._http.post('http://127.0.0.1:5000/flightbooking/',cancelObj)
  }
}
