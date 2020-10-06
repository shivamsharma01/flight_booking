import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { BookingService } from '../booking/booking.service';

@Component({
  selector: 'app-confirm-booking',
  templateUrl: './confirm-booking.component.html',
  styleUrls: ['./confirm-booking.component.css']
})
export class ConfirmBookingComponent implements OnInit {
  confirmForm: FormGroup;
  constructor(private _bookingService: BookingService) { }

  ngOnInit(): void {
    this.initForms();
  }

  initForms() {
    this.confirmForm = new FormGroup({
      bookingid: new FormControl(''),
      ccNumber: new FormControl(''),
    });
  }

  makePayment() {
    if (this._bookingService.validateCreditCard(this.confirmForm.get('bookingid').value, this.confirmForm.value)) {
      this._bookingService.confirmBooking(this.confirmForm.get('bookingid').value, this.confirmForm.value).subscribe((data: any) => {
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

}
