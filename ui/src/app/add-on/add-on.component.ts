import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { BookingService } from '../booking/booking.service';

@Component({
  selector: 'app-add-on',
  templateUrl: './add-on.component.html',
  styleUrls: ['./add-on.component.css']
})
export class AddOnComponent implements OnInit {
  addOnForm: FormGroup;
  constructor(private _bookingService: BookingService) { }

  ngOnInit(): void {
    this.initForms();
  }

  initForms() {
    this.addOnForm = new FormGroup({
      bookingid: new FormControl(''),
      ccNumber: new FormControl(''),
    });
  }

  makePayment() {
    if (this._bookingService.validateCreditCard(this.addOnForm.get('bookingid').value, this.addOnForm.value)) {
      this._bookingService.makeAddOn(this.addOnForm.value).subscribe((data: any) => {
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

