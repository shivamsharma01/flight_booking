import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { MainService } from '../service/main.service';

@Component({
  selector: 'app-cancel-booking',
  templateUrl: './cancel-booking.component.html',
  styleUrls: ['./cancel-booking.component.css']
})
export class CancelBookingComponent implements OnInit {
  cancelForm: FormGroup;

  constructor(private _mainService: MainService) { }

  ngOnInit(): void {
    this.initForms();
  }

  initForms() {
    this.cancelForm = new FormGroup({
      bookingid: new FormControl('')
    });
  }

  cancelBooking() {
    if (this._mainService.validateCancel(this.cancelForm.get('bookingid').value)) {
      this._mainService.cancelTicket(this.cancelForm.get('bookingid').value).subscribe((data: any) => {
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
