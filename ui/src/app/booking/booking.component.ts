import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { BookingService } from './booking.service';

@Component({
  selector: 'app-booking',
  templateUrl: './booking.component.html',
  styleUrls: ['./booking.component.css']
})
export class BookingComponent implements OnInit {
  dictionary = { 'B': 10000, 'E': 5000, 'F': 20000 };
  bookingForm: FormGroup;
  paymentForm: FormGroup;
  travelClass: any[] = [{ label: 'Ecomomy', value: 'E' }, { label: 'Business', value: 'B' }, { label: 'First class', value: 'F' }];
  clickedBookTicket: boolean;
  booking_id: number;
  price: number;
  constructor(private _bookingService: BookingService) { }

  ngOnInit(): void {
    this.initForms();
  }

  bookTicket() {
    if (this._bookingService.validateBooking(this.bookingForm.value)) {
      this._bookingService.bookTicket(this.bookingForm.value).subscribe((data: any) => {
        console.log(data);
        data = JSON.parse(data);
        if (data.error == false) {
          this.booking_id = data.message.split('-')[1];
          this._bookingService.callMessageService("success", "Seat reserved. Booking ID: " + this.booking_id);
          this.clickedBookTicket = true;
        } else {
          this._bookingService.callMessageService('error', data.message);
        }
      });
    }
  }

  makePayment() {
    if (this._bookingService.validateCreditCard(this.booking_id, this.paymentForm.value)) {
      this._bookingService.confirmBooking(this.booking_id, this.paymentForm.value).subscribe((data: any) => {
        console.log(data);
        data = JSON.parse(data);
        if (data.error == false) {
          this._bookingService.callMessageService("success", data.message);
        } else {
          console.log(data.message);
          this._bookingService.callMessageService('error', data.message);
        }
        this.initForms();
      });
    }
  }

  cancelBooking() {
    if (this._bookingService.validateCancel(this.booking_id)) {
      this._bookingService.cancelTicket(this.booking_id).subscribe((data: any) => {
        console.log(data);
        data = JSON.parse(data);
        if (data.error == false) {
          this._bookingService.callMessageService("success", data.message);
        } else {
          console.log(data.message);
          this._bookingService.callMessageService('error', data.message);
        }
        this.initForms();
      });
    }
  }

  initForms() {
    this.price = 0;
    this.clickedBookTicket = false;
    this.bookingForm = new FormGroup({
      src: new FormControl(''),
      destination: new FormControl(''),
      departureDate: new FormControl(''),
      class: new FormControl(''),
      name: new FormControl(''),
    });

    this.paymentForm = new FormGroup({
      ccNumber: new FormControl('')
    });
    this.bookingForm.get('class').valueChanges.subscribe(val => {
      this.price = this.dictionary[val];
    })
  }

}
