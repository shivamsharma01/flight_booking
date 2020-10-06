import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { BookingService } from '../booking/booking.service';

@Component({
  selector: 'app-cancel-booking',
  templateUrl: './cancel-booking.component.html',
  styleUrls: ['./cancel-booking.component.css']
})
export class CancelBookingComponent implements OnInit {
  cancelForm: FormGroup;

  constructor(private _bookingService: BookingService) { }

  ngOnInit(): void {
    this.initForms();
  }

  initForms() {
    this.cancelForm = new FormGroup({
      bookingid: new FormControl('')
    });
  }

  cancelBooking() {
    if (this._bookingService.validateCancel(this.cancelForm.get('bookingid').value)) {
      this._bookingService.cancelTicket(this.cancelForm.get('bookingid').value).subscribe((data: any) => {
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
