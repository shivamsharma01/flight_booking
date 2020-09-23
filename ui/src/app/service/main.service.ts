import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class MainService {

  constructor(private _http:HttpClient) {
   }

   getData() : Observable<any> {
    return of({name:'test',age:32});
  }
}
