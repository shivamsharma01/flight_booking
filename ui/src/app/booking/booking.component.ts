import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { MainService } from '../service/main.service';

@Component({
  selector: 'app-booking',
  templateUrl: './booking.component.html',
  styleUrls: ['./booking.component.css']
})
export class BookingComponent implements OnInit {
  bookingForm: FormGroup;
  paymentForm: FormGroup;
  travelClass: any[] = [{ label: 'Ecomomy', value: 'E' }, { label: 'Business', value: 'B' }, { label: 'First class', value: 'F' }];
  clickedBookTicket: boolean;
  booking_id: number;
  price: number;
  constructor(private _mainService: MainService) { }

  ngOnInit(): void {
    this.initForms();
  }

  bookTicket() {
    console.log(this.bookingForm.value)
    if (this._mainService.validateBooking(this.bookingForm.value)) {
      this._mainService.bookTicket(this.bookingForm.value).subscribe((data: any) => {
        console.log(data);
        data = JSON.parse(data);
        if (data.error == false) {
          this.booking_id = data.booking_id;
          this._mainService.callMessageService("success", "Seat reserved. Booking ID: " + this.booking_id);
          this.clickedBookTicket = true;
        } else {
          this._mainService.callMessageService('error', data.message);
        }
      });
    }
  }

  makePayment() {
    if (this._mainService.validateCreditCard(this.booking_id, this.paymentForm.value)) {
      this._mainService.confirmBooking(this.booking_id, this.paymentForm.value).subscribe((data: any) => {
        console.log(data);
        data = JSON.parse(data);
        if (data.error == false) {
          this._mainService.callMessageService("success", data.success_msg);
        } else {
          console.log(data.message);
          this._mainService.callMessageService('error', data.message);
        }
        this.initForms();
      });
    }
  }

  cancelBooking() {
    if (this._mainService.validateCancel(this.booking_id)) {
      this._mainService.cancelTicket(''+this.booking_id).subscribe((data: any) => {
        console.log(data);
        data = JSON.parse(data);
        if (data.error == false) {
          this._mainService.callMessageService("success", data.success_msg);
        } else {
          console.log(data.message);
          this._mainService.callMessageService('error', data.message);
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
      this.price = this._mainService.dictionary[val];
    })
  }

}
