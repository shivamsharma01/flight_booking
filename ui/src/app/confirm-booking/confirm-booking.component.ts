import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { MainService } from '../service/main.service';

@Component({
  selector: 'app-confirm-booking',
  templateUrl: './confirm-booking.component.html',
  styleUrls: ['./confirm-booking.component.css']
})
export class ConfirmBookingComponent implements OnInit {
  confirmForm: FormGroup;
  constructor(private _mainService: MainService) { }

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
    if (this._mainService.validateCreditCard(this.confirmForm.get('bookingid').value, this.confirmForm.value)) {
      this._mainService.confirmBooking(this.confirmForm.get('bookingid').value, this.confirmForm.value).subscribe((data: any) => {
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

}
