import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { BookingService } from './booking.service';

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

  constructor(private _bookingService: BookingService) { }

  ngOnInit(): void {
    this.initForms();
  }

  bookTicket() {
    this._bookingService.bookTicket(this.bookingForm.value).subscribe((data: any) => {
      console.log(data);
      data = JSON.parse(data);
      if (data.error == false) {
        this.booking_id = data.message.split('-')[1];
        console.log(this.booking_id);
        this.clickedBookTicket = true;
      } else {
        // display error
        console.log(data.message);
      }
    });

  }

  makePayment() {
    let bookingObj = new BookingObject();
    let paymentObj = new BookingObject();
    bookingObj.type = 'booking';
    paymentObj.type = 'payment';
    bookingObj.data = new Booking();
    paymentObj.data = new PaymentObject();
    bookingObj.data.name = this.bookingForm.get('name')
    bookingObj.data.src_location = this.bookingForm.controls.src
    bookingObj.data.dest_location = this.bookingForm.controls.destination
    bookingObj.data.class = this.bookingForm.controls.class
    bookingObj.data.travel_date = this.bookingForm.controls.departureDate
    let booking = this._bookingService.bookTicket(bookingObj);
    booking.subscribe(data => {
      console.log('data', data)
      if (data) {
        paymentObj.data.booking_id = data.id;
        paymentObj.data.card_number = this.paymentForm.get('ccNumber');
        this._bookingService.confirmBooking(paymentObj).subscribe(payment => {
          console.log('payment success, ticked booked. Your ticket number is :', data.id)
        })
      }
    })
  }

  cancelBooking() {
    this._bookingService.cancelTicket(this.booking_id).subscribe(data => {
      this.clickedBookTicket = false;
      this.initForms();
    });
  }

  initForms() {
    this.bookingForm = new FormGroup({
      src: new FormControl(''),
      destination: new FormControl(''),
      departureDate: new FormControl(''),
      class: new FormControl(''),
      name: new FormControl(''),
    })

    this.paymentForm = new FormGroup({
      ccNumber: new FormControl(''),
      expiryDate: new FormControl(''),
      nameOnCard: new FormControl(''),
      cvv: new FormControl('')
    })
  }

}

export class BookingObject {

  type: any;
  data: any;
}

export class Booking {
  name: any
  src_location: any
  dest_location: any
  class: any
  travel_date: any
}

export class PaymentObject {
  booking_id: any
  card_number: any
}
