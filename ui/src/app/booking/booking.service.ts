import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpHeaders } from '@angular/common/http';
import { MessageService } from 'primeng/api';

@Injectable({
  providedIn: 'root'
})
export class BookingService {

  constructor(private _http: HttpClient, private messageService: MessageService) { }

  validateBooking(bookingObj: any): boolean {
    if (bookingObj['name'] == '' || bookingObj['name'] == null) {
      this.callMessageService("error", "Please enter passenger name.");
      return false;
    }
    if (bookingObj['src'] == '' || bookingObj['src'] == null) {
      this.callMessageService("error", "Please enter a source.");
      return false;
    }
    if (bookingObj['destination'] == '' || bookingObj['destination'] == null) {
      this.callMessageService("error", "Please enter a destination.");
      return false;
    }
    if (bookingObj['class'] == '' || bookingObj['class'] == null) {
      this.callMessageService("error", "Please select a class.");
      return false;
    }
    if (bookingObj['departureDate'] == '' || bookingObj['departureDate'] == null) {
      this.callMessageService("error", "Please select date of departure.");
      return false;
    }
    return true;
  }

  callMessageService(type: string, msg: string) {
    this.messageService.add({
      severity: type,
      summary: type[0].toUpperCase() + type.slice(1) + " Message",
      detail: msg,
    });
  }

  validateCreditCard(bookingId, payment: any): boolean {
    if (bookingId == '' || bookingId == null) {
      this.callMessageService("error", "Please enter a valid Booking Id.");
      return false;
    }
    if (payment['ccNumber'] == '' || payment['ccNumber'] == null) {
      this.callMessageService("error", "Please enter a valid credit card number.");
      return false;
    }
    return true;
  }

  confirmBooking(bookingId, payment: any): Observable<any> {
    const headers = new HttpHeaders({ 'Content-Type': 'application/json', })
    return this._http.post<any>('http://127.0.0.1:5000/flightbooking/', {
      "type": "payment",
      "data": {
        "booking_id": bookingId,
        "card_number": payment.ccNumber
      }
    }, { headers, responseType: 'text' as 'json' });
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

  validateCancel(booking_id: any): boolean {
    if (booking_id == '' || booking_id == null) {
      this.callMessageService("error", "Please enter a valid Booking Id.");
      return false;
    }
    return true;
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
  
  validateDateChange(changeObj: any): boolean {
    if (changeObj['bookingid'] == '' || changeObj['bookingid'] == null) {
      this.callMessageService("error", "Please enter a valid Booking Id.");
      return false;
    }
    if (changeObj['departureDate'] == '' || changeObj['departureDate'] == null) {
      this.callMessageService("error", "Please enter a valid Date.");
      return false;
    }
    return true;
  }

  changeDate(changeObj: any): Observable<any> {
    const headers = new HttpHeaders({ 'Content-Type': 'application/json', })
    return this._http.post<any>('http://127.0.0.1:5000/flightbooking/', {
      "type": "update-date",
      "data": {
        "booking_id": changeObj.bookingid,
        "travel_date": changeObj.departureDate
      }
    }, { headers, responseType: 'text' as 'json' });
  }

  makeAddOn(changeObj: any): Observable<any> {
    const headers = new HttpHeaders({ 'Content-Type': 'application/json', })
    return this._http.post<any>('http://127.0.0.1:5000/flightbooking/', {
      "type": "add-on",
      "data": {
        "booking_id": changeObj.bookingid,
        "card_number": changeObj.ccNumber
      }
    }, { headers, responseType: 'text' as 'json' });
  }

}