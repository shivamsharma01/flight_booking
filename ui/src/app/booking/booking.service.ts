import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';
import { HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class BookingService {

  constructor(private _http: HttpClient) { }


  confirmBooking(paymentObj: any): Observable<any> {
    return this._http.post('http://127.0.0.1:5000/flightbooking/', paymentObj)
  }

  bookTicket(bookingObj: any): Observable<any> {
    const headers = new HttpHeaders({ 'Content-Type': 'application/json', })

    return this._http.post<any>('http://127.0.0.1:5000/flightbooking/', {
      "type": "booking",
      "data": {
        "name": bookingObj.name,
        "src_location": bookingObj.src,
        "dest_location": bookingObj.destination,
        "class": bookingObj.class,
        "travel_date": bookingObj.departureDate,
      }
    }, { headers, responseType: 'text' as 'json' });
  }

  cancelTicket(booking_id: any): Observable<any> {
    const headers = new HttpHeaders({ 'Content-Type': 'application/json', })

    return this._http.post<any>('http://127.0.0.1:5000/flightbooking/', {
      "type": "cancel",
      "data": {
        "booking_id": booking_id
      }
    }, { headers, responseType: 'text' as 'json' });
  }

}