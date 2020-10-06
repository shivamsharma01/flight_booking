import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { BookingService } from '../booking/booking.service';

@Component({
  selector: 'app-change-date',
  templateUrl: './change-date.component.html',
  styleUrls: ['./change-date.component.css']
})
export class ChangeDateComponent implements OnInit {
  changeForm: FormGroup;
  constructor(private _bookingService: BookingService) { }

  ngOnInit(): void {
    this.initForms();
  }

  initForms() {
    this.changeForm = new FormGroup({
      bookingid: new FormControl(''),
      departureDate: new FormControl(''),
    });
  }
  
  changeDate() {
    if (this._bookingService.validateDateChange(this.changeForm.value)) {
      this._bookingService.changeDate(this.changeForm.value).subscribe((data: any) => {
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
